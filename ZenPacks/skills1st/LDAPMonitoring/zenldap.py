# This is an example of a custom collector daemon.

COLLECTOR_NAME = "zenldap"

import logging
log = logging.getLogger("zen.%s" % COLLECTOR_NAME)

import ldap, time


import Globals
import zope.component
import zope.interface

from twisted.internet import defer

from Products.ZenCollector.daemon import CollectorDaemon
from Products.ZenCollector.interfaces \
    import ICollectorPreferences, IScheduledTask, IEventService, IDataService

from Products.ZenCollector.tasks \
    import SimpleTaskFactory, SimpleTaskSplitter, TaskStates

from Products.ZenUtils.observable import ObservableMixin

# unused is way to keep Python linters from complaining about imports that we
# don't explicitely use. Occasionally there is a valid reason to do this.
from Products.ZenUtils.Utils import unused

# We must import our ConfigService here so zenhub will allow it to be
# serialized and deserialized. We'll declare it unused to satisfy linters.
from ZenPacks.skills1st.LDAPMonitoring.services.LdapConfigService \
    import LdapConfigService


unused(Globals)
unused(LdapConfigService)

from monparsers import parse
from Products.ZenEvents.ZenEventClasses import Error, Clear, Critical
from twisted.python.failure import Failure


# Your implementation of ICollectorPreferences is where you can handle custom
# command line (or config file) options and do global configuration of the
# daemon.
class ZenLdapPreferences(object):
    zope.interface.implements(ICollectorPreferences)

    def __init__(self):
        self.collectorName = 'zenldap'
        self.configurationService = \
            "ZenPacks.skills1st.LDAPMonitoring.services.LdapConfigService"

        # How often the daemon will collect each device. Specified in seconds.
        self.cycleInterval = 5 * 60

        # How often the daemon will reload configuration. In seconds.
        self.configCycleInterval = 5 * 60

        self.options = None

    def buildOptions(self, parser):
        """
        Required to implement the ICollectorPreferences interface.
        """
        pass

    def postStartup(self):
        """
        Required to implement the ICollectorPreferences interface.
        """
        pass


# The implementation of IScheduledTask for your daemon is usually where most
# of the work is done. This is where you implement the specific logic required
# to collect data.
class ZenLdapTask(ObservableMixin):
    zope.interface.implements(IScheduledTask)

    def __init__(self, taskName, deviceId, interval, taskConfig):
        super(ZenLdapTask, self).__init__()
        self._taskConfig = taskConfig

        self._eventService = zope.component.queryUtility(IEventService)
        self._dataService = zope.component.queryUtility(IDataService)
        self._preferences = zope.component.queryUtility(
            ICollectorPreferences, 'zenldap')

        # All of these properties are required to implement the IScheduledTask
        # interface.
        self.name = taskName
        self.configId = deviceId
        self.interval = interval
        self.state = TaskStates.STATE_IDLE
        self._devId = deviceId
        self._manageIp = self._taskConfig.manageIp
        self._datapoints = self._taskConfig.datapoints
        self._thresholds = self._taskConfig.thresholds

    # doTask is where the collector logic should go. It is also required to
    # implement the IScheduledTask interface. It will be called directly by the
    # framework when it's this task's turn to run.

    def _failure(self, result, summary='Could not fetch statistics', severity=Error, comp=None):
        """
        Errback for an unsuccessful asynchronous connection or collection request.
        """
        err = result.getErrorMessage()
        log.error("Device %s: %s", self._devId, err)
        collectorName = self._preferences.collectorName

        self._eventService.sendEvent(dict(
            summary=summary,
            message=err,
            component=comp or collectorName,
            eventClass='/Status/LDAPMonitor',
            device=self._devId,
            severity=severity,
            agent=collectorName,
            ))

         # give the result to the rest of the errback chain
        return result

    def _sendEvents(self, components):
        """
        Send Error and Clear events 
        """
        events = []
        errors = []
        for comp, severity in components.iteritems():
            event = dict(
                summary = "Could not fetch statistics",
                message = "Could not fetch statistics",
                eventClass = '/Status/LDAPMonitor',
                device = self._devId,
                severity = severity,
                agent = self._preferences.collectorName,
                )
            if comp:
                event['component'] = comp
            if isinstance(severity, Failure):
                event['message'] = severity.getErrorMessage()
                event['severity'] = Error
                errors.append(event)
            else:
                events.append(event)

        if len(errors) == len(components) > 0:
            event = errors[0]
            del event['component']
            events.append(event)
        else:
            events.extend(errors)

        for event in events:
            self._eventService.sendEvent(event)

    def _collectSuccessful(self, results={}):
        """
        Callback for a successful fetch of monitor stats from the remote device.
        """
        log.debug("Successful collection from %s [%s], results=%s",
                  self._devId, self._manageIp, results)

        log.info('In collectSuccessful.  self._datapoints is %s \n' % (self._datapoints))
        compstatus = {}
        for dpname, comp, rrdP, rrdT, rrdC, tmin, tmax in self._datapoints:
            value = results.get(dpname, 0)
            compstatus[comp] = Clear
            try:
                self._dataService.writeRRD(rrdP, float(value), rrdT, rrdC, min=tmin, max=tmax)
            except Exception, e:
                compstatus[comp] = Failure(e)
        self._sendEvents(compstatus)
        return results

    def doTask(self):
        log.debug("Polling for stats from %s [%s]", self._devId, self._manageIp)

        ldapuri = self._taskConfig.ldapuri
        ldapcreds = self._taskConfig.credentials
        ldapfilter = self._taskConfig.searchFilter

        log.debug("%s %s %s" % (ldapuri, ldapcreds[0], ldapfilter))

        start_time = time.time()

        slapd = ldap.initialize(ldapuri)

        try:
            slapd.simple_bind_s(*ldapcreds)
        except ldap.INVALID_CREDENTIALS:
            msg = 'authentication failure: %s/%s: check credentials!' % (ldapuri, ldapcreds[0])
            return self._failure(Failure(ldap.LDAPError(msg)))
        except ldap.SERVER_DOWN:
            return self._failure(Failure(ldap.LDAPError('server uncontactable')),
                                 summary='LDAP server uncontactable',
                                 severity=Critical)
        except ldap.LDAPError, e:
            return self._failure(Failure(e))

        # seems some ldap implementations require a + attr list to retrieve operational
        # attributes, but others don't :(
        try:
            # no timeout - we're using this call to set response time ...
            resultseq = slapd.search_s(ldapfilter, ldap.SCOPE_SUBTREE, attrlist=['*', '+'])
        except Exception, e:
            msg = 'search failure(%s): %s?%s: is cn=monitor activated?' % (str(e), ldapuri, ldapfilter)
            return self._failure(Failure(ldap.LDAPError(msg)))

        slapd.unbind()

        # Set response time unit to  millisecondss we typically will get
        #  sub-second response time and we do not want that to represent as the integer 0
        resp_time = (time.time() - start_time) * 1000

        # get monparsers to sort out what was returned ...
        results = parse(resultseq, {'responsetime':resp_time})

        self._collectSuccessful(results)


    # cleanup is required to implement the IScheduledTask interface.
    def cleanup(self):
        pass


if __name__ == '__main__':
    myPreferences = ZenLdapPreferences()
    myTaskFactory = SimpleTaskFactory(ZenLdapTask)
    myTaskSplitter = SimpleTaskSplitter(myTaskFactory)

    daemon = CollectorDaemon(myPreferences, myTaskSplitter)
    daemon.run()
