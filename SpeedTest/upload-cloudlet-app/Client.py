import socket
import sys
import time
import schedule

HOST = 'localhost'
PORT = 8000
SECONDS_FOR_TEST = 5
AMOUNT_OF_TESTS = 6
TESTS_INTERVAL = 1

def uploadCheck():

    # Run the upload test AMOUNT_OF_TESTS times
    for i in range(0,AMOUNT_OF_TESTS):

        # Create a client socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((HOST, PORT))

        # Create e message of 1 MiB
        message = "a" * 1024 * 1024

        # First send the cluster name
        client.send("Cluster5-4-3\0".encode())

        startTime = time.time()

        # Send 1MB of data for 5 seconds
        while ((time.time() - startTime) < SECONDS_FOR_TEST):
            client.send(message.encode())
        client.close()


def main():
    uploadCheck()
    schedule.every(TESTS_INTERVAL).minutes.do(uploadCheck)

    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == "__main__":
  main()
