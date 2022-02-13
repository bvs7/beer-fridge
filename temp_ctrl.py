#!/usr/bin/env python3
#
# Run the temperature control program and output the temperature to a csv file
#
#
# Changelog:
#   2.2 Added quick temp ramp
#   2.1 - Records temperature in a csv
#   2.0 - Successfully checks temperature and turns on and off fridge
#
#   1.0 - Created program

import time
import Adafruit_MCP9808.MCP9808 as MCP9808
import RPi.GPIO as GPIO
import csv
from datetime import datetime
from numpy import mod

UPPER_LIMIT = 53 # F
LOWER_LIMIT = 50 # F

CHECK_PERIOD = 1 # sec
RECORD_PERIOD = 10 # sec

RECORD_CSV = False # If true, will record data in csv file

def run():

	UPPER_LIMIT = 68 # F
	LOWER_LIMIT = 66 # F

	print("Would run temp_ctrl now if it were implemented....")
	sensor = MCP9808.MCP9808()

	sensor.begin()

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(4,GPIO.OUT)
	fridge_on = True
	GPIO.output(4, GPIO.HIGH)

	#record_counter = 0 # Use this as a sloppy way to determine when to record

	#INCREMENT_HOUR = mod((datetime.now().timetuple()[3] + 1), 24) #Determine an hour to increment based on current time

        #Uncomment for temp ramp and uncomment some lines down in next function
"""
        while True:
		temp = sensor.readTempC() * 9.0 / 5.0 + 32.0
		timestamp = time.time()
		
		print("Temp: {}".format(temp))
		if not fridge_on:
			if temp > UPPER_LIMIT:
				if __name__ == "__main__":
					print("FRIDGE ON")
					fridge_on = True
					GPIO.output(4, GPIO.HIGH)
		else:
			if temp < LOWER_LIMIT:
				if __name__ == "__main__":
					print("FRIDGE OFF")
					fridge_on = False
					GPIO.output(4, GPIO.LOW)
		
		#Used to decrement fridge temp by 6 F every 12 hours until it hits 68 F
		print(datetime.now())
		print(INCREMENT_HOUR)
		if(LOWER_LIMIT > 32): #Don't want to freeze
			if(INCREMENT_HOUR == datetime.now().timetuple()[3]):
				LOWER_LIMIT -= 1
				UPPER_LIMIT -= 1
				INCREMENT_HOUR = mod((INCREMENT_HOUR + 2), 24) #Wait another 3 hours before increasing the temperature
				print("TEMPERATURE DECREASED")
				print("UPPER LIMIT: " + str(UPPER_LIMIT))
				print("LOWER LIMIT: " + str(LOWER_LIMIT))
        	
			
"""
#Uncomment for record of temps. Needs work.

"""
        record_counter -= CHECK_PERIOD
	if record_counter <= 0:
		while record_counter <= 0:
			record_counter += RECORD_PERIOD
			if RECORD_CSV:
				with open("fridge_temp_data.csv","a") as datafile:
					writer = csv.DictWriter(datafile, ("time","temp","fridge on"))
					writer.writerow({"time":timestamp,"temp":temp, "fridge on":fridge_on})
		
"""
	

if __name__ == "__main__":
    run()
    UPPER_LIMIT = 54 # F
    LOWER_LIMIT = 50 # F

    print("Would run temp_ctrl now if it were implemented....")
    sensor = MCP9808.MCP9808()

    sensor.begin()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4,GPIO.OUT)

    # Initialize fridge state
    fridge_on = GPIO.input(4)

    record_counter = 0 # Use this as a sloppy way to determine when to record

    while True:
        temp = sensor.readTempC() * 9.0 / 5.0 + 32.0
        timestamp = time.time()
        print(datetime.now())
        print("Temp: {}, Fridge On?: {}".format(temp,fridge_on))
        if not fridge_on:
            if temp > UPPER_LIMIT:
                if __name__ == "__main__":
                    print("FRIDGE ON")
                fridge_on = True
                GPIO.output(4, GPIO.HIGH)
        else:
            if temp < LOWER_LIMIT:
                if __name__ == "__main__":
                    print("FRIDGE OFF")
                fridge_on = False
                GPIO.output(4, GPIO.LOW)
        #UNCOMMENT HERE FOR TEMP RAMP
        #Used to increment fridge temp by 5 F every 12 hours until it hits 68 F
        #INCREMENT_HOUR = mod((datetime.now().timetuple()[3] + 3), 24) #Determine an hour to increment based on current time
        #if(UPPER_LIMIT < 68): #Don't want to exceed 68 F
            #if(INCREMENT_HOUR == datetime.now().timetuple()[3]):
                #LOWER_LIMIT += 1.25
                #UPPER_LIMIT += 1.25
                #INCREMENT_HOUR = mod((INCREMENT_HOUR + 3), 24) #Wait another 3 hours before increasing the temperature
                #print("TEMPERATURE INCREASED")
                #print("UPPER LIMIT: " + str(UPPER_LIMIT))
                #print("LOWER LIMIT: " + str(LOWER_LIMIT))

        record_counter -= CHECK_PERIOD
        if record_counter <= 0:
            while record_counter <= 0:
                record_counter += RECORD_PERIOD
            if RECORD_CSV:
                with open("fridge_temp_data.csv","a") as datafile:
                    writer = csv.DictWriter(datafile, ("time","temp","fridge on"))
                    writer.writerow({"time":timestamp,"temp":temp, "fridge on":fridge_on})
        time.sleep(CHECK_PERIOD)

if __name__ == "__main__":
    run()
