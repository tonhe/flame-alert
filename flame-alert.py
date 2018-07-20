#!/usr/bin/env python3
import requests
import csv
from collections import deque
from math import floor
import time

COOKID='12345' # FlameBoss Cook ID
MEAT_ALARM=190  # Meat "Done" Temp in F
PIT_ALARM_HIGH=250 # Pit too hot temp
PIT_ALARM_LOW=210  # Pit too cold temp

# Probably Don't have to touch these...
PIT_ALARM_VARIENCE=20 # Allow pit to fluctuate 20F
SLEEP_INT=60 # How long between updates
FB_RAW_URL=f'https://myflameboss.com/cooks/{COOKID}/raw'

# IFTTT Webhook Config
IFTTT_WEBHOOK_EVENT='msg'
IFTTT_WEBHOOK_KEY='xxxxxxxxxx'

# FlameBoss CSV Indexes
PIT_SET_TEMP_INDEX=1
PIT_TEMP_INDEX=2
MEAT1_TEMP_INDEX=3
MEAT1_TEMP_INDEX=4 # Not used
MEAT2_TEMP_INDEX=5 # Not used


def temp_to_f (foo): # Convert data from FlameBoss to Fahrenheit
	return floor((((2 * int(foo) + 5) * 9 / 100) + 32))


def do_alert(msg): # Generates IFTTT Alert using Webhooks + SMS
 	report = {}
 	report[“value1”] = msg
	webhook_url=f'https://maker.ifttt.com/trigger/{IFTTT_WEBHOOK_EVENT}/with/key/{IFTTT_WEBHOOK_KEY}'
	requests.post(webhook_url, data=report)


def CheckMyMeat(): # the main event....
	raw = requests.get(FB_RAW_URL, stream=True)
	last_update = deque(csv.reader(raw.text.splitlines()), 1)[0]

	PIT_SET_TEMP = temp_to_f(last_update[PIT_SET_TEMP_INDEX])
	PIT_TEMP = temp_to_f(last_update[PIT_TEMP_INDEX])
	MEAT1_TEMP = temp_to_f(last_update[MEAT1_TEMP_INDEX])

	if 	PIT_TEMP >= (PIT_SET_TEMP + PIT_ALARM_VARIENCE):
		print (f"Pit Temp too HIGH - Currently at {PIT_TEMP}ºF / {PIT_SET_TEMP}ºF - Sending SMS")
		do_alert(f"Pit Temp too HIGH {PIT_TEMP}ºF / {PIT_SET_TEMP}ºF")
	elif 	PIT_TEMP <= (PIT_SET_TEMP - IT_ALARM_VARIENCE):
		print (f"Pit Temp too LOW - Currently at {PIT_TEMP}ºF / {PIT_SET_TEMP}ºF - Sending SMS")
		do_alert(f"Pit Temp too LOW {PIT_TEMP}ºF / {PIT_SET_TEMP}ºF")

	if 	MEAT1_TEMP >= MEAT_ALARM:
		print (f"Meat Done! - Current temp {MEAT1_TEMP}ºF - Sending SMS")
		do_alert(f"Meat Done! - Current temp {MEAT1_TEMP}ºF")
	else:
		print (f"Currently at {MEAT1_TEMP}ºF / {MEAT_ALARM}ºF - Checking again in {SLEEP_INT} seconds.")


if __name__ == "__main__": #############################################################
	while True:
		CheckMyMeat()
		time.sleep(SLEEP_INT)
	print ('fin') # Script ended....
