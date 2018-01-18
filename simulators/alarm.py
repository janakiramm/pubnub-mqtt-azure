from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
 
from termcolor import colored
import sys
import signal
import os
import json
from datetime import datetime
alarm_count = 0
run_level = 1
class AlarmCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass
 
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def message(self, pubnub, message):
		global alarm_count
		global run_level
		state = message.message['alarm'].upper()
		
		if (state == "OFF"):
			print colored(str(datetime.now().time().strftime("%H:%M:%S")) +' - No anomaly detected in Fan', 'yellow')
			print colored(str(datetime.now().time().strftime("%H:%M:%S")) +' - Alarm state is OFF' ,'green')
			run_level = 1
			alarm_count = 0
		else:	
			alarm_count = alarm_count + 1
			print colored(str(datetime.now().time().strftime("%H:%M:%S")) +'- Anomaly Detected!', 'red')
			print colored(str(datetime.now().time().strftime("%H:%M:%S")) +'- Alarm count - ' + str(alarm_count),'yellow')
		if (alarm_count >= 5):
			if (run_level == 1):
				print colored('Alarm count exceeded the maximum threshold. Setting the fan run level to 0', 'red')
				publish()
				run_level = 0
				alarm_count = 0
# Replace Pub_Key and Sub_Key with your keys
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "<Sub_Key>"
pnconfig.publish_key = "<Pub_Key>"
pnconfig.ssl = False	
pubnub = PubNub(pnconfig)
pubnub.add_listener(AlarmCallback())
pubnub.subscribe().channels('turbine.alarm').execute()
print('connected')
def signal_handler(signal, frame):
	print("Caught Signal CTRL+C..exiting gracefully")
	sys.exit(0)
def publish():
	pubnub.publish().channel('turbine.command').message({'run':0}).sync()
