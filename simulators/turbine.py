import time
import requests
import random
import datetime
import calendar
import json
import paho.mqtt.client as mqtt
from termcolor import colored

broker_address = "mqtt.pndsn.com"
run = 1
fault = False #Change this to true to introduce anomaly


def on_message(mosq, obj, msg):
    global run    
    run=json.loads(msg.payload)["run"]
    print colored('Command received with run level:' + str(run),'yellow')
    if(run == 0):
    	print colored('Attempting to stop the fan...','yellow')

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Replace Pub_Key and Sub_Key with your keys
client = mqtt.Client("<Pub_Key>/<Sub_Key>/client1") 
client.on_message = on_message
client.on_subscribe = on_subscribe

client.connect(broker_address)

client.subscribe("turbine/command", 0)

while run == 1:
	d={}
	d["deviceID"] = 1
	d["timeStamp"] = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
	
	if fault == True:		
		d["rotation"] = round(random.uniform(200,400),1)
		d["temperature"] = round(random.uniform(47.0,72.0),1)
		d["vibration"] = round(random.uniform(210.0,320.0),1)
		d["sound"] = round(random.uniform(55.0,75.0),1)
	else:   
		d["rotation"] = round(random.uniform(500,700),1)
		d["temperature"] = round(random.uniform(35.0,45.0),1)
		d["vibration"] = round(random.uniform(100.0,200.0),1)
		d["sound"] = round(random.uniform(45.0,52.0),1)
	
	payload = json.dumps(d, ensure_ascii=False)
	print colored("Fan's run level is 1",'white')
	print colored(payload,'blue')
	client.publish("turbine/message",payload)
	time.sleep(2)
	client.loop()

print colored('Fan stopped','red')
