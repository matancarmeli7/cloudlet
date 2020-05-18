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
num_of_checks = 3

# Files to download for the test
f_1MB = main_url + "1MB.bin"
f_10MB = main_url + "10MB.bin"
f_100MB = main_url + "100MB.bin"
f_500MB = main_url + "500MB.bin"
f_1000MB = main_url + "1000MB.bin"


# Log to central Splunk
def logSplunk(log):
  myobj = {"event": log}
  print("Sending the following log to splunk: " + str(log))
  x = requests.post(splunk_url, json = myobj, auth=('Splunk', token), verify=False)

# Downloading a file multiple times while timing each download, returning lowest speed result.
def speedtest(URL, times):

  speeds = []
  bad_tests = 0
  
  print("Started speed test")

  for i in range(times):
    # Issue an http get request while timing it
    
    start = time.time()
    response = requests.get(url = URL, verify=False)
    end = time.time()

    final_time = end - start


    # If a test takes too little time in an initial test, don't count it    
    if (final_time > min_check_time):

	    # Transfer Bytes to Megabits per second
      size = float(len(response.content))/1000/1000
      Mbps = (size/final_time)*8
	    
      print("Current URL is:" + URL + ", Current test time was: " +  str(final_time) + " And current Mbps is: " + str(Mbps))
      
      speeds.append(Mbps)
  
  # If all the tests were bad
  #if len(speeds) == 0:
    if len(speeds) == 0 or 0 in speeds:
      return 0

  print("Finished a download speed test for cluster: " + OCP_NAME + ", speed is: " + str(min(speeds)))
  
  # Getting the slowest result
  return min(speeds)

# Running speedtests scans and logging to splunk
def checks():

  # Run initial small test to resolve DNS
  Mbps = speedtest(f_1MB, 2)
  
  # Chooses the largest file to test with while acting on the network capabilities
  Mbps = speedtest(f_1MB, num_of_checks)
  
  if not Mbps:
    Mbps = speedtest(f_10MB, num_of_checks)
    if not Mbps:
      Mbps = speedtest(f_100MB, num_of_checks)
      if not Mbps:
        Mbps = speedtest(f_500MB, num_of_checks)
        if not Mbps:
          Mbps = speedtest(f_1000MB, num_of_checks)
 
  logSplunk({"Download Mbps" : Mbps, "Cluster": OCP_NAME})
  print ("Download Mbps: " + str(Mbps) + ", Cluster: " + OCP_NAME) 

#Run checks function every 6 min
def main():
  checks()
  schedule.every(3).minutes.do(checks)

  while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
  main()
