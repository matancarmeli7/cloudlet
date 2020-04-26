import socket
import sys
import time
import requests
import os

PORT = int(os.environ['PORT'])
KB_CHUNKS = int(os.environ['KB_CHUNKS'])
SPLUNK_TOKEN = os.environ['SPLUNK_TOKEN']
SPLUNK_URL = os.environ['SPLUNK_URL']
TESTS_PER_CLIENT = int(os.environ['TESTS_PER_CLIENT'])

# Log to central Splunk
def logSplunk(log):
  myobj = {"event": log}
  x = requests.post(SPLUNK_URL, json = myobj, auth=('Splunk', SPLUNK_TOKEN), verify=False)

def uploadTest():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('0.0.0.0', PORT)
    print('starting up')
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    # Create dictionary to hold data for each client
    clientsData = {}

    # Listen forever
    while True:
        # Save if the current client finished successfully
        finishedSuccessfully = True;

        try:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = sock.accept()
            print('Accepted a connection')
            start = time.time()
            
            # Init counter variables
            dataAmount = 0
            end = 0

            # The first 20 characters will be the cluster name
            clusterName = connection.recv(20).decode().split("\0")[0]

            # Init if never head about the current cluster
            if not clusterName in clientsData:
                clientsData[clusterName] = {}
                clientsData[clusterName]['testCount'] = 0
                clientsData[clusterName]['speed'] = 0

            # Receive the data in small chunks and retransmit it
            while True:
                # Receive KB_CHUNKS of data
                data = connection.recv(1024 * KB_CHUNKS)
                if data:
                    dataAmount += KB_CHUNKS;
                else:
                    print ('No more data from ' + str(client_address))
                    end = time.time()
                    break
        except Exception:
            finishedSuccessfully = False
            pass
        finally:
            # Clean up the connection
            connection.close()

            # Calculate the speed of the upload only if finished successfully
            if (finishedSuccessfully):
                # Convert to MB
                dataAmount = dataAmount  / 1024
                finalTime = end - start

                print ("Data amount: " + str(dataAmount) + ", final Time: " + str(finalTime))

                # convert to Mbit per second, from Mbyte per second
                speed = (dataAmount / finalTime) * 8

                # Increase the test count by one
                clientsData[clusterName]['testCount'] += 1

                # If it's the first test for the current cluster
                if clientsData[clusterName]['testCount'] == 1:
                    # Save the speed for the current cluster
                    clientsData[clusterName]['speed'] = speed

                # Save only the smallest speed test for the current client
                elif  (speed < clientsData[clusterName]['speed']):
                    clientsData[clusterName]['speed'] = speed

                # After reaching the desired amount of testing for the current client
                if (clientsData[clusterName]['testCount'] == TESTS_PER_CLIENT):
                    logSplunk({"Upload Mbps": str(clientsData[clusterName]['speed']), "Cluster": clusterName})
                    clientsData[clusterName]['testCount'] = 0
                    print("Speed for cluster " + str(clusterName) + " is: " + str(clientsData[clusterName]['speed']))

def main():
    uploadTest()

if __name__ == "__main__":
    main()
