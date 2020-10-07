import minio
import time
from minio import Minio
from minio.error import ResponseError
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

sys.path.insert(1, '/minio-test/src/config')
from config import *

httpClient = urllib3.PoolManager(
                timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
                        cert_reqs='CERT_REQUIRED',
                        ca_certs='/etc/pki/ca-trust/source/anchors/rootCA.pem',
                        retries=urllib3.Retry(
                            total=5,
                            backoff_factor=0.2,
                            status_forcelist=[500, 502, 503, 504]))

minioClient = Minio(minio_url,
                    secure = False,
                    http_client=httpClient,
                    access_key = minio_access_key,
                    secret_key = minio_secret_key)

def main():
    makeBucketRes = makeBucket()
    if makeBucketRes == True:
        removeBucketRes = removeBucket()
        if removeBucketRes == False:
            print("SUCCESS")
            sys.exit(0)
        else:    
            print(removeBucketRes)
            sys.exit(1)
    else:
        print(makeBucketRes)
        sys.exit(1)

def makeBucket():
    global bucketName
    bucketName = bucket_name
    try:
        minioClient.make_bucket(bucketName)
    
    except Exception as err:
        return(err)
    
    found = minioClient.bucket_exists(bucketName)
    return(found)

def removeBucket():
    try:
        minioClient.remove_bucket(bucketName)

    except Exception as err:
        return(err)

    found = minioClient.bucket_exists(bucketName)
    return(found)

main()
