#
# $Id: dlsApi.py,v 1.28 2009/09/21 13:05:39 delgadop Exp $
#
# DLS Client. $Name: DLS_1_1_3 $.
# Antonio Delgado Peris. CIEMAT. CMS.
#

"""
 This module defines the CMS Dataset Location Service (DLS) client interface.
 Python applications interacting with a given DLS catalog implementation will
 use methods defined in the DlsApi class, defined in this module.

 This class serves as an interface definition. It should not be instantiated
 directly, but all instantiable API implementations should provide the code
 for the methods listed here (they could be derived classes).

 This module also includes an API exception class, to propagate error
 conditions when interacting with the DLS catalog.
"""

#########################################
# Imports 
#########################################
from os import environ
from sys import stdout


#########################################
# Module globals
#########################################
DLS_VERB_NONE = 0    # print nothing
DLS_VERB_INFO = 5    # print info
DLS_VERB_WARN = 10   # print only warnings (to stdout)
DLS_VERB_HIGH = 20   # print warnings (stdout) and error messages (stderr)


#########################################
# DlsApiError class
#########################################

# Just get all the exceptions from the appropriate module
from dlsApiExceptions import *



#########################################
# DlsApi class
#########################################

class DlsApi(object):
  """
  This class serves as a DLS interface definition. It should not be instantiated
  directly, but all instantiable API implementations should provide the code
  for the methods listed here.
  
  Some DLS implementations may support hierarchy in the FileBlock namespace.
  Some others may have a flat FileBlock namespace. This should not affect use of
  the methods. Every method accepting FileBlock names as argument should require
  them in their complete form (that is including any subdirectories). 

  Unless specified, in the instantiable implementations, all methods that can raise
  an exception will raise one derived from DlsApiError, but further information
  should be provided by those implementations documentation.
  """

  def __init__(self, dls_endpoint = None, verbosity = DLS_VERB_WARN, **kwd):
    """
    This constructor is used as a general data members initialiser.
    But remember that this class should not be instantiated, since no method
    here is implemented!

    The variables set are the DLS server endpoint (optionally with a port
    number, otherwise a default is used) and the verbosity. For some
    implementations, also a path to the DLS root directory is required.
    Implementations not using this path should accept it and just ignore it.
 
    Notice that this method allows to have an empty DLS endpoint, but instantiable
    DLS API classes should not allow this. They should deny instantiation if no
    DLS endpoint can be retrieved from (in this order):
         - specified dls_endpoint
         - DLS_ENDPOINT environmental variable
         - DLS config file (for some implementations, check specific documentation)
         - DLS catalog advertised in the Information System (if implemented)
         - Possibly some default value (if defined in a given implementation)
  
    The DLS_ENDPOINT variable is checked in this constructor. Other environmental
    variables may be used in particular DLS API implementations.

    The verbosity level affects invocations of all methods in this object. See
    the setVerbosity method for information on accepted values.

    @param dls_endpoint: the DLS server, as a string "hostname[:port][/path/to/DLS]"
    @param verbosity: value for the verbosity level
    @param kwd: Flags: any other parameters for the DLS server
                  e.g. a dbs_client_config file or version for DLS with DBS back-end
    """

    self.setVerbosity(verbosity)

    self.server = dls_endpoint

    if(not self.server):
      self.server = environ.get("DLS_ENDPOINT")
    
    self.warnfd = stdout
    self.debugfd = stdout

  
  def __del__(self):
    """
    Destructor. May need to close the file used to log the warnings and debug
    info
    """
    
    if(self.warnfd != stdout):
       try:
          self.warnfd.close()
       except Exception, inst:
          pass

    if(self.debugfd != stdout):
       try:
          self.debugfd.close()
       except Exception, inst:
          pass


  ############################################
  # Methods defining the main public interface
  ############################################

  def add(self, dlsEntryList, **kwd):
    """
    Adds the specified DlsEntry object (or list of objects) to the DLS.

    For each specified DlsEntry with a non-registered FileBlock, a new entry is
    created in the DLS, and all locations listed in the DlsLocation list of the object
    are also registered. For the DlsEntry objects with an already registered FileBlock,
    only the locations are added. If no locations are specified, then the FileBlock
    itself is not created, unless the allowEmptyBlocks (**kwd) flag is set to True.

    If the checkLocations (**kwd) flag is set to True (default), before adding
    any location to a FileBlock, all of its specified locations are checked to
    be resolvable into IP adresses in order to be admitted as valid locations.
    If it is set to False, no check is made.

    For DLS implementations with hierarchical FileBlock namespace, the method may
    support a flag, createParent (**kwd), that, if true, will cause the check for
    existence of the specified FileBlock parent directory tree, and the creation of
    that tree if it does not exist. The default for this flag is True.

    The supported attributes of the FileBlocks and of the locations, which are not null
    are also set for all the new registrations. Unsupported attributes are just ignored.

    Check the documentation of the concrete DLS client API implementation for
    supported attributes.

    The method will not raise an exception in case there is an error adding a FileBlock
    or location, but will go on with the rest, unless errorTolerant (**kwd) is set 
    to False. This last may be useful when transactions are used. In that case an error
    may cause and automatic roll-back so it is better that the method exits after 
    the first failure.

    If session(**kwd) is set to True, the whole operation of the method is
    performed within a session (if the DLS implementation supports it).
    That is, the following call::
      api.add(x, session = True)
    is equivalent to::
      api.startSession()
      api.add(x)
      api.endSession()

    If trans(**kwd) is set to True, the whole operation of the method is
    performed within a transaction (if the DLS implementation supports it),
    in the same way as if it was within a session. If trans is True, the
    errorTolerant and session flags are ignored and considered False.

    In some implementations it is not safe to nest sessions or transactions,
    so do not do it.

    @exception XXXX: On error with the DLS catalog

    @param dlsEntryList: the DlsEntry object (or list of objects) to be added to the DLS
    @param kwd: Flags:
      - checkLocations: boolean (default True) for checking existence of added locations
      - createParent: boolean (default True) for parent directory creation
      - errorTolerant: boolean (default True) for raising an exception after failure
      - trans: boolean (default False) for using a transaction for the operations
      - session: boolean (default False) for using a session for the operations
      - allowEmptyBlocks: booleand (default False) for adding FileBlocks without location
    """

    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg) 
 
  def update(self, dlsEntryList, **kwd):
    """
    Updates the attributes of the specified DlsEntry object (or list of objects)
    in the DLS.

    For each specified DlsEntry, the supported not null attributes of the composing
    DlsFileBlock object and the supported not null attributes of the DlsLocation
    objects of the composing locations list are updated.

    Check the documentation of the concrete DLS client API implementation for
    supported attributes.

    The method will not raise an exception in case there is an error updating the
    attributes of a FileBlock or location, but will go on with the rest, unless
    errorTolerant (**kwd) is set to False. This last may be useful when transactions
    are used. In that case an error may cause and automatic roll-back so it is better
    that the method exits after the first failure.

    If session(**kwd) is set to True, the whole operation of the method is
    performed within a session (if the DLS implementation supports it).
    That is, the following call::
      api.update(x, session = True)
    is equivalent to::
      api.startSession()
      api.update(x)
      api.endSession()

    If trans(**kwd) is set to True, the whole operation of the method is
    performed within a transaction (if the DLS implementation supports it),
    in the same way as if it was within a session. If trans is True, the
    errorTolerant and session flags are ignored and considered False.
    
    In some implementations it is not safe to nest sessions or transactions,
    so do not do it.

    @exception XXXX: On error with the DLS catalog

    @param dlsEntryList: the DlsEntry object (or list of objects) to be updated
    @param kwd: Flags:
     - errorTolerant: boolean (default True) for raising an exception after failure
     - trans: boolean (default False) for using a transaction for the operations
     - session: boolean (default False) for using a session for the operations
    """

    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg) 


  def delete(self, dlsEntryList, **kwd):
    """
    Deletes the locations of the list composing the specified DLSEntry object
    (or list of objects) from the DLS. If the last location associated with
    the FileBlock is deleted, the FileBlock is also removed.

    For each specified DlsEntry, the locations specified in the composing
    location list are removed (none if empty). However, if all (**kwd) is set
    to True, then all locations associated with the FileBlock are removed,
    regardless of the contents of the specified location list.
    
    In any case, if the last location associated in the catalog with the
    specified FileBlock is deleted, the FileBlock itself is also removed, 
    unless keepFileBlock (**kwd) is set to true.

    For DLS implementations with a hierarchical FileBlock namespace, in the
    all==True case, the method will also delete empty directories in the
    hierarchy. Non empty directories will refuse to be removed (raising 
    an exception or printing a warning).

    A location will not be removed if it is custodial (f_type  == "P"),
    unless force (*kwd) is set to True.

    The method will not raise an exception for every error, but will try to
    go on with all the asked deletions, unless errorTolerant (**kwd) is set 
    to False. 
    
    If session(**kwd) is set to True, the whole operation of the method is
    performed within a session (if the DLS implementation supports it).
    That is, the following call::
      api.delete(x, session = True)
    is equivalent to::
      api.startSession()
      api.delete(x)
      api.endSession()

    In some implementations it is not safe to nest sessions, so do not do it.

    NOTE: In some implementations it is not safe to use this method within a
    transaction. 

    @exception XXXX: On error with the DLS catalog

    @param dlsEntryList: the DlsEntry object (or list of objects) to be deleted 
    @param kwd: Flags:
      - all: boolean (default False) for removing all locations 
      - keepFileBlock: boolean (default False) for not deleting empty Fileblocks
      - force: boolean (default False) for removing custodial locations 
      - errorTolerant: boolean (default True) for raising an exception after failure
      - session: boolean (default False) for using a session for the operations
    """

    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)

    
  def getLocations(self, fileBlockList, **kwd):
    """
    Returns a list of DlsEntry objects holding the locations in which the specified
    FileBlocks are stored.
    
    A single FileBlock or a list of those may be used as argument. Each FileBlock may
    be specified as simple strings (names) or as DlsFileBlock objects. The
    returned list contains a DlsEntry object per specified FileBlock.

    The returned objects will have a composing DlsFileBlock object containing
    the specified FileBlock name, and a composing DlsLocation object list holding
    the corresponding retrieved locations.

    By default, the method may raise an exception if an error in the DLS operation
    occurs. But if errorTolerant (**kwd) is set to true, the method will not
    break on the first error, but will warn and try to keep on with the rest
    of fileblocks in the argument list. In this case, the returned list will
    contain only the entries for which the associated replicas could be
    successfully retrieved. It is also possible that, even if errorTolerant is
    used, an exception is raised in case of general failure.

    If longList (**kwd) is set to true, some location attributes are also included
    in the returned DlsLocation objects. Check the documentation of the concrete
    DLS client API implementation for the list of attributes.

    NOTE: Some implementations may not support the long listing.

    If session(**kwd) is set to True, the whole operation of the method is
    performed within a session (if the DLS implementation supports it).
    That is, the following call::
      api.getLocations(x, session = True)
    is equivalent to::
      api.startSession()
      api.getLocations(x)
      api.endSession()

    In some implementations it is not safe to nest sessions, so do not do it.

    NOTE: Normally, it makes no sense to use this method within a transaction.

    For operational reasons, some implementations (indicated in their documentation)
    may hide some FileBlocks locations from the result. The showProd(**kwd) and
    showCAF(**kwd) flags may be set to True to turn off prod-only and CAF filters.
    Likewise, if the subscribed or custodial flags are set to True, some replicas are 
    not shown. If not supported, the flags are ignored. Please do not use them unless 
    you know what you are doing.

    @exception XXXX: On error with the DLS catalog

    @param fileBlockList: the FileBlock as string/DlsFileBlock (or list of those)
    @param kwd: Flags:
     - longList: boolean (default False) for the listing of location attributes
     - session: boolean (default False) for using a session for the operations
     - errorTolerant: boolean (default False) for raising an exception after failure
     - showProd: boolean (default False) for turning off the filtering of prod-only replicas
     - showCAF: boolean (default False) for turning off the filtering of CAF replicas
     - subscribed: boolean (default False) for showing only subscribed replicas
     - custodial: boolean (default False) for showing only custodial replicas

    @return: a list of DlsEntry objects containing the locations
    """

    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)
    

  def getFileBlocks(self, locationList, **kwd):
    """
    Returns a list of DlsEntry objects holding the FileBlocks stored in the
    specified locations.
    
    NOTE: Depending on the implementation, this method may be a very expensive
    operation and affect DLS response, so use it only with care!!

    A single location or a list of those may be used as argument. The locations
    may  be specified as simple strings (hostnames) or as DlsLocation objects.
    The returned list contains a DlsEntry object per FileBlock-location pair; 
    i.e.: for each specified location, one DlsEntry object per FileBlock
    stored there.

    The returned objects will have a composing DlsFileBlock object containing the
    interesting FileBlock name, and a composing DlsLocation object holding the 
    corresponding specified location.

    The method may raise an exception if an error in the DLS operation occurs.

    If session(**kwd) is set to True, the whole operation of the method is
    performed within a session (if the DLS implementation supports it).
    That is, the following call::
      api.getFileBlocks(x, session = True)
    is equivalent to::
      api.startSession()
      api.getFileBlocks(x)
      api.endSession()

    In some implementations it is not safe to nest sessions, so do not do it.

    NOTE: Normally, it makes no sense to use this method within a transaction, so
    please avoid it. 

    For operational reasons, some implementations (indicated in their documentation)
    may hide some FileBlocks locations from the result. The showProd(**kwd) and
    showCAF(**kwd) flags may be set to True to turn off prod-only and CAF filters.
    Likewise, if the subscribed or custodial flags are set to True, some replicas are 
    not shown. If not supported, the flags are ignored. Please do not use them unless 
    you know what you are doing.

    @exception XXXX: On error with the DLS catalog

    @param locationList: the location as string/DlsLocation (or list of those)
    @param kwd: Flags:
     - session: boolean (default False) for using a session for the operations
     - showProd: boolean (default False) for turning off the filtering of prod-only replicas
     - showCAF: boolean (default False) for turning off the filtering of CAF replicas
     - subscribed: boolean (default False) for showing only subscribed replicas
     - custodial: boolean (default False) for showing only custodial replicas

    @return: a list of DlsEntry objects containing the FileBlocks
    """
    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)


  def listFileBlocks(self, fileBlockList, **kwd):
    """
    Returns a list of DlsFileBlock objects holding the information of the
    specified FileBlocks, or, for implementations with hierarchical FileBlock
    namespace, of the FileBlocks under the specified FileBlock directory.
    
    A single FileBlock, or a list of those, or a single Fileblock directory (not 
    a list) may be used as argument. In the case of FileBlocks, they may be
    specified as simple strings (FileBlock names) or as DlsFileBlock objects,
    and the returned list will contain a DlsFileBlock object per specified
    FileBlock. In the case of directories, the argument should be a string 
    holding the directory name, and the returned list will hold a DlsFileBlock 
    object per FileBlock under that directory.

    The returned DlsFileBlock objects will contain both the FileBlock name
    and, if longList (**kwd) is set to true, some FileBlock attributes.
    Check the documentation of the concrete DLS client API implementation
    for the list of attributes

    For the case of directory listing, if recursive (**kwd) is set to True,
    the returned list will contain also the FileBlocks of the subdirectories
    under the specified one in a recursive way. DLS implementations with 
    flat FileBlock namespace will just ignore this flag.

    NOTE: Be aware that depending on the catalog a recursive listing may be
    a very costly operation and affect DLS response, so please use this
    flag only with care!!
    
    The method may raise an exception if an error in the DLS operation occurs.

    If session(**kwd) is set to True, the whole operation of the method is
    performed within a session (if the DLS implementation supports it).
    That is, the following call::
      api.listFileBlocks(x, session = True)
    is equivalent to::
      api.startSession()
      api.listFileBlocks(x)
      api.endSession()

    In some implementations it is not safe to nest sessions, so do not do it.

    NOTE: Normally, it makes no sense to use this method within a transaction, so
    please avoid it. 

    @exception XXXX: On error with the DLS catalog

    @param fileBlockList: the FileBlock, as string or DlsFileBlock object (or
    list of those), or a FileBlock namespace directory, as a string
    @param kwd: Flags:
     - longList: boolean (default True) for the listing of location attributes
     - session: boolean (default False) for using a session for the operations
     - recursive: boolean (default False) for recursive listing of a directory 

    @return: a list of DlsFileBlock objects containing the FileBlock information
    """
    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)


  def renameFileBlock(self, oldFileBlock, newFileBlock, **kwd):
    """
    Renames the specified oldFileBlock to the new name specified as
    newFileBlock. Both arguments can be specified either as DlsFileBlock objects
    or simple strings (holding the name of the FileBlocks).

    If newFileBlock exists alread, it will be removed before the rename
    takes place.

    For DLS implementations with hierarchical FileBlock namespace, directory 
    FileBlocks may also be renamed. Check the corresponding implementation 
    documentation. Also, the method may support a flag, createParent (**kwd),
    that, if true, will cause the check for existence of the specified
    newFileBlock parent directory tree, and the creation of that tree if it
    does not exist. The default for this flag is False.

    The method will raise an exception in case there is an error renaming the
    FileBlock or creating the parent directories of the new FileBlock.

    If session(**kwd) is set to True, the whole operation of the method is
    performed within a session (if the DLS implementation supports it).
    That is, the following call::
      api.add(x, session = True)
    is equivalent to::
      api.startSession()
      api.add(x)
      api.endSession()

    If trans(**kwd) is set to True, the whole operation of the method is
    performed within a transaction (if the DLS implementation supports it),
    in the same way as if it was within a session. If trans is True, the
    session flag is ignored and considered False.

    In some implementations it is not safe to nest sessions or transactions,
    so do not do it.

    @exception XXXX: On error with the DLS catalog

    @param oldFileBlock: the FileBlock to rename, as DlsFileBlock object or string
    @param newFileBlock: the new name for the FileBlock, as DlsFileBlock object or string
    @param kwd: Flags:
      - createParent: boolean (default True) for parent directory creation
      - trans: boolean (default False) for using a transaction for the operations
      - session: boolean (default False) for using a session for the operations
    """

    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg) 
 

  def getAllLocations(self, **kwd):
    """
    Returns all the locations in the DLS that are associated with any
    FileBlock in the catalog. The locations are returned as a list
    of DlsLocation objects.

    This methods accepts no arguments (other than possibly some kwd flags).

    NOTE: Depending on the implementation, this method may be a very expensive
    operation and affect DLS response, so use it only with care!!
    
    The method may raise an exception if an error in the DLS operation occurs.

    If session(**kwd) is set to True, the whole operation of the method is
    performed within a session (if the DLS implementation supports it).
    That is, the following call::
      api.getAllLocations(session = True)
    is equivalent to::
      api.startSession()
      api.getAllLocations(x)
      api.endSession()

    In some implementations it is not safe to nest sessions, so do not do it.

    NOTE: Normally, it makes no sense to use this method within a transaction, so
    please avoid it. 

    @exception XXXX: On error with the DLS catalog

    @param kwd: Flags:
     - session: boolean (default False) for using a session for the operations

    @return: a list of DlsLocation objects containing the locations information
    """
    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)


  def dumpEntries(self, dir = "/", **kwd):
    """
    Returns the DLS entries under the specified directory in the FileBlock
    namespace, as a list of DlsEntry objects. These objects will include both
    FileBlock names and associated locations. In the case of DLS
    implementations with a flat FileBlock namespace, the directory argument
    will be ignored (i.e.: it will behave as if "/" is specified).
    
    A FileBlock directory (not a list) must be specified as argument
    of the method, in the form of a string or a DlsFileBlock object.
    
    If recursive (**kwd) is set to True, the returned list will contain also
    the FileBlocks of the subdirectories under the specified one in a
    recursive way. DLS implementations with flat FileBlock namespace will
    just ignore this flag.

    NOTE: Be aware that depending on the catalog a recursive listing may be
    a very costly operation and affect DLS response, so please use this flag
    only with care!!
    
    The method may raise an exception if an error in the DLS operation occurs.

    If session(**kwd) is set to True, the whole operation of the method is
    performed within a session (if the DLS implementation supports it).
    That is, the following call::
      api.dumpEntries(x, session = True)
    is equivalent to::
      api.startSession()
      api.dumpEntries(x)
      api.endSession()

    In some implementations it is not safe to nest sessions, so do not do it.

    NOTE: Normally, it makes no sense to use this method within a transaction, so
    please avoid it. 

    For operational reasons, some implementations (indicated in their documentation)
    may hide some FileBlocks locations from the result. The showProd(**kwd) and
    showCAF(**kwd) flags may be set to True to turn off prod-only and CAF filters.
    Likewise, if the subscribed or custodial flags are set to True, some replicas are 
    not shown. If not supported, the flags are ignored. Please do not use them unless 
    you know what you are doing.

    @exception XXXX: On error with the DLS catalog

    @param dir: the FileBlock dir, as string or DlsFileBlock object
    @param kwd: Flags:
     - session: boolean (default False) for using a session for the operations
     - recursive: boolean (default False) for recursive listing of a directory 
     - showProd: boolean (default False) for turning off the filtering of prod-only replicas
     - showCAF: boolean (default False) for turning off the filtering of CAF replicas
     - subscribed: boolean (default False) for showing only subscribed replicas
     - custodial: boolean (default False) for showing only custodial replicas

    @return: a list of DlsEntry objects representing the DLS data
    """
    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)


  def getFileLocs(self, fileBlockList, **kwd):
    """
    Returns the files composing the specified FileBlocks and the locations
    where each of these files are replicated.
    
    NOTE: A FileBlock is composed of files. DLS original function dealt with
    FileBlocks cataloging and not at all with files. Only some DLS API 
    implementations will support this method. 

    A single FileBlock or a list of those may be used as argument. Each FileBlock
    may be specified as simple strings (names) or as DlsFileBlock objects. 
    
    The returned list contains a pair of DlsFileBlock object and dict per specified
    FileBlock. Each dict has DlsFile objects as keys and a list of DlsLocation
    objects as values for each DlsFile.

    For operational reasons, some implementations (indicated in their documentation)
    may hide some file locations from the result. The showProd(**kwd) and
    showCAF(**kwd) flags may be set to True to turn off prod-only and CAF filters.
    Likewise, if the subscribed or custodial flags are set to True, some replicas are 
    not shown. If not supported, the flags are ignored. Please do not use them unless 
    you know what you are doing.

    @exception XXXX: On error with the DLS catalog

    @param fileBlock: the FileBlock as string/DlsFileBlock
    @param kwd: Flags:
     - showProd: boolean (default False) for turning off the filtering of prod-only replicas
     - showCAF: boolean (default False) for turning off the filtering of CAF replicas
     - subscribed: boolean (default False) for showing only subscribed replicas
     - custodial: boolean (default False) for showing only custodial replicas

    @return: list of pairs DlsFileBlock-dict, each dict with DlsFile objs as keys and lists of DlsLocation as values 
    """

    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)
   

  def startSession(self):
    """
    For DLS implementations supporting sessions (for performance improvements
    in the DLS access), starts a session. If the DLS implementation does
    not support sessions, the method does nothing.

    The session is opened with the server set at object creation time and 
    should be ended with the endSession method afterwards.    

    A transaction with the DLS implies a session with it, so do not include
    one within another. Do not nest transactions or sessions either.

    @exception XXXX: On error with the DLS catalog
    """
    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)
  
 
  def endSession(self):
    """
    For DLS implementations supporting sessions (for performance improvements
    in the DLS access), ends a previoulsy opened session. If the DLS
    implementation does not support sessions, the method does nothing.

    The session to end is the one opened previously with the startSession
    method.

    @exception XXXX: On error with the DLS catalog
    """
    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)
  
 
  def startTrans(self):
    """
    For DLS implementations supporting transactions (for performance
    improvements and atomic operations in the DLS access), starts a transaction.
    If the DLS implementation does not support transactions, the method does
    nothing.

    The transaction is opened with the server set at object creation time. 
    From that moment on, every operation is performed within a transaction, so 
    any failure or a call to the abortTrans method will cause a roll-back 
    of the operations. If no error is produced and the transaction is ended
    with the endTrans method, the operations are then executed at once.

    A transaction with the DLS implies a session with it, so do not include
    one within another. Do not nest transactions or sessions either.

    Please check the DLS implementation notes on handling transactions in DLS
    interaction, since this is not always trivial.

    @exception XXXX: On error with the DLS catalog
    """
    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)
  
 
  def endTrans(self):
    """
    For DLS implementations supporting transactions (for performance
    improvements and atomic operations in the DLS access), ends a transaction,
    causing the execution of all the operations performed during the 
    transaction (since startTrans was used to start it). If the DLS
    implementation does not support transactions, the method does nothing.

    If a failure on the interaction with DLS occurs within the transaction,
    the operations are roll-backed.

    Please check the DLS implementation notes on handling transactions in DLS
    interaction.

    @exception XXXX: On error with the DLS catalog
    """
    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)
  
  
  def abortTrans(self):
    """
    For DLS implementations supporting transactions (for performance
    improvements and atomic operations in the DLS access), aborts a transaction,
    causing the roll-back of all operations performed within the
    transaction (since startTrans was used to start it). If the DLS
    implementation does not support transactions, the method does nothing.

    Please check the DLS implementation notes on handling transactions in DLS
    interaction.

    @exception XXXX: On error with the DLS catalog
    """
    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)
  
 

  ##################################
  # Other public methods (utilities)
  ##################################

  def changeFileBlocksLocation(self, org_location, dest_location, **kwd):
    """
    For all the FileBlocks registered in the DLS server in the location
    "org_location", changes them so that they no longer exist in "org_location",
    but they are now in "dest_location".

    If the checkLocations (**kwd) flag is set to True (default), before adding
    any performing the replacement the specified new location is checked to
    be resolvable into IP adresses in order to be admitted as valid location.
    If the test is not passed, the renaming is not performed. If the flag is set
    to False, this check is skipped.

    The method may raise an exception if there is an error in the operation.

    @param org_location: original location to be changed (hostname), as a string
    @param dest_location: new location for FileBlocks (hostname), as a string
    @param kwd: Flags:
      - checkLocations: boolean (default True) for checking validity of dest_location
    """
    msg = "This is just a base class!"
    msg += " This method should be implemented in an instantiable DLS API class"
    raise NotImplementedError(msg)

        
  def setVerbosity(self, value = DLS_VERB_WARN):
    """
    Sets the verbosity level for all subsequent DlsApi methods.
    
    Currently admitted values are:    
     - DLS_VERB_NONE => print nothing
     - DLS_VERB_WARN => print only warnings (to stdout)
     - DLS_VERB_HIGH => print warnings (stdout) and debug messages (stdout)

    @exception ValueError: if the specified value is not one of the admitted ones

    @param value: the new value for the verbosity level 
    """
    admitted_vals = [DLS_VERB_NONE, DLS_VERB_INFO, DLS_VERB_WARN, DLS_VERB_HIGH]
    if(value not in admitted_vals):
      msg = "The specified value is not one of the admitted ones"
      raise ValueError(msg)

    self.verb = value


  def setWarningLogFile(self, fname = None):
    """
    Sets a file to redirect the warning messages of the API (by default is just stdout)
    
    @exception Exception: if the file cannot be opened in append mode

    @param fname: the name of the file to be used for the warning messages
    """
    if(file):
       # May raise an exception (for user to deal with)
       self.warnfd = open(fname, 'a')
    else:
       self.warnfd = stdout

  def setDebugLogFile(self, fname = None):
    """
    Sets a file to redirect the debug messages of the API (by default is just stdout)
    
    @exception Exception: if the file cannot be opened in append mode

    @param fname: the name of the file to be used for the debug messages
    """
    if(file):
       # May raise an exception (for user to deal with)
       self.debugfd = open(fname, 'a')
    else:
       self.debugfd = stdout

 
 
  ##################################
  # Private methods
  ##################################

  def _warn(self, msg):
    if(self.verb >= DLS_VERB_WARN):
       self.warnfd.write("Warning: %s\n\n" % (msg))
       self.warnfd.flush()

  def _debug(self, msg):
    if(self.verb >= DLS_VERB_HIGH):
       self.debugfd.write("--%s\n\n" % (msg))
       self.debugfd.flush()
