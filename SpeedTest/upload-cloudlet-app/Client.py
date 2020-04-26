import socket
import sys
import time
import schedule
import ssl

HOST = '52.154.154.164'
#HOST = 'speedtest-upload.apps.ocp43-test.sales.lab.tlv.redhat.com'
PORT = 30037
SECONDS_FOR_TEST = 5
AMOUNT_OF_TESTS = 6
TESTS_INTERVAL = 5

def uploadCheck():

    # Run the upload test AMOUNT_OF_TESTS times
    for i in range(0,AMOUNT_OF_TESTS):

        # Create a client socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)

        client.connect((HOST, PORT))

        #client = ssl.wrap_socket(client, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE,
        #                    ssl_version=ssl.PROTOCOL_SSLv23)

        # Create e message of 1 KB
        message = "a" * 1024

        # First send the cluster name
        client.send("Cluster5-4-3\0".encode())

        startTime = time.time()
        amountSent = 0
        # Send 1MB of data for 5 seconds
        while ((time.time() - startTime) < SECONDS_FOR_TEST):
            client.send(message.encode())
            amountSent += 1
            print(str(amountSent))
            time.sleep(1)
        client.close()


def main():
    uploadCheck()
    schedule.every(TESTS_INTERVAL).minutes.do(uploadCheck)

    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == "__main__":
  main()
