#!/usr/bin/env python
# Author:       Jane Curry
# Date:         December 17th 2013
# Description:  Checks the full query of cn=monitor and outputs to a file
#               Files generated on master and slave(s) and are then compared.
#               If identical then replication is good.
#                zLDAPSlaves zProperty (which is a list)used to get slaves.
#               LDAP parameters for the slave must be the same as the master.
#               Requires parameters:
#                       -N ${device/zLDAPDN} 
#                       -W ${device/zLDAPPW} 
#                       -P ${device/zLDAPProto} 
#                       -D ${device/id} 
#                       -S ${device/zLDAPSlaves}
#   eg. /usr/bin/ldapsearch -x  -LLL -D ${device/zLDAPDN}  -w ${device/zLDAPPW} -H ${device/zLDAPProto}://${device/id}/  -b 'cn=monitor' -s sub '*' '+'
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

    exitCode = STATE_OK

    cmd = '/usr/bin/ldapsearch -x  -LLL -D '+ dn +' -w '+ pwd +' -H '+options.proto + '://' + device + ' -b \'cn=monitor\' -s sub \'*\' \'+\' '

    # Create output  file for master
    master_out = open('/tmp/master.out', 'w')

    print 'cmd is %s ' % (cmd)
    p = Popen(cmd, shell=True, stdout=master_out,stderr=master_out)
    master_out.close()

    # Now check slaves and compare with master file
    if options.slaves != '[]':
        # If slaves exists it will arrive as a string representing a list of strings
        #  eg. "['s1', 's2']"

        for s in eval(options.slaves):
            cmd = '/usr/bin/ldapsearch -x  -LLL -D '+ dn +' -w '+ pwd +' -H '+options.proto + '://' + s + ' -b \'cn=monitor\' -s sub \'*\' \'+\' '
            slave_out = open('/tmp/slave.out', 'w')
            print 'cmd is %s ' % (cmd)
            p = Popen(cmd, shell=True, stdout=slave_out,stderr=slave_out)
            slave_out.close()

            master_out = open("/tmp/master.out").readlines()
            slave_out = open("/tmp/slave.out").readlines()

            print 'master is %s long and slave is %s long \n' % (len(master_out), len(slave_out))
            len_diff = len(master_out) - len(slave_out)
            if len_diff != 0:
                try:
                    master_out.close()
                    slave_out.close()
                except:
                    pass
                print "Master and Slave files are different length"
                sys.exit(STATE_WARNING)

            for m, s in zip(master_out, slave_out):
                print ' in for loop m is %s s is %s \n ' % (m,s)
                if m != s:
                    try:
                        master_out.close()
                        slave_out.close()
                    except:
                        pass
                    print "Master and slave files differ. Expected %r; got %r." % (m, s)
                    sys.exit(STATE_WARNING)

            # If we get here then we have checked all slaves and found no errors
            try:
                master_out.close()
                slave_out.close()
            except:
                pass

            print('Master and slave files are identical')
            sys.exit(STATE_OK)

# if we're being called as a stand-alone script. Not imported.
if __name__ == "__main__":
    main()


