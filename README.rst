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
It uses zProperties introduced by the ZenPack to authenticate to an LDAP server.
It check LDAP replication by checking contextCSN records and by comparing full
LDAP subtree searches.

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
        ('zLDAPRepContext',    'dc=example,dc=org',     'string'),
        ('zLDAPSlaves', [],          'lines'),
        ]

These properties are all unique; they are not the same as those shipped with the
ZenPacks.zenoss.LDAPMonitor ZenPack.

zLDAPSlaves is used to denote slaves of an LDAP master (it is a Python list).  
It is used to perform replication checks between master and slave(s). 
The LDAP parameters for master and slaves MUST be the same.

zLDAPRepContext is used to specify parameters for a full check of the replication
between master and slave(s).

A new LDAP datasource called "Ldap Protocol" is introduced.  It utilises the new
zProperties and runs an LDAP query with "cn=monitor".  The datasource from the standard
ZenPacks.zenoss.LDAPMonitor has a type of LDAPMonitor. The datasource has a large
number of datapoints associated with it which are defined in the config.py file in 
the ZenPack's base directory.

A new Zenoss daemon, zenldap, is provided to gather LDAP information using the
"Ldap Protocol" data source type.  It uses monparsers.py in the ZenPack base directory, 
to parse the LDAP data into data points.  monparsers.py uses configuration data 
from config.py in the base directory. 

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

The ZenPack provides new, unique events as part of the ZenPack:

* /Status/LDAPMonitor
   * /Status/LDAPMonitor/ResponseTime
   * /Status/LDAPMonitor/Replication_CSN
   * /Status/LDAPMonitor/Replication_Files

The repllication events are NOT self-clearing.  To prevent self-clearing, each event
has the following transform to change the clearing fingerprint and set severity to Info:


# Need to prevent automatic clearing mechanism for these events

# Auto-clearing based on device, component and event class

if evt.severity == 0:                      # Good news, clearing event
  evt.component = evt.component + 'GoodNews'
    evt.severity = 2



A sample LDAP Protocol monitoring template is provided called 
LDAPMonitor (the standard template provided with ZenPacks.zenoss.LDAPMonitor is
called LDAPServer). The BasicLdap datasource gathers the MONITORABLE datapoints defined in config.py,  
using a cn=monitor LDAP query.  

Two further COMMAND datasources are included in the LDAPMonitor template, one to
check replication by comparing the CSN; the second compares the complete subtree
specified by the zLDAPRepContext zProperty.  Both are driven by scripts under the
ZenPack's libexec directory.

* ldap_rel_check.py
   * Uses the /usr/bin/ldapsearch command to get the context CSN
* ldap_rel_check_files_pythonldap.py
   * Uses the python ldap library to gather the full subtrees from master and slave(s)


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

zenpack --install ZenPacks.skills1st.LDAPMonitoring-1.0.1-py2.7.egg

Alternatively, download the tar bundle from github and
install in development mode.

zenpack --link --install ZenPacks.skills1st.LDAPMonitoring

Restart zenoss completely after installation.



Change History
==============
* 1.0
   * Initial Release
* 1.0.1
   * ldap_rel_check_files_pythonldap.py to check full replication

Screenshots
===========

.. External References Below. Nothing Below This Line Should Be Rendered

.. _Latest Package for Python 2.7: https://github.com/jcurry/ZenPacks.skills1st.LDAPMonitoring/blob/master/dist/ZenPacks.skills1st.LDAPMonitoring-1.0.1-py2.7.egg?raw=true



Acknowledgements
================
Thanks to Alan Milligan for an excellent starting point.

