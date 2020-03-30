VMware vSAN SDK for Python
=================================

The VMware vSAN SDK supports the development of programs that manage
vSAN using vSAN Management API.

VMware vSAN runs in conjunction with vCenter and ESXi servers.
Please note that the VMware vSphere API is required as a baseline for using
vSAN API (i.e. vSphere API should be used for logging in, retreiving
ManagedEntities like vCenter clusters).

VMware vSAN SDK for Python depends on pyVmomi (v6.7.0) - the Python
SDK for the VMware vSphere API. You should know how to use pyVmomi before
trying this SDK. Please refer to https://github.com/vmware/pyvmomi for pyVmomi
documentation and software.

The vSAN SDK for Python includes the following documentation and software.
*  vSAN API reference - HTML documents in the 'docs' directory
   You can browse it with your browsers by opening the index.html locally.

*  Python bindings - the Python module/file under the 'bindings' directory
   It allows you to access vSAN management APIs. You need to put it
   in a path where your Python programs can import. Note that pyVmomi must
   be loaded before importing the vSAN bindings.

*  Sample codes - the sample programs and dependent libraries under the
   'samplecode' directory. To run the sample program, firstly you need to put
   the python binding - 'vsanmgmtObjects.py' to the same directory of the
   sample or paths where can be searched by Python. Then you can run the
   sample codes.

Sample code usage:
   python vsanapisamples.py -s <host-address> -u <username> -p <password>
      --cluster <cluster-name>
   python vsaniscsisamples.py -s <host-address> -u <username> -p <password>
      --cluster <cluster-name>

* Use "-h" or "--help" to see parameter usage message.
* Note that the vsanapisamples.py and vsaniscsisamples.py depends on the
  vsanapiutis.py, which provides uitlity libraries to retrieve vSAN
  Managed Objects.
* You can use the sample code to get vSAN Managed Objects on vCenter and
  ESXi servers. It will automatically identify the target server type.
