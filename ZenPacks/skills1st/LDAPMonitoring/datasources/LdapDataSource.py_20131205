# Creating a custom datasource type requires defining a subclass of
# Products.ZenModel.RRDDataSource.RRDDataSource as illustrated below. This
# class gets instantiated, configured and stored in the ZODB everytime someone
# adds this type of datasource to a template.

# You will also need to add an IRRDDataSourceInfo subinterface to control how
# the user interface for configuring this datasource is drawn. This interface
# is typically defined in ../interfaces.py. You will then need to define a
# RRDDataSourceInfo subclass to control how your datasource gets serialized
# for passing through the API. This info adapter class is typically defined in
# ../info.py.

from Products.ZenModel.RRDDataSource import RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from ZenPacks.skills1st.LDAPMonitoring.config import MONITORABLE


class LdapDataSource(ZenPackPersistence, RRDDataSource):

    # All subclasses of ZenPackPersistence need to set their ZENPACKID.
    ZENPACKID = 'ZenPacks.skills1st.LDAPMonitoring'

    # These define how this datasource type is displayed in the datasource type
    # picker when adding a new datasource to a monitoring template. Keep it
    # short and unambiguous.
    sourcetypes = ('Ldap Protocol',)
    sourcetype = sourcetypes[0]

    # Set default values for properties inherited from RRDDataSource.
    eventClass = '/Status/LDAPMonitor'
    component = "${here/id}"

    # Add default values for custom properties of this datasource.
    hostname = '${dev/ip}'
    #ipAddress = '${dev/manageIp}'
    ipAddress = '${dev/id}'

    ldapProto = '${dev/zLDAPProto}'
    ldapPort = '${dev/zLDAPPort}'
    #ldapPort = 389
    ldapDN = '${dev/zLDAPDN}'
    ldapPW = '${dev/zLDAPPW}'
    timeout = 20
    cycletime = 20

    searchFilter = 'cn=monitor'

    _properties = RRDDataSource._properties + (
        {'id':'ldapProto',    'type':'string',    'mode':'w'},
        {'id':'ldapPort',     'type':'string',       'mode':'w'},
        {'id':'ldapDN',       'type':'string',    'mode':'w'},
        {'id':'ldapPW',       'type':'string',    'mode':'w'},
        {'id':'timeout',      'type':'int',       'mode':'w'},
        {'id':'cycletime',    'type':'int',       'mode':'w'},
        {'id':'searchFilter', 'type':'string',    'mode':'r'},
        )

    _relations = RRDDataSource._relations

    def __init__(self, id, title=None, buildRelations=True):
        RRDDataSource.__init__(self, id, title, buildRelations)
        self.addDataPoints()

    def ldapURI(self, device):
        """
        LDAP server connection string - this is really the getCommand() function here
        """
        return self.getCommand(device,
                               "%s://%s:%s" % (self.ldapProto, self.ipAddress, self.ldapPort))

    def getDescription(self):
        return '%s://%s:%s (%s)' % (self.ldapProto, self.hostname, self.ldapPort, self.searchFilter)

    def useZenCommand(self):
        return False

    def checkCommandPrefix(self, context, cmd):
        return cmd

    def addDataPoints(self):
        for dpname, dptype in MONITORABLE:
            # put next section in try/except in case self has no instantiation of the datapoints relationship (or it fails)
            try:
                if not hasattr(self.datapoints, dpname,):
                    dp = self.manage_addRRDDataPoint(dpname,)
                    dp.rrdtype = dptype
                    dp.rrdmin = 0
            except:
                pass



