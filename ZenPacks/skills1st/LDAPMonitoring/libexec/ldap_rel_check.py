#!/usr/bin/env python
# Author:       Jane Curry
# Date:         December 3rd 2013
# Description:  Checks the contextCSN on an ldap master, gets the slaves from the master's
#                zLDAPSlaves zProperty (which is a list), and then runs the same query against
#                         the slave.  If both are the same, then replication is working
#                         LDAP parameters for the slave must be the same as the master.
#               Requires parameters:
#                       -N ${device/zLDAPDN} 
#                       -W ${device/zLDAPPW} 
#                       -P ${device/zLDAPProto} 
#                       -D ${device/id} 
#                       -S ${device/zLDAPSlaves}
#   eg. /usr/bin/ldapsearch -x  -LLL -D ${device/zLDAPDN}  -w ${device/zLDAPPW} -H ${device/zLDAPProto}://${device/id}/  -b 'dc=mserv,dc=local' -s base 'contextCSN'
#

from subprocess import Popen,PIPE
from optparse import OptionParser
import sys

# Nagios return codes
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
#

def get_cli_options():
    """Get command line options. Return them in a usable form."""

    parser = OptionParser()

    parser.add_option(
        '-D', '--device',
        dest='device', 
        help='ldap master device to send ldap query')

    parser.add_option(
        '-N', '--dn',
        dest='dn', default='""',
        help='Distinguished Name')

    parser.add_option(
        '-W', '--pwd',
        dest='pwd', default='""',
        help='Password for DN')

    parser.add_option(
        '-P', '--proto',
        dest='proto', default='ldap',
        help='LDAP protocol (ldap or ldaps)')

    parser.add_option(
        '-S', '--slaves',
        dest='slaves', default=[],
        help='ldap slaves list for this master eg [\'s1\', \'s2\']')

    options, args = parser.parse_args()

    return options

def main():
    options = get_cli_options()

    if not options.device:
        print 'Incorrect parameters supplied, please use --help for usage'
        return
    dn = options.dn
    if not options.dn:
        dn = '""'
    pwd = options.pwd
    if not options.pwd:
        pwd = '""'
    device = options.device
    #print 'DN is %s pwd is %s proto is %s device is %s slaves is %s' % ( dn, pwd, options.proto, device, options.slaves)

    cmd = '/usr/bin/ldapsearch -x  -LLL -D '+ dn +' -w '+ pwd +' -H '+options.proto + '://' + device + ' -b \'dc=mserv,dc=local\' -s base \'contextCSN\' | grep contextCSN'

    #cmd = '/usr/bin/ldapsearch -x  -LLL -D '+ dn +' -w '+ pwd +' -H '+options.proto + '://' + device + ' -b \'cn=monitor\' -s base \'contextCSN\' '

    #print 'cmd is %s ' % (cmd)
    p = Popen(cmd, shell=True, stdout=PIPE,stderr=PIPE)
    masterCSN=[]
    for r in p.stdout.readlines():
        masterCSN.append(r)
    if not masterCSN:
        print 'No master CSN found for master %s' % (device)
        sys.exit(STATE_WARNING)

    if options.slaves != '[]':
        # If slaves exists it will arrive as a string representing a list of strings
        #  eg. "['s1', 's2']"

        for s in eval(options.slaves):
            cmd = '/usr/bin/ldapsearch -x  -LLL -D '+ dn +' -w '+ pwd +' -H '+options.proto + '://' + s + ' -b \'dc=mserv,dc=local\' -s base \'contextCSN\' | grep contextCSN'
            #cmd = '/usr/bin/ldapsearch -x  -LLL -D '+ dn+ ' -w '+ pwd +' -H '+options.proto + '://' + s + ' -b \'cn=monitor\' -s base \'contextCSN\' '
            p = Popen(cmd, shell=True, stdout=PIPE,stderr=PIPE)
            slaveCSN=[]
            for r in p.stdout.readlines():
                slaveCSN.append(r)
            if slaveCSN != masterCSN:
                print 'Slave %s CSN different from master %s. Master CSN is %s. Slave CSN is %s ' % (s, device, masterCSN, slaveCSN)
                sys.exit(STATE_WARNING)
            else:
                print 'Slave %s CSN same as  master %s. CSN is %s.  ' % (s, device, masterCSN)
                sys.exit(STATE_OK)


# if we're being called as a stand-alone script. Not imported.
if __name__ == "__main__":
    main()


