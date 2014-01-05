#!/usr/bin/env python
# Author:       Jane Curry
# Date:         December 17th 2013
# Description:  

import sys

# Nagios return codes
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
#

def main():

    masterResultseq = [('dc=example,dc=org', {'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.500662Z#000000#000#000000'], 'description': ['Simple example'], 'objectClass': ['organization', 'dcObject'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'entryUUID': ['c4755e22-3c81-1032-81c9-77679238dd1b'], 'dc': ['example'], 'o': ['The Example Org'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'createTimestamp': ['20130418144115Z'], 'entryDN': ['dc=example,dc=org'], 'subschemaSubentry': ['cn=Subschema'], 'structuralObjectClass': ['organization'], 'modifyTimestamp': ['20130418144115Z']}), ('dc=people,dc=example,dc=org', {'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.515384Z#000000#000#000000'], 'objectClass': ['organizationalUnit', 'dcObject'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'entryUUID': ['c4779d22-3c81-1032-81ca-77679238dd1b'], 'dc': ['people'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'createTimestamp': ['20130418144115Z'], 'entryDN': ['dc=people,dc=example,dc=org'], 'subschemaSubentry': ['cn=Subschema'], 'structuralObjectClass': ['organizationalUnit'], 'ou': ['People'], 'modifyTimestamp': ['20130418144115Z']})]

    #print 'masterResultseq is %s \n' % (masterResultseq)
    if not masterResultseq:
        sys.exit(STATE_WARNING)
    masterResultseqSort = sorted(masterResultseq)
    #print 'masterResultseqSort is %s \n' % (masterResultseqSort)
    
    # dcs in different order
    slaveResultseq1 = [('dc=people,dc=example,dc=org', {'objectClass': ['organizationalUnit', 'dcObject'], 'entryUUID': ['c4779d22-3c81-1032-81ca-77679238dd1b'], 'dc': ['people'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'entryDN': ['dc=people,dc=example,dc=org'], 'subschemaSubentry': ['cn=Subschema'], 'structuralObjectClass': ['organizationalUnit'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.515384Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'createTimestamp': ['20130418144115Z'], 'ou': ['People']}), ('dc=example,dc=org', {'description': ['Simple example'], 'objectClass': ['organization', 'dcObject'], 'entryUUID': ['c4755e22-3c81-1032-81c9-77679238dd1b'], 'dc': ['example'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'structuralObjectClass': ['organization'], 'subschemaSubentry': ['cn=Subschema'], 'entryDN': ['dc=example,dc=org'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.500662Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'o': ['The Example Org'], 'createTimestamp': ['20130418144115Z']})] 

    #print 'slaveResultseq1 is %s \n' % (slaveResultseq1)
    if not slaveResultseq1:
        sys.exit(STATE_WARNING)
    
    # dict keys in different order - objectClass and entryUUID swapped
    # Matches in spite of objectClass and entryUUID swapped
    slaveResultseq2 = [('dc=people,dc=example,dc=org', {'entryUUID': ['c4779d22-3c81-1032-81ca-77679238dd1b'],'objectClass': ['organizationalUnit', 'dcObject'], 'dc': ['people'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'entryDN': ['dc=people,dc=example,dc=org'], 'subschemaSubentry': ['cn=Subschema'], 'structuralObjectClass': ['organizationalUnit'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.515384Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'createTimestamp': ['20130418144115Z'], 'ou': ['People']}), ('dc=example,dc=org', {'description': ['Simple example'], 'objectClass': ['organization', 'dcObject'], 'entryUUID': ['c4755e22-3c81-1032-81c9-77679238dd1b'], 'dc': ['example'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'structuralObjectClass': ['organization'], 'subschemaSubentry': ['cn=Subschema'], 'entryDN': ['dc=example,dc=org'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.500662Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'o': ['The Example Org'], 'createTimestamp': ['20130418144115Z']})] 

    # non-match in dn key
    #slaveResultseq2 = [('dc=peopleZZZ,dc=example,dc=org', {'entryUUID': ['c4779d22-3c81-1032-81ca-77679238dd1b'],'objectClass': ['organizationalUnit', 'dcObject'], 'dc': ['people'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'entryDN': ['dc=people,dc=example,dc=org'], 'subschemaSubentry': ['cn=Subschema'], 'structuralObjectClass': ['organizationalUnit'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.515384Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'createTimestamp': ['20130418144115Z'], 'ou': ['People']}), ('dc=example,dc=org', {'description': ['Simple example'], 'objectClass': ['organization', 'dcObject'], 'entryUUID': ['c4755e22-3c81-1032-81c9-77679238dd1b'], 'dc': ['example'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'structuralObjectClass': ['organization'], 'subschemaSubentry': ['cn=Subschema'], 'entryDN': ['dc=example,dc=org'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.500662Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'o': ['The Example Org'], 'createTimestamp': ['20130418144115Z']})] 

    # non-match in value of objectClass
    #slaveResultseq2 = [('dc=people,dc=example,dc=org', {'entryUUID': ['c4779d22-3c81-1032-81ca-77679238dd1b'],'objectClass': ['organizationalUnitZZZ', 'dcObject'], 'dc': ['people'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'entryDN': ['dc=people,dc=example,dc=org'], 'subschemaSubentry': ['cn=Subschema'], 'structuralObjectClass': ['organizationalUnit'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.515384Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'createTimestamp': ['20130418144115Z'], 'ou': ['People']}), ('dc=example,dc=org', {'description': ['Simple example'], 'objectClass': ['organization', 'dcObject'], 'entryUUID': ['c4755e22-3c81-1032-81c9-77679238dd1b'], 'dc': ['example'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'structuralObjectClass': ['organization'], 'subschemaSubentry': ['cn=Subschema'], 'entryDN': ['dc=example,dc=org'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.500662Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'o': ['The Example Org'], 'createTimestamp': ['20130418144115Z']})] 

    #print 'slaveResultseq2 is %s \n' % (slaveResultseq2)
    if not slaveResultseq2:
        sys.exit(STATE_WARNING)
    
    # dict keys in different order - objectClass and entryUUID swapped and objectClass value list has entries swapped
    slaveResultseq3 = [('dc=people,dc=example,dc=org', {'entryUUID': ['c4779d22-3c81-1032-81ca-77679238dd1b'],'objectClass': ['dcObject', 'organizationalUnit'], 'dc': ['people'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'entryDN': ['dc=people,dc=example,dc=org'], 'subschemaSubentry': ['cn=Subschema'], 'structuralObjectClass': ['organizationalUnit'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.515384Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'createTimestamp': ['20130418144115Z'], 'ou': ['People']}), ('dc=example,dc=org', {'description': ['Simple example'], 'objectClass': ['organization', 'dcObject'], 'entryUUID': ['c4755e22-3c81-1032-81c9-77679238dd1b'], 'dc': ['example'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'structuralObjectClass': ['organization'], 'subschemaSubentry': ['cn=Subschema'], 'entryDN': ['dc=example,dc=org'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.500662Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'o': ['The Example Org'], 'createTimestamp': ['20130418144115Z']})]

    #print 'slaveResultseq3 is %s \n' % (slaveResultseq3)
    if not slaveResultseq3:
        sys.exit(STATE_WARNING)
    
    # dict has different number of entries
    slaveResultseq4 = [('dc=people,dc=example,dc=org', {'entryUUID': ['c4779d22-3c81-1032-81ca-77679238dd1b'],'objectClass': ['dcObject', 'organizationalUnit'], 'dc': ['people'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'entryDN': ['dc=people,dc=example,dc=org'], 'subschemaSubentry': ['cn=Subschema'], 'structuralObjectClass': ['organizationalUnit'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.515384Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'createTimestamp': ['20130418144115Z'], 'ou': ['People']}), ('dc=example,dc=org', {'description': ['Simple example'], 'objectClass': ['organization', 'dcObject'], 'entryUUID': ['c4755e22-3c81-1032-81c9-77679238dd1b'], 'dc': ['example'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'structuralObjectClass': ['organization'], 'subschemaSubentry': ['cn=Subschema'], 'entryDN': ['dc=example,dc=org'], 'modifyTimestamp': ['20130418144115Z'], 'hasSubordinates': ['TRUE'], 'entryCSN': ['20130418144115.500662Z#000000#000#000000'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'o': ['The Example Org'], 'createTimestamp': ['20130418144115Z']}), ('uid=u1,dc=people,dc=example,dc=org', {'hasSubordinates': ['FALSE'], 'entryCSN': ['20130418144115.516423Z#000000#000#000000'], 'description': ['A User'], 'objectClass': ['account', 'simpleSecurityObject'], 'creatorsName': ['cn=root,dc=example,dc=org'], 'entryUUID': ['c477c5a4-3c81-1032-81cb-77679238dd1b'], 'modifiersName': ['cn=root,dc=example,dc=org'], 'createTimestamp': ['20130418144115Z'], 'entryDN': ['uid=u1,dc=people,dc=example,dc=org'], 'subschemaSubentry': ['cn=Subschema'], 'structuralObjectClass': ['account'], 'modifyTimestamp': ['20130418144115Z'], 'uid': ['u1']})]

    #print 'slaveResultseq4 is %s \n' % (slaveResultseq4)
    if not slaveResultseq4:
        sys.exit(STATE_WARNING)
    
    slaveResultseq5 = []
    print 'slaveResultseq5 is %s \n' % (slaveResultseq5)
    
    slaves = [ slaveResultseq1, slaveResultseq2, slaveResultseq3, slaveResultseq4, slaveResultseq5]
    #slaves = [ slaveResultseq1, slaveResultseq2, slaveResultseq3, slaveResultseq5]
    # Now check slaves and compare with master file
    if slaves != '[]':
        # If slaves exists it will arrive as a string representing a list of strings
        #  eg. "['s1', 's2']"
        for s in slaves:
            print 'slaveResultseq is %s \n' % (s)

            if not s:
                print 'No slaveResultsequence'
                sys.exit(STATE_WARNING)

            if len(masterResultseq) != len(s):
                print 'LDAP content different length'
                sys.exit(STATE_WARNING)

            slaveResultseqSort = sorted(s)
            #if masterResultseqSort != slaveResultseqSort:
                #print 'LDAP content of  master different from slave for slaveResultseq %s \n' % (slaveResultseqSort)
                #sys.exit(STATE_WARNING)
            for m, s in zip(masterResultseqSort, slaveResultseqSort):
                #print 'm is %s and s is %s \n' % (m, s)
                #print 'm0 is %s and s0 is %s \n' % (m[0], s[0])
                #print 'm1 is %s and s1 is %s \n' % (m[1], s[1])
                if m[0] == s[0]:        # dn keys are the same
                    #for m1, s1 in zip(m[1], s[1]):      # get dictionaries for matching dn
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


