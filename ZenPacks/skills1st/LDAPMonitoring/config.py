#
# Copyright 2012 Corporation of Balclutha (http://www.balclutha.org)
# 
#                All Rights Reserved
# 
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
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


MONITORABLE =  (
               ('addentryops', 'DERIVE'),
               ('anonymousbinds', 'DERIVE'),
               ('bindsecurityerrors', 'DERIVE'),
               ('bytesrecv', 'DERIVE'),
               ('bytessent', 'DERIVE'),
               ('cacheentries', 'DERIVE'),
               ('cachehits', 'DERIVE'),
               ('chainings', 'DERIVE'),
               ('compareops', 'DERIVE'),
               ('connections', 'DERIVE'),
               ('connectionseq', 'DERIVE'),
               ('copyentries', 'DERIVE'),
               ('entriesreturned', 'DERIVE'),
               ('errors', 'DERIVE'),
               ('inops', 'DERIVE'),
               ('listops', 'DERIVE'),
               ('masterentries', 'DERIVE'),
               ('modifyentryops', 'DERIVE'),
               ('modifyrdnops', 'DERIVE'),
               ('onelevelsearchops', 'DERIVE'),
               ('readops', 'DERIVE'),
               ('referrals', 'DERIVE'),
               ('referralsreturned', 'DERIVE'),
               ('removeentryops', 'DERIVE'),
               ('searchops', 'DERIVE'),
               ('securityerrors', 'DERIVE'),
               ('simpleauthbinds', 'DERIVE'),
               ('slavehits', 'DERIVE'),
               ('strongauthbinds', 'DERIVE'),
               ('unauthbinds', 'DERIVE'),
               ('wholetreesearchops', 'DERIVE'),
               ('responsetime', 'GAUGE'),
                )
ERRORDP = (
           ('bindsecurityerrors', 'Bind Security'),
           ('securityerrors', 'Security'),
           ('errors', 'Total Errors'))

BINDDP = (('anonymousbinds', 'Anonymous'),
          ('simpleauthbinds', 'Simple Auth'),
          ('strongauthbinds', 'Strong Auth'),
          ('unauthbinds', 'Unauth'))

# wtf - no failures!!
FAILDP = (('failures', 'Failures'),)

OPSDP = (('addentryops', 'Add Entry'),
         ('modifyentryops', 'Mod Entry'),
         ('removeentryops', 'Del Entry'),
         ('searchops', 'Search'),
         ('referrals', 'Referrals'),
         ('chainings', 'Chainings'))

CACHEDP = (('cacheentries', 'Cache Entries'),
           ('cachehits', 'Cache Hits'),
           ('slavehits', 'Slave Hits'),
           ('masterentries', 'Master Entries'))

MONITORED = ERRORDP + BINDDP + OPSDP + CACHEDP
