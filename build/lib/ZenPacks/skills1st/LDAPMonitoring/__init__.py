# Nothing is required in this __init__.py, but it is an excellent place to do
# many things in a ZenPack.
#
# The example below which is commented out by default creates a custom subclass
# of the ZenPack class. This allows you to define custom installation and
# removal routines for your ZenPack. If you don't need this kind of flexibility
# you should leave the section commented out and let the standard ZenPack
# class be used.
#

import Globals

from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenUtils.Utils import unused

unused(Globals)
#
#
class ZenPack(ZenPackBase):
    """ Zenoss config properties 
      All zProperties defined here will automatically be created when the
      ZenPack is installed.
    """

    packZProperties = [
        ('zLDAPProto', 'ldap',       'string'),
        ('zLDAPPort',  '389',          'string'),
        ('zLDAPDN',    'cn=Manager', 'string'),
        ('zLDAPPW',    'secret',     'password'),
        ]


#     def install(self, dmd):
#         ZenPackBase.install(self, dmd)
#
#         # Put your customer installation logic here.
#         pass
#
#     def remove(self, dmd, leaveObjects=False):
#         if not leaveObjects:
#             # When a ZenPack is removed the remove method will be called with
#             # leaveObjects set to False. This means that you likely want to
#             # make sure that leaveObjects is set to false before executing
#             # your custom removal code.
#             pass
#
#         ZenPackBase.remove(self, dmd, leaveObjects=leaveObjects)
