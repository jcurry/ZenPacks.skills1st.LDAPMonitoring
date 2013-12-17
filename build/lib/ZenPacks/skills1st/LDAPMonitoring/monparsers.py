#
# Copyright 2012 Corporation of Balclutha (http://www.balclutha.org)
# 
#                All Rights Reserved
# 
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
#
#
# Corporation of Balclutha DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS, IN NO EVENT SHALL Corporation of Balclutha BE LIABLE FOR
# ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE. 
#
from config import MONITORED
import logging
log = logging.getLogger('zen.zenldap')


KEYS = map(lambda x:x[0], MONITORED)

def _dn(dn, results):
    """ fetch the attribute hash corresponding to the dn """
    r = filter(lambda x: x[0].lower() == dn, results)
    if r:
        return r[0][1]
    raise KeyError, '%s: %s' % (dn, map(lambda x: x[0], results))

def _isFDS(base):
    """ is this a Fedora Directory Server... """
    return base.get('version',[''])[0].startswith('389')
    
def _FDS(ldapresults, results={}):
    """
    Fedora Directory Server (389-ds)
    """
    snmp = _dn('cn=snmp,cn=monitor', ldapresults)
    for k in KEYS:
        results[k] = snmp[k][0]

def _isOpenLDAP(base):
    """ is this an OpenLDAP server ..."""
    return base.get('monitoredInfo',[''])[0].startswith('OpenLDAP')

def _OpenLDAP(ldapresults, results={}):
    """
    OpenLDAP mappings
    """
    results['connectionstotal'] = _dn('cn=total,cn=connections,cn=monitor', ldapresults).get('monitorCounter', [0])[0]
    results['connectionscurrent'] = _dn('cn=current,cn=connections,cn=monitor', ldapresults).get('monitorCounter', [0])[0]
    results['bytes'] = _dn('cn=bytes,cn=statistics,cn=monitor', ldapresults).get('monitorCounter', [0])[0]
    results['entries'] = _dn('cn=entries,cn=statistics,cn=monitor', ldapresults).get('monitorCounter', [0])[0]
    results['threadsMax'] = _dn('cn=max,cn=threads,cn=monitor', ldapresults).get('monitoredInfo', [0])[0]
    results['threadsMaxPending'] = _dn('cn=max pending,cn=threads,cn=monitor', ldapresults).get('monitoredInfo', [0])[0]
    results['threadsOpen'] = _dn('cn=open,cn=threads,cn=monitor', ldapresults).get('monitoredInfo', [0])[0]
    results['threadsStarting'] = _dn('cn=starting,cn=threads,cn=monitor', ldapresults).get('monitoredInfo', [0])[0]
    results['threadsActive'] = _dn('cn=active,cn=threads,cn=monitor', ldapresults).get('monitoredInfo', [0])[0]
    results['threadsPending'] = _dn('cn=pending,cn=threads,cn=monitor', ldapresults).get('monitoredInfo', [0])[0]
    results['threadsBackload'] = _dn('cn=backload,cn=threads,cn=monitor', ldapresults).get('monitoredInfo', [0])[0]
    results['threadsState'] = _dn('cn=state,cn=threads,cn=monitor', ldapresults).get('monitoredInfo', [0])[0]

    results['opsInitiated'] = _dn('cn=operations,cn=monitor', ldapresults).get('monitorOpInitiated', [0])[0]
    results['opsCompleted'] = _dn('cn=operations,cn=monitor', ldapresults).get('monitorOpCompleted', [0])[0]
    results['addopsInitiated'] = _dn('cn=add,cn=operations,cn=monitor', ldapresults).get('monitorOpInitiated', [0])[0]
    results['addopsCompleted'] = _dn('cn=add,cn=operations,cn=monitor', ldapresults).get('monitorOpCompleted', [0])[0]
    results['compareopsInitiated'] = _dn('cn=compare,cn=operations,cn=monitor', ldapresults).get('monitorOpInitiated', [0])[0]
    results['compareopsCompleted'] = _dn('cn=compare,cn=operations,cn=monitor', ldapresults).get('monitorOpCompleted', [0])[0]
    results['modifyopsInitiated'] = _dn('cn=modify,cn=operations,cn=monitor', ldapresults).get('monitorOpInitiated', [0])[0]
    results['modifyopsCompleted'] = _dn('cn=modify,cn=operations,cn=monitor', ldapresults).get('monitorOpCompleted', [0])[0]
    results['modrdnopsInitiated'] = _dn('cn=modrdn,cn=operations,cn=monitor', ldapresults).get('monitorOpInitiated', [0])[0]
    results['modrdnopsCompleted'] = _dn('cn=modrdn,cn=operations,cn=monitor', ldapresults).get('monitorOpCompleted', [0])[0]
    results['deleteopsInitiated'] = _dn('cn=delete,cn=operations,cn=monitor', ldapresults).get('monitorOpInitiated', [0])[0]
    results['deleteopsCompleted'] = _dn('cn=delete,cn=operations,cn=monitor', ldapresults).get('monitorOpCompleted', [0])[0]
    results['searchopsInitiated'] = _dn('cn=search,cn=operations,cn=monitor', ldapresults).get('monitorOpInitiated', [0])[0]
    results['searchopsCompleted'] = _dn('cn=search,cn=operations,cn=monitor', ldapresults).get('monitorOpCompleted', [0])[0]
    results['abandonopsInitiated'] = _dn('cn=abandon,cn=operations,cn=monitor', ldapresults).get('monitorOpInitiated', [0])[0]
    results['abandonopsCompleted'] = _dn('cn=abandon,cn=operations,cn=monitor', ldapresults).get('monitorOpCompleted', [0])[0]
    results['extendedopsInitiated'] = _dn('cn=extended,cn=operations,cn=monitor', ldapresults).get('monitorOpInitiated', [0])[0]
    results['extendedopsCompleted'] = _dn('cn=extended,cn=operations,cn=monitor', ldapresults).get('monitorOpCompleted', [0])[0]

    results['bindopsInitiated'] = _dn('cn=bind,cn=operations,cn=monitor', ldapresults).get('monitorOpInitiated', [0])[0]
    results['bindopsCompleted'] = _dn('cn=bind,cn=operations,cn=monitor', ldapresults).get('monitorOpCompleted', [0])[0]
    results['unbindopsInitiated'] = _dn('cn=unbind,cn=operations,cn=monitor', ldapresults).get('monitorOpInitiated', [0])[0]
    results['unbindopsCompleted'] = _dn('cn=unbind,cn=operations,cn=monitor', ldapresults).get('monitorOpCompleted', [0])[0]


def parse(ldapresults, results):
    """
    parse ldap.search_s result tuples and assign into a hash, keyed upon our
    datapoint names
    """
    base = _dn('cn=monitor', ldapresults)
    log.debug('In parse - base is %s \n' % (base))
    
    if _isFDS(base):
        _FDS(ldapresults, results)
    elif _isOpenLDAP(base):
        log.debug('In monparser open LDAP selected. ldapresults is %s \n' % (ldapresults))
        _OpenLDAP(ldapresults, results)
    else:
        raise NotImplementedError, 'No parser for %s' % ldapresults
    return results
