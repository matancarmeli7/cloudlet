import requests
import time
import schedule

# File to donwload for the test
url = "http://speedtest-cloudapp-http.apps.ocp43-prod.cloudlet-dev.com/100MB.bin"

splunk_TOKEN = "0dde0859-27ff-43aa-b981-3eaca4fa4813"

# Log to central Splunk
def logSplunk(log, TOKEN):
    url = 'https://13.90.23.80:8088/services/collector/event'
    myobj = {"event": log}
    x = requests.post(url, json = myobj, auth=('Splunk', TOKEN), verify=False)

speeds = []

def speedtest():
	# Loop 10 times for minimum result
	for i in range(10):
	    # Issue an http get request while timing it
	    start = time.time()
	    response = requests.get(url)
	    end = time.time()

	    final_time = end - start

	    # Transfer Bytes to MegaBytes
	    size = float(len(response.content))/1000/1000

	    # Adding Mbps to list while transfering Bytes to Bits
	    speeds.append(size/final_time*8)

	# Getting the slowest result and logging splunk
	Mbps = min(speeds)
	logSplunk({"Mbps: ": Mbps}, splunk_TOKEN)
        print "Mbps: {}".format(Mbps)

def main():
        speedtest()
        schedule.every(5).minutes.do(speedtest)

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    main()
