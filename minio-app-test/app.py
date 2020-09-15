import minio
import time
from minio import Minio
from minio.error import ResponseError
import sys

sys.path.insert(1, '/minio-test/src/config')
from config import *
minioClient = Minio(minio_url,
                    secure = False,
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
