import minio
import time
from minio import Minio
from minio.error import ResponseError
import sys
import urllib3
import base64
from kubernetes import client, config

urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

sys.path.insert(1, '/minio-test/src/config')
from config import *


def minioCon():
    httpClient = urllib3.PoolManager(
                    timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
                            cert_reqs='CERT_REQUIRED',
                            ca_certs='/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem',
                            retries=urllib3.Retry(
                                total=5,
                                backoff_factor=0.2,
                                status_forcelist=[500, 502, 503, 504]))

    accessKey = minioSecret('accesskey')
    secretKey = minioSecret('secretkey')
    minioClient = Minio(minio_url,
                        secure = True,
                        http_client=httpClient,
                        access_key = accessKey,
                        secret_key = secretKey)
    return(minioClient)

def minioSecret(data_64):
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    base64_data_json=v1.read_namespaced_secret('minio-creds-secret', 'quay-minio')
    base64_data = base64_data_json.data[data_64]
    base64_bytes = base64_data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    data_decode = message_bytes.decode('ascii')
    return(data_decode)

def makeBucket(minioClient):
    global bucketName
    bucketName = bucket_name
    try:
        minioClient.make_bucket(bucketName)
    
    except Exception as err:
        return(err)
    
    found = minioClient.bucket_exists(bucketName)
    return(found)

def removeBucket(minioClient):
    try:
        minioClient.remove_bucket(bucketName)

    except Exception as err:
        return(err)

    found = minioClient.bucket_exists(bucketName)
    return(found)

def main():
    minioClient = minioCon()
    makeBucketRes = makeBucket(minioClient)
    if makeBucketRes == True:
        removeBucketRes = removeBucket(minioClient)
        if removeBucketRes == False:
            print("SUCCESS")
            sys.exit(0)
        else:
            print('err ' + str(removeBucketRes))
            sys.exit(1)
    else:
        print('err ' + str(makeBucketRes))
        sys.exit(1)

if __name__ == '__main__':
    main()
