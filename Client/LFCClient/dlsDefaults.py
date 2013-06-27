#
# $Id: dlsDefaults.py,v 1.6 2010/12/03 10:21:19 delgadop Exp $
#
# DLS Client Defaults. $Name: DLS_1_1_3 $.
# Antonio Delgado Peris. CIEMAT. CMS.
#

"""
 This module simply defines some DLS default values as constants, so that
 other modules can use them. Editing this file directly will have the same
 effect as modifying a configuration file. The runtime value for some of 
 the variables here may be modified by other means (such as API calls or 
 CLI options), for others may be not. In any case, the values here define 
 what the defaults are.
"""

DLS_PHEDEX_MAX_BLOCKS_PER_QUERY = 100
DLS_PHEDEX_MAX_BLOCKS_PER_FILE_QUERY = 50
DLS_PHEDEX_MAX_SES_PER_QUERY = 10

DLS_API_VERSION = "DLS_1_1_3"

def getApiVersion():

    # DLS Client Api version, set from the CVS checkout tag
    # For HEAD version (len < 2), use above default
    version = "$Name: DLS_1_1_3 $"
    version = version[7:-2]
    if len(version) < 2:
         version = DLS_API_VERSION

    return version
