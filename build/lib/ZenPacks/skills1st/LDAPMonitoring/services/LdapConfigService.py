"""
LdapConfigService
ZenHub service for providing configuration to the zenldap collector daemon.

    This provides the daemon with a dictionary of datapoints for every device.
"""

import logging
log = logging.getLogger('zen.zenldap')

import Globals
from Products.ZenUtils.Utils import unused

unused(Globals)

from Products.ZenCollector.services.config import CollectorConfigService
from ZenPacks.skills1st.LDAPMonitoring.datasources.LdapDataSource import LdapDataSource


# Your daemon configuration service should almost certainly subclass
# CollectorConfigService to make it as easy as possible for you to implement.
class LdapConfigService(CollectorConfigService):
    """
    ZenHub service for the zenldap collector daemon.
    """

    # When the collector daemon requests a list of devices to poll from ZenHub
    # your service can filter the devices that are returned by implementing
    # this _filterDevice method. If _filterDevice returns True for a device,
    # it will be returned to the collector. If _filterDevice returns False, the
    # collector daemon won't collect from it.
    def _filterDevice(self, device):
        # First use standard filtering.
        filter = CollectorConfigService._filterDevice(self, device)

        """
        only return those with LDAP monitoring
        return CollectorConfigService._filterDevice(self, device) and \
            'LDAPServer' in device.getProperty('zDeviceTemplates', [])
        """

        # If the standard filtering logic said the device shouldn't be filtered
        # we can setup some other contraint.
        ldapFlag = False
        if filter:
            # We only monitor devices that have a template with datasource of type "Ldap Protocol"
            for t in device.getRRDTemplates():
                for ds in t.datasources():
                    if ds.sourcetype == 'Ldap Protocol':
                        ldapFlag = True
            #return device.id.startswith('z')
        #    pass

        #return filter
        return CollectorConfigService._filterDevice(self, device) and ldapFlag
            #'LDAPMonitor' in device.getProperty('zDeviceTemplates', [])

    # The _createDeviceProxy method allows you to build up the DeviceProxy
    # object that will be sent to the collector daemon. Whatever is returned
    # from this method will be sent as the device's representation to the
    # collector daemon. Use serializable types. DeviceProxy works, as do any
    # simple Python types.
    def _createDeviceProxy(self, device):
        proxy = CollectorConfigService._createDeviceProxy(self, device)

        proxy.configCycleInterval = 5 * 60
        proxy.datapoints = []
        proxy.thresholds = []

        perfServer = device.getPerformanceServer()

        compName = device.id
        basepath = device.rrdPath()

        for templ in device.getRRDTemplates():
            dpnames = []
            for ds in filter(lambda ds: isinstance(ds, LdapDataSource), templ.getRRDDataSources()):

                try:
                    proxy.ldapuri = ds.ldapURI(device)
                    proxy.credentials = device.getProperty('zLDAPDN'), device.getProperty('zLDAPPW')
                    proxy.searchFilter = ds.searchFilter
                except:
                    log.error('Device not LDAP: %s' % device)
                    continue

                for dp in ds.getRRDDataPoints():
                    dpname = dp.name()
                    dpnames.append(dpname)
                    proxy.datapoints.append((dp.id,
                                             compName,
                                             "/".join((basepath, dpname)),
                                             dp.rrdtype,
                                             dp.getRRDCreateCommand(perfServer),
                                             dp.rrdmin,
                                             dp.rrdmax))

            dpn = set(dpnames)
            for thr in templ.thresholds():
                if not (thr.enabled and dpn & set(thr.dsnames)):
                    continue
                proxy.thresholds.append(thr.createThresholdInstance(device))

        return proxy


# For diagnostic purposes, allow the user to show the results of the
# proxy creation.
# Run this service as a script to see which devices will be sent to the daemon.
# Add the --device=name flag to see the detailed contents of the proxy that
# will be sent to the daemon
#
if __name__ == '__main__':
    from Products.ZenHub.ServiceTester import ServiceTester
    tester = ServiceTester(LdapConfigService)
    def printer(config):
        # Fill this out
        print config.datapoints
    tester.printDeviceProxy = printer
    tester.showDeviceInfo()

