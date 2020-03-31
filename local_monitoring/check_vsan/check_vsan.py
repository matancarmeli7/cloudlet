#!/usr/bin/python
from pyVim.connect import SmartConnect, Disconnect
import sys
import ssl
import atexit
import argparse
import getpass
#import the VSAN API python bindings
import vmware.vsan.vsanmgmtObjects as vsanmgmtObjects
import vmware.vsan.vsanapiutils as vsanapiutils
nagOK=0
nagWARN=1
nagCRIT=2
nagUNKWN=3

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(
       description='Process args for VSAN SDK sample application')
   parser.add_argument('-H', '--hostname', required=True, action='store',
                       help='Remote host to connect to')
   parser.add_argument('-o', '--port', type=int, default=443, action='store',
                       help='Port to connect on')
   parser.add_argument('-u', '--user', required=True, action='store',
                       help='User name to use when connecting to host')
   parser.add_argument('-p', '--password', required=False, action='store',
                       help='Password to use when connecting to host')
   parser.add_argument('--cluster', dest='clusterName', metavar="CLUSTER",
                      default='VSAN-Cluster')
   parser.add_argument('-v', '--verbose', action='count', default=0,
                       help='-v: verbose output, -vv: debug output')
   args = parser.parse_args()
   return args

def getClusterInstance(clusterName, serviceInstance):
   content = serviceInstance.RetrieveContent()
   searchIndex = content.searchIndex
   datacenters = content.rootFolder.childEntity
   for datacenter in datacenters:
      cluster = searchIndex.FindChild(datacenter.hostFolder, clusterName)
      if cluster is not None:
         return cluster
   return None


def showStat( stat, msg ):
   if stat == nagOK:
     print"OK: " + msg
   elif stat == nagWARN:
      print"Warning: " + msg
   elif stat == nagCRIT:
      print"Critical: " + msg
   else:
      print"Unknown: " + msg
    

#Start program
def main():
   args = GetArgs()
   if args.password:
      password = args.password
   else:
      password = getpass.getpass(prompt='Enter password for host %s and '
                                        'user %s: ' % (args.hostname,args.user))
   
   # Some default states
   nagStat = nagOK
   statMsg = ""
   numHealthyObjs = 0
   debugOut = ""
      #For python 2.7.9 and later, the defaul SSL conext has more strict
   #connection handshaking rule. We may need turn of the hostname checking
   #and client side cert verification
   context = None
   if sys.version_info[:3] > (2,7,4):
      context = ssl.create_default_context()
      context.check_hostname = False
      context.verify_mode = ssl.CERT_NONE
   
   try:
      si = SmartConnect(host=args.hostname,
                     user=args.user,
                     pwd=password,
                     port=int(args.port),
                     sslContext=context)
      atexit.register(Disconnect, si)
   except Exception, e:
   	  statMsg = "Connection failure."
   	  if args.verbose > 1:
   	  	debugOut += "\nDEBUG::" + str(e)
   	  nagStat = nagUNKWN
   	  showStat(nagStat,statMsg+debugOut)
   	  return nagStat


   #for detecting whether the host is VC or ESXi
   aboutInfo = si.content.about
      
   if aboutInfo.apiType == 'VirtualCenter':
      majorApiVersion = aboutInfo.apiVersion.split('.')[0]
      if int(majorApiVersion) < 6:
         statMsg = "The Virtual Center with version "+aboutInfo.apiVersion+" (lower than 6.0) is not supported."
         nagStat = nagUNKWN
         showStat(nagStat,statMsg)
         return nagStat

      #H Access VC side VSAN Health Service API
      vcMos = vsanapiutils.GetVsanVcMos(si._stub, context=context)
      # Get vsan health system
      vhs = vcMos['vsan-cluster-health-system']

      cluster = getClusterInstance(args.clusterName, si)

      if cluster is None:
         statMsg = "Cluster "+args.clusterName+" is not found for "+args.host+"."
         nagStat = nagUNKWN
         showStat(nagStat,statMsg)
         return nagStat
      
			# We need to fetch results from cache otherwise the checks timeout.
			      
      healthSummary = vhs.QueryClusterHealthSummary(
         cluster=cluster, includeObjUuids=True, fetchFromCache=True )
      objectStatus = healthSummary.objectHealth
      

      for objStatus in objectStatus.objectHealthDetail:
         if args.verbose > 0:
            debugOut += "\n" + objStatus.health + ": " + str(objStatus.numObjects)
         if objStatus.health != "healthy" and objStatus.numObjects > 0:
            statMsg += objStatus.health+": "+ str(objStatus.numObjects)
            nagStat = nagCRIT
         elif objStatus.health == "healthy":
            numHealthyObjs = objStatus.numObjects

      
      statMsg += " Healthy: " + str(numHealthyObjs)
      showStat(nagStat,statMsg+debugOut)

      
      return nagStat

# Start program
if __name__ == "__main__":
   exit(main())
