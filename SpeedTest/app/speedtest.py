import requests
import time
import schedule

# Files to donwload for the test
f_1MB = "http://speedtest-cloudapp-http.apps.ocp43-prod.cloudlet-dev.com/1MB.bin"
f_10MB = "http://speedtest-cloudapp-http.apps.ocp43-prod.cloudlet-dev.com/10MB.bin"
f_100MB = "http://speedtest-cloudapp-http.apps.ocp43-prod.cloudlet-dev.com/100MB.bin"
f_500MB = "http://speedtest-cloudapp-http.apps.ocp43-prod.cloudlet-dev.com/500MB.bin"
f_1000MB = "http://speedtest-cloudapp-http.apps.ocp43-prod.cloudlet-dev.com/1000MB.bin"

splunk_TOKEN = "0dde0859-27ff-43aa-b981-3eaca4fa4813"

# Log to central Splunk
def logSplunk(log, TOKEN):
    url = 'https://13.90.23.80:8088/services/collector/event'
    myobj = {"event": log}
    x = requests.post(url, json = myobj, auth=('Splunk', TOKEN), verify=False)

<<<<<<< HEAD
def speedtest(URL, last):
    # Issue an http get request while timing it
    start = time.time()
    response = requests.get(url = URL, verify=False)
    end = time.time()

    final_time = end - start
     
    # If a test takes less then 5 seconds return 0 for bad size for test
    
    if final_time < 5 and not last:
        return 0

    # Transfer Bytes to Megabits per second
    size = float(len(response.content))/1000/1000
    Mbps = size/final_time*8

    return Mbps

def checks():

        last = False

	Mbps = speedtest(f_1MB, last)
        if Mbps:
            size = f_1MB
        else:
            Mbps = speedtest(f_10MB, last)
            if Mbps:
                size = f_10MB
            else:
                Mbps = speedtest(f_100MB, last)
                if Mbps:
                    size = f_100MB
                else:
                    Mbps = speedtest(f_500MB, last)
                    if Mbps:
                        size = f_500MB
                    else:
                        size = f_1000MB
                        last = True

	speeds = []
	# Loop 10 times for minimum result
	for i in range(10):
            print i    
            # Adding Mbps to list
	    speeds.append(speedtest(size, last))

	# Getting the slowest result and logging splunk
	Mbps = min(speeds)
	logSplunk({"Mbps: ": Mbps}, splunk_TOKEN)
        print "Mbps: {}".format(Mbps)

def main():
        checks()
	schedule.every(6).minutes.do(checks)

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    main()
