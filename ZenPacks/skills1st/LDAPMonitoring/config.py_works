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
               ('opsInitiated', 'DERIVE'),
               ('opsCompleted', 'DERIVE'),
               ('addopsInitiated', 'DERIVE'),
               ('addopsCompleted', 'DERIVE'),
               ('compareopsInitiated', 'DERIVE'),
               ('compareopsCompleted', 'DERIVE'),
               ('modifyopsInitiated', 'DERIVE'),
               ('modifyopsCompleted', 'DERIVE'),
               ('modrdnopsInitiated', 'DERIVE'),
               ('modrdnopsCompleted', 'DERIVE'),
               ('deleteopsInitiated', 'DERIVE'),
               ('deleteopsCompleted', 'DERIVE'),
               ('searchopsInitiated', 'DERIVE'),
               ('searchopsCompleted', 'DERIVE'),
               ('abandonopsInitiated', 'DERIVE'),
               ('abandonopsCompleted', 'DERIVE'),
               ('extendedopsInitiated', 'DERIVE'),
               ('extendedopsCompleted', 'DERIVE'),
               ('connectionstotal', 'DERIVE'),
               ('connectionscurrent', 'GAUGE'),
               ('bytes', 'DERIVE'),
               ('entries', 'DERIVE'),
               ('bindopsInitiated', 'DERIVE'),
               ('bindopsCompleted', 'DERIVE'),
               ('unbindopsInitiated', 'DERIVE'),
               ('unbindopsCompleted', 'DERIVE'),
               ('threadsMax', 'GAUGE'),
               ('threadsMaxPending', 'GAUGE'),
               ('threadsOpen', 'GAUGE'),
               ('threadsStarting', 'GAUGE'),
               ('threadsActive', 'GAUGE'),
               ('threadsPending', 'GAUGE'),
               ('threadsBackload', 'GAUGE'),
               ('responsetime', 'GAUGE'),
                )

BINDDP = (('bindopsInitiated', 'Binds Initiated'),
          ('bindopsCompleted', 'Binds Completed'),
          ('unbindopsInitiated', 'Unbinds Initiated'),
          ('unbindopsCompleted', 'Unbinds Completed')
          )

THREADDP = (('threadsMax', 'Threads Max'),
          ('threadsMaxPending', 'Threads Max Pending'),
          ('threadsOpen', 'Threads Open'),
          ('threadsStarting', 'Threads Starting'),
          ('threadsActive', 'Threads Active'),
          ('threadsPending', 'Threads Pending'),
          ('threadsBackload', 'Threads Backload')
          )

OPSDP = (
         ('opsInitiated', 'Total Operations Initiated'),
         ('opsCompleted', 'Total Operations Completed'),
         ('addopsInitiated', 'Add Operations Initiated'),
         ('addopsCompleted', 'Add Operations Completed'),
         ('compareopsCompleted', 'Compare Operations Completed'),
         ('compareopsCompleted', 'Compare Operations Completed'),
         ('modifyopsCompleted', 'Modify Operations Completed'),
         ('modifyopsCompleted', 'Modify Operations Completed'),
         ('modrdnopsCompleted', 'Modrdn Operations Completed'),
         ('modrdnopsCompleted', 'Modrdn Operations Completed'),
         ('deleteopsCompleted', 'Delete Operations Completed'),
         ('deleteopsCompleted', 'Delete Operations Completed'),
         ('searchopsCompleted', 'Search Operations Completed'),
         ('searchopsCompleted', 'Search Operations Completed'),
         ('abandonopsCompleted', 'Abandon Operations Completed'),
         ('abandonopsCompleted', 'Abandon Operations Completed'),
         ('extendedopsCompleted', 'Extended Operations Completed'),
         ('extendedopsCompleted', 'Extended Operations Completed'),
         ('connectionstotal', 'Total Connections'),
         ('connectionscurrent', 'Current Connections'),
         ('bytes', 'Bytes'),
         ('entries', 'Entries'),
         )


MONITORED = BINDDP + OPSDP + THREADDP
