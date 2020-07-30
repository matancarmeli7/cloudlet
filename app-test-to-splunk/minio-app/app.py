#!/usr/bin/python3
import minio
import flask
import time
from flask import Flask
from minio import Minio
#from minio.error import ResponseError
#import response
import sys

sys.path.insert(1, '/minio-test/src/config')
from config import *
minioClient = Minio(minio_url,
                    secure = False,
                    access_key = minio_access_key,
                    secret_key = minio_secret_key)

app = Flask(__name__)

@app.route("/minio/test")
def main():
    makeBucketRes = makeBucket()
    try:
        if makeBucketRes.status_code == 200:
            removeBucketRes = removeBucket()
    except Exception:
        return(str(makeBucketRes))
    try:
        if removeBucketRes.status_code == 200:
            return("SUCCESS")
    except Exception:
       return(str(removeBucketRes))

def makeBucket():
    global bucketName
    bucketName = bucket_name
    status_code = flask.Response(status=200)
    try:
        minioClient.make_bucket(bucketName, location="us-east-1")
        return(status_code)
    except Exception as err:
        return(err)

def removeBucket():
    try:
        minioClient.remove_bucket(bucketName)
        status_code = flask.Response(status=200)
        return(status_code)

    except Exception as err:
        return(err)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
