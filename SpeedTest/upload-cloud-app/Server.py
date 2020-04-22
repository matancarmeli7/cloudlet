import socket
import sys
import time
import requests

PORT = 8000
KB_CHUNKS = 16
SPLUNK_TOKEN = "0dde0859-27ff-43aa-b981-3eaca4fa4813"
SPLUNK_URL = "https://13.90.23.80:8088/services/collector/event"
TESTS_PER_CLIENT = 6

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
    print("Debug")
    # Listen forever
    while True:
        # Save if the current client finished successfully
        finishedSuccessfully = True;

        try:
            print("Debug 2")
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = sock.accept()

            start = time.time()

            # Init counter variables
            dataAmount = 0
            end = 0

            print('connection from: ' + str(client_address))

            # The first 20 characters will be the cluster name
            clusterName = connection.recv(20).decode()

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
