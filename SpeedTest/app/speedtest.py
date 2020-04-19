import requests
import time
import schedule
import os
import socket

# Define needed variables
main_url = os.environ['MAIN_APP_URL']
token = os.environ['SPLUNK_TOKEN']
splunk_url = os.environ['SPLUNK_URL']
min_check_time = os.environ['MIN_CHECK_TIME']


# Files to download for the test
f_1MB = main_url + "/1MB.bin"
f_10MB = main_url + "/10MB.bin"
f_100MB = main_url + "/100MB.bin"
f_500MB = main_url + "/500MB.bin"
f_1000MB = main_url + "/1000MB.bin"


# Log to central Splunk
def logSplunk(log, TOKEN):
  myobj = {"event": log}
  x = requests.post(splunk_url, json = myobj, auth=('Splunk', TOKEN), verify=False)

# Downloading a file multiple times while timing each download, returning lowest speed result.
def speedtest(URL, initialCheck, times):

  speeds = []
  bad_tests = 0

  for i in range(times):
    # Issue an http get request while timing it
    start = time.time()
    response = requests.get(url = URL, verify=False)
    end = time.time()

    final_time = end - start

    # If a test takes less then min_check_time return 0 for bad size for test    
    if final_time < min_check_time and initialCheck:
      bad_tests += 1

	# Transfer Bytes to Megabits per second
  size = float(len(response.content))/1000/1000
  Mbps = (size/final_time)*8
	
  speeds.append(Mbps)

  # If all the tests were bad
  if bad_tests == times:
    return 0

  # Getting the slowest result
  Mbps = min(speeds)
  return Mbps

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
	Mbps = speedtest(size, initialCheck, 10)
  
	logSplunk({"Mbps" : Mbps, "Cluster": "cloudlet-ocp43-prod"}, token)
  print "Mbps: {}".format(Mbps)

hostname = socket.gethostname()

#Run checks function every 6 min
def main():
  checks()
  schedule.every(3).minutes.do(checks)

  while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
  main()
