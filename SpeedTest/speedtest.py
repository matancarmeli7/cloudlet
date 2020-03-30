import requests
import time

speeds = []
url = "https://speed.hetzner.de/100MB.bin"

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

# Getting the slowest result
Mbps = min(speeds)
print "{} Mbps".format(Mbps)
