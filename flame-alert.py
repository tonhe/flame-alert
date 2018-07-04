#!/usr/bin/env python3
import requests
import csv
from collections import deque
from math import floor
from twilio.rest import Client
import time

COOKID='123456' # FlameBoss Cook ID
MEAT_ALARM=190  # Meat "Done" Temp in F
PIT_ALARM_HIGH=250 # Pit too hot temp 
PIT_ALARM_LOW=210  # Pit too cold temp
TWILO_SID='xxxxxxxxxxxxxxxx'
TWILO_TOKEN='xxxxxxxxxxxxxxxx'
SMS_SRC='+5555555555' # Twilo Phone Number
SMS_DST='+5555555555' # Send SMS alert to ...
SLEEP_INT=60 # How long between updates

def temp_to_f (foo):
	#((2 * c + 5) * 9 / 100) + 32;
	return floor((((2 * int(foo) + 5) * 9 / 100) + 32))
	
def CheckMyMeat():
	URL='https://myflameboss.com/cooks/' + COOKID + '/raw'
	webpage = requests.get(URL, stream=True)
	last_update = deque(csv.reader(webpage.text.splitlines()), 1)[0]
	#time,set_temp,pit_temp,meat_temp1,meat_temp2,meat_temp3,duty_cycle
	# 0  , 1      , 2      , 3        , 4        , 5        , 6
	MEAT0_TEMP = temp_to_f(last_update[3])
	PIT_TEMP = temp_to_f(last_update[2])
	if 	PIT_TEMP >= PIT_ALARM_HIGH:
		print ("Pit Temp too HIGH (Currently at %iºF) Sending SMS" % PIT_TEMP)
		client = Client(TWILO_SID, TWILO_TOKEN)
		client.messages.create(to=SMS_DST, 
                       		   from_=SMS_SRC,
		                       body="Pit Temp too HIGH %iºF" % PIT_TEMP)
	if 	PIT_TEMP <= PIT_ALARM_LOW:
		print ("Pit Temp too LOW (Currently at %iºF) Sending SMS" % PIT_TEMP)
		client = Client(TWILO_SID, TWILO_TOKEN)
		client.messages.create(to=SMS_DST, 
		                       from_=SMS_SRC, 
		                       body="Pit Temp too LOW %iºF" % PIT_TEMP)
	if 	MEAT0_TEMP >= MEAT_ALARM:
		print ("Meat Done! Currently at %iºF -- Sending SMS" % MEAT0_TEMP)
		client = Client(TWILO_SID, TWILO_TOKEN)
		client.messages.create(to=SMS_DST, 
		                       from_=SMS_SRC, 
		                       body="Meat Done! - Currently at %iºF" % MEAT0_TEMP)
	else:
		print ("Currently at %iºF / %iºF - Checking again in %i seconds." % (MEAT0_TEMP,MEAT_ALARM,SLEEP_INT))
	
if __name__ == "__main__": #############################################################
	while True:
		CheckMyMeat()
		time.sleep(SLEEP_INT)
	print ('fin')
