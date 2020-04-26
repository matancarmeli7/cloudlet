import socket
import sys
import time
import schedule
import ssl
import os

HOST = os.environ['UPLOAD_HOST']
PORT = int(os.environ['PORT'])
SECONDS_FOR_TEST = int(os.environ['TEST_LENGTH'])
AMOUNT_OF_TESTS = int(os.environ['TESTS_AMOUNT'])
TESTS_INTERVAL = int(os.environ['TESTS_INTERVAL'])
KB_CHUNKS_NUM = int(os.environ['KB_CHUNKS'])

def uploadCheck():
    

    # Run the upload test AMOUNT_OF_TESTS times
    for i in range(0,AMOUNT_OF_TESTS):
        # Create a client socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)

        client.connect((HOST, PORT))
        
        # Create e message of KB_CHUNKS_NUM KB
        message = "a" * 1024 * KB_CHUNKS_NUM

        # First send the cluster name
        client.send("ClusterInside\0".encode())

        startTime = time.time()
        amountSent = 0
        
        # Send data for 5 seconds
        while ((time.time() - startTime) < SECONDS_FOR_TEST):
            client.send(message.encode())
            amountSent += KB_CHUNKS_NUM
        
        client.close()
        print("Test number " + str(i) + ", sent: " + str(amountSent) + "KB")

def main():
    uploadCheck()
    schedule.every(TESTS_INTERVAL).minutes.do(uploadCheck)

    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == "__main__":
  main()
