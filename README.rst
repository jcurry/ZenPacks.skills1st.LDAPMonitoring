=======================
LDAP Monitoring ZenPack 
=======================

Description
===========

This ZenPack started from Alan Milligan's work with the 
ZenPacks.lbn.LDAPMonitor ZenPack, which required various extra pre-requisite
ZenPacks.  This offering is completely standalone but has adapted the core
monitoring from Alan's ZenPack.

It provides a new Zenoss daemon, zenldap, which gathers LDAP data.
it uses zProperties introduced by the ZenPack to authenticate to an LDAP server.

Requirements & Dependencies
===========================

    * Zenoss Versions Supported: 4.x
    * External Dependencies: Acces to LDAP devices must be available for monitoring
    * ZenPack Dependencies: Python ldap
      (check whether there is an ldap directory under $PYTHONPATH)
    * Installation Notes: Restart zenoss entirely after installation
    * Configuration:

Components
==========

The ZenPack introduces new zProperties through the __init__.py in the base directory::

      packZProperties = [
        ('zLDAPProto', 'ldap',       'string'),
        ('zLDAPPort',  389,          'string'),
        ('zLDAPDN',    'cn=Manager', 'string'),
        ('zLDAPPW',    'secret',     'password'),
        ('zLDAPSlaves', [],          'lines'),
        ]

These properties are all unique; they are not the same as those shipped with the
ZenPacks.zenoss.LDAPMonitor ZenPack.

zLDAPSlaves is used to denote slaves of an LDAP master.  It is used to check that
the contextCSN is the same between master and slaves, as a replication check.  The 
LDAP parameters for master and slaves must be the same.

A new LDAP datasource called "Ldap Protocol" is introduced.  It utilises the new
zProperties and runs an LDAP query with "cn=monitor".  The datasource from the standard
ZenPacks.zenoss.LDAPMonitor has a type of LDAPMonitor.

A new Zenoss daemon, zenldap, is provided to gather LDAP information using the
"Ldap Protocol" data source type.  It uses monparsers.py to parse the LDAP data into
data points.  monparsers uses configuration data from config.py in the base directory. 

The damon runs every 5 minutes by default.
zenldap uses the Python ldap modules to communicate with LDAP devices - python ldap
is a prerequisite for this ZenPack.

Under the services directory, LdapConfigService.py  configures a collector instance for
the zenldap collector daemon. The collection service filters devices so it will only
collect from devices with a template with a datasource whose sourcetype is "Ldap Protocol".
You can run the LdapConfigService.py standalone to see which devices will be included in
the remit of the zenldap daemon. Change to the ZenPack's services directory and run
"python LdapConfigService.py"; you can add a --device=<device name> to query for a specific
device.

The event /Status/LDAPMonitor is provided as an object of the ZenPack.

A sample LDAP Protocol monitoring template is provided called 
LDAPMonitor (the standard template provided with ZenPacks.zenoss.LDAPMonitor is
called LDAPServer). The BasicLdap datasource gathers about 30 attributes using
a cn=monitor LDAP query.  The ldapRelCheck datasource is a command datasource that
runs the ldap_rel_check.py script in the ZenPack's libexec directory, to
determine whether replication is working.




General Comments
----------------

Download
========
Download the appropriate package for your Zenoss version from the list
below.

* Zenoss 4.0+ `Latest Package for Python 2.7`_

ZenPack installation
======================

This ZenPack can be installed from the .egg file using either the GUI or the
zenpack command line. 

zenpack --install ZenPacks.skills1st.LDAPMonitoring-1.0.0-py2.7.egg

Alternatively, download the tar bundle from github and
install in development mode.

zenpack --link --install ZenPacks.skills1st.LDAPMonitoring

Restart zenoss completely after installation.



Change History
==============
* 1.0
   * Initial Release

Screenshots
===========

.. External References Below. Nothing Below This Line Should Be Rendered

.. _Latest Package for Python 2.7: https://github.com/jcurry/ZenPacks.skills1st.LDAPMonitoring/blob/master/dist/ZenPacks.skills1st.LDAPMonitoring-1.0.0-py2.7.egg?raw=true



Acknowledgements
================
Thanks to Alan Milligan for an excellent starting point.

