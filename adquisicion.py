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
N=150
S_2=0
buf = np.zeros((N,))
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Configuration pin output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


def adquisicion (i):
	global sw,S_2

	while True:     
		#tic = tm.default_timer()
		A2 = mcp.read_adc(2)
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
		
		#toc = tm.default_timer()
    		#A2=A2+S_2
   		 #Power of the battery
   		sw=1
		time.sleep(0.00080)
		
		#print(toc-tic)
		#g=g+1
		
		#print("Potencia del panel = "+Pp)
		#print("Voltaje del panel = "+Vpanel)
	
	#A2=A2/20
  

def main():
	global sw
	i=1
	thread.start_new_thread(adquisicion,(i,))
	while True:
		
		#tic = tm.default_timer()
		time.sleep(0.00000050)
		if sw==1: #dato nuevo 
			#print(A2)
			
			buf[1:N]=buf[0:N-1]
			buf[0]=S_2
			me=np.mean(buf)
			sw=0
			#toc = tm.default_timer()
			#print(toc-tic)
			print(me)
			
		#print(sw)
		

main()
	
	
