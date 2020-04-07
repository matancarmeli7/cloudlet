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

def speedtest(URL, initialCheck, times):

    speeds = []
    bad_tests = 0

    for i in range(times):
	print i
        # Issue an http get request while timing it
        start = time.time()
        response = requests.get(url = URL, verify=False)
        end = time.time()

        final_time = end - start
	     
        # If a test takes less then 5 seconds return 0 for bad size for test    
        if final_time < 5 and initialCheck:
            bad_tests = bad_tests + 1

	# Transfer Bytes to Megabits per second
	size = float(len(response.content))/1000/1000
	Mbps = size/final_time*8
	
	speeds.append(Mbps)

    if bad_tests:
        return 0

    # Getting the slowest result
    Mbps = min(speeds)
    return Mbps

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
	print size
	# Getting the slowest result and logging splunk
	Mbps = speedtest(size, initialCheck, 10)

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
