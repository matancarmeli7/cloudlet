import requests
import time
import schedule
import os
import socket

# Define needed variables
main_url = os.environ['MAIN_APP_URL']
token = os.environ['SPLUNK_TOKEN']
splunk_url = os.environ['SPLUNK_URL']
min_check_time = int(os.environ['MIN_CHECK_TIME'])
OCP_NAME = os.environ['OCP_NAME']

# Files to download for the test
f_500KB = main_url + "/500KB.bin"
f_1MB = main_url + "/1MB.bin"
f_10MB = main_url + "/10MB.bin"
f_100MB = main_url + "/100MB.bin"
f_500MB = main_url + "/500MB.bin"
f_1000MB = main_url + "/1000MB.bin"


# Log to central Splunk
def logSplunk(log):
  myobj = {"event": log}
  print("Sending the following log to splunk: " + str(log))
  x = requests.post(splunk_url, json = myobj, auth=('Splunk', token), verify=False)

# Downloading a file multiple times while timing each download, returning lowest speed result.
def speedtest(URL, initialCheck, times):

  speeds = []
  bad_tests = 0
  
  print("Started speed test")

  for i in range(times):
    # Issue an http get request while timing it
    start = time.time()
    response = requests.get(url = URL, verify=False)
    end = time.time()

    final_time = end - start

    # If a test takes too much time in an initial test, don't count it    
    if not(final_time < min_check_time and initialCheck):

	    # Transfer Bytes to Megabits per second
      size = float(len(response.content))/1000/1000
      Mbps = (size/final_time)*8
	
      speeds.append(Mbps)
  

  # If all the tests were bad
  if len(speeds) == 0:
    return 0

  print("Finished a download speed test for cluster: " + OCP_NAME + ", speed is: " + str(min(speeds)))
  
  # Getting the slowest result
  return min(speeds)

# Running speedtests scans and logging to splunk
def checks():

  initialCheck = True

  # Chooses the largest file to test with while acting on the network capabilities
  Mbps = speedtest(f_1MB, initialCheck, 2)
  
  if Mbps:
    size = f_1MB
  else:
    Mbps = speedtest(f_10MB, initialCheck, 2)
    if Mbps:
      size = f_10MB
    else:
      Mbps = speedtest(f_100MB, initialCheck, 2)
      if Mbps:
        size = f_100MB
      else:
        Mbps = speedtest(f_500MB, initialCheck, 2)
        if Mbps:
          size = f_500MB
        else:
          size = f_1000MB
 
  initialCheck = False
	
  # Getting the slowest result and sending logs to splunk
  Mbps = speedtest(size, initialCheck, 5)
  
  logSplunk({"Download Mbps" : Mbps, "Cluster": OCP_NAME})
  print ("Download Mbps: " + str(Mbps) + ", Cluster: " + OCP_NAME) 

#Run checks function
def main():
  checks()

if __name__ == "__main__":
  main()
