import flask
import time
from flask import Flask

app = Flask(__name__)

@app.route("/app/test")
def appTest():
    if appTestFunction():
        print("all good")
    else:
        print("oh no")    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000')

def appTestFunction():
    pass
    # Write your test code here
    # You're welcomed to add multible functions that you will call from here
    # Your final return of this function should be boolean - true or false
    # If you need to access the cluster fqdn use cluster_fqdn var
