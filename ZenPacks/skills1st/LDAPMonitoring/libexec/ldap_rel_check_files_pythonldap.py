#!/usr/bin/env python
# Author:       Jane Curry
# Date:         December 17th 2013
# Description:  Checks the full query of cn=monitor on master and slave(s) using python ldap library.
#               If identical then replication is good.
#                zLDAPSlaves zProperty (which is a list)used to get slaves.
#               LDAP parameters for the slave must be the same as the master.
#               Requires parameters:
#                       -N ${device/zLDAPDN} 
#                       -W ${device/zLDAPPW} 
#                       -P ${device/zLDAPProto} 
#                       -T ${device/zLDAPPort} 
#                       -R ${device/zLDAPRepContext} 
#                       -D ${device/id} 
#                       -S ${device/zLDAPSlaves}
#

import ldap
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
        dest='dn', default='',
        help='Distinguished Name')

    parser.add_option(
        '-W', '--pwd',
        dest='pwd', default='',
        help='Password for DN')

    parser.add_option(
        '-P', '--proto',
        dest='proto', default='ldap',
        help='LDAP protocol (ldap or ldaps)')

    parser.add_option(
        '-T', '--port',
        dest='port', default='389',
        help='LDAP Port - default is 389')

    parser.add_option(
        '-R', '--rep',
        dest='rep', default='dc=example,dc=org',
        help='LDAP replication Context string')

    parser.add_option(
        '-S', '--slaves',
        dest='slaves', default=[],
        help='ldap slaves list for this master eg [\'s1\', \'s2\']')

    options, args = parser.parse_args()

    return options

def getLdap(url, credentials, rep):
    ''' Use Python ldap library to initialise and bind to LDAP server and to get data'''

    resultseq=[]
    slapd = ldap.initialize(url)
    try:
        slapd.simple_bind_s(*credentials)
    except ldap.INVALID_CREDENTIALS:
        print  'Authentication failure: %s/%s: check credentials!' % (url, credentials[0])
    except ldap.SERVER_DOWN:
        print  'LDAP server uncontactable when performing replication file checks '
    except ldap.LDAPError, e:
        print  'LDAP server request failed when performing bind for replication file checks. error code is %s ' % (e)

    try:
        # Use synchronous search method with 30s timeout
        resultseq = slapd.search_st(rep, ldap.SCOPE_SUBTREE, attrlist=['*', '+'], timeout=30)
        #resultseq = slapd.search_st(rep, ldap.SCOPE_BASE, attrlist=['*', '+'], timeout=30)
    except ldap.TIMEOUT:
        print  'LDAP search failure - timeout requesting %s from %s ' % (rep, url)
    except Exception, e:
        print  'LDAP search failure requesting %s from %s error code is %s' % (rep, url, e)

    slapd.unbind()
    return resultseq

def main():
    options = get_cli_options()

    if not options.device:
        print 'Incorrect parameters supplied, please use --help for usage'
        return
    device = options.device
    rep = options.rep
    credentials = options.dn,options.pwd
    url=options.proto +  '://' + device + ':' + options.port


    masterResultseq = getLdap(url, credentials, rep)

    #print 'masterResultseq is %s \n' % (masterResultseq)
    if not masterResultseq:
        sys.exit(STATE_WARNING)
    masterResultseqSort = sorted(masterResultseq)
    
    # Now check slaves and compare with master file
    if options.slaves != '[]':
        # If slaves exists it will arrive as a string representing a list of strings
        #  eg. "['s1', 's2']"

        for s in eval(options.slaves):
            url=options.proto +  '://' + s + ':' + options.port
            slaveResultseq = getLdap(url, credentials, rep)

            #print 'slaveResultseq is %s \n' % (slaveResultseq)

            if not slaveResultseq:
                sys.exit(STATE_WARNING)

            if len(masterResultseq) != len(slaveResultseq):
                print 'LDAP content of  %s is different to %s - different length' % (device, s)
                sys.exit(STATE_WARNING)

            slaveResultseqSort = sorted(s)
            # Check all entries match
            for m, s in zip(masterResultseqSort, slaveResultseqSort):
                #print 'm is %s and s is %s \n' % (m, s)
                #print 'm0 is %s and s0 is %s \n' % (m[0], s[0])
                #print 'm1 is %s and s1 is %s \n' % (m[1], s[1])
                if m[0] == s[0]:        # dn keys are the same
                    for mk, mv in m[1].iteritems():               #get key, value
                        entryMatch = False
                        for sk, sv in s[1].iteritems():
                            if mk != sk:            # different keys
                                continue
                            else:
                                if sorted(mv) != sorted(sv):        # key, value dont match
                                #if mv != sv:        # key, value dont match - this proves that the sorted works
                                    print 'key %s  master value %s slave value %s pairs dont match \n' % (mk, mv, sv)
                                    sys.exit(STATE_WARNING)
                                else:
                                    entryMatch = True
                                    break
                        if not entryMatch:
                            print 'No slave key matching master key %s \n' % (mk)
                            sys.exit(STATE_WARNING)

                    # If we get here then we have successfully checked all key,value dictionary entries for this dn 
                # dn keys not the same - must be a non-match
                else:
                    print 'dn keys dont match for master %s and slave %s \n' % (m[0], s[0])
                    sys.exit(STATE_WARNING)

            # If we get here then all entries for all dn's match
            print 'Master and slave files are identical - for slaveResultseq %s \n' % (slaveResultseqSort)
        sys.exit(STATE_OK)


# if we're being called as a stand-alone script. Not imported.
if __name__ == "__main__":
    main()


