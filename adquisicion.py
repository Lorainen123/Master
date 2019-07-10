import numpy as np
from math import *
import time
from time import sleep
import serial
import requests
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI
from ina219 import INA219
import RPi.GPIO as GPIO
import thread
import timeit as tm

#Configuration SPI Port and device
SPI_PORT   = 0
SPI_DEVICE = 0
sw=0
buf = np.zeros((10,))
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Configuration pin output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


def adquisicion (i):
	global sw,S_2
	while i==1:     
		tic = tm.default_timer()
		A2 = mcp.read_adc(7)
		V2 = mcp.read_adc(5)
    		#Value for zero adjustment of the sensors
    		#Conversion of digital value to analog
    		#current sensors	
	
		S_2m=((A2)*(5.15/1023))
		S_2=-25.3+10*S_2m
		
   		 #voltage sensors
   		S_7 = ((V2)*(5.15/1023))*(37.5/7.5)
	
    		#Calculation of panel voltage
    		Vpanel=1.1+S_7
   		 #Power of the panel
		#Pp = Vpanel*S_2
		time.sleep(0.00988)
		toc = tm.default_timer()
    
   		 #Power of the battery
   
		#print(S_2)
		#print(toc-tic)
		sw=1
		#print("Potencia del panel = "+Pp)
		#print("Voltaje del panel = "+Vpanel)
  

def main():
	global sw
	i=1
	thread.start_new_thread(adquisicion,(i,))
	while True:
		if sw==1: #dato nuevo 
			buf[0]=S_2
			buf[1:N]=buf[0:N-1]
			
		else: 
			print("esperando dato")
	
	

main()
	
	
