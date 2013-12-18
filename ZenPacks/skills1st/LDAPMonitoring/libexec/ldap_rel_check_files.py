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

import subprocess
#from subprocess import Popen,PIPE,call
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

    url=options.proto +  '://' + device
    #print ' dn is %s and pwd is %s \n' % (dn,pwd)
    # Blank strings actually come through as "" - need to make them really the null string
    if dn == '""':
        dn = ''
    if pwd == '""':
        pwd=''
    
    cmd = ["/usr/bin/ldapsearch", "-x", "-o", "nettimeout=10", "-LLL", "-D", dn, "-w", pwd, "-H", url, "-b", "dc=mserv,dc=local", "-S", "dn", "-s",  "sub", "*", "+" ]
    #cmd = ["/usr/bin/ldapsearch", "-x", "-o", "nettimeout=10", "-LLL", "-D", dn, "-w", pwd, "-H", url, "-b", "cn=monitor", "-S",  "dn" ]

    # Create output  file for master
    masterFile='/tmp/' + device + '_ldapMaster.out'
    master_out = open(masterFile, 'w')

    #print 'cmd is %s ' % (cmd)
    p = subprocess.call(cmd, shell=False, stdout=master_out,stderr=master_out)
    #master_out.flush()
    #os.fsync(master_out.fileno())
    master_out.close()

    # Now check slaves and compare with master file
    if options.slaves != '[]':
        # If slaves exists it will arrive as a string representing a list of strings
        #  eg. "['s1', 's2']"

        for s in eval(options.slaves):
            url=options.proto +  '://' + s
            cmd = ["/usr/bin/ldapsearch", "-x", "-o", "nettimeout=10", "-LLL", "-D", dn, "-w", pwd, "-H", url, "-b", "dc=mserv,dc=local", "-S", "dn", "-s",  "sub", "*", "+" ]
            #cmd = ["/usr/bin/ldapsearch", "-x", "-o", "nettimeout=10", "-LLL", "-D", dn, "-w", pwd, "-H", url, "-b", "cn=monitor", "-S",  "dn"]
            slaveFile = '/tmp/' + s + '_ldapSlave.out'
            slave_out = open(slaveFile, 'w')
            #print 'cmd is %s ' % (cmd)
            p = subprocess.call(cmd, shell=False, stdout=slave_out,stderr=slave_out)
            #slave_out.flush()
            #os.fsync(slave_out.fileno())
            slave_out.close()

            master_out = open(masterFile).readlines()
            slave_out = open(slaveFile).readlines()

            len_diff = len(master_out) - len(slave_out)
            if len_diff != 0:
                try:
                    master_out.close()
                    slave_out.close()
                except:
                    pass
                print 'LDAP content of  %s is different to %s - different length' % (device, s)
                sys.exit(STATE_WARNING)

            for m, sl in zip(master_out, slave_out):
                if m != sl:
                    try:
                        master_out.close()
                        slave_out.close()
                    except:
                        pass
                    print 'LDAP content of  %s is different to %s ' % (device, s)
                    #print "Master and slave files differ. Expected %r; got %r." % (m, s)
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


