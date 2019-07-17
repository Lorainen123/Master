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
bufred = np.zeros((N,))
bufsol = np.zeros((N,))
bufbat = np.zeros((N,))
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
Itotal=0

#Configuration pin output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Low current sensors configurations
try:
    ina = INA219(shunt_ohms=0.1,
                 max_expected_amps = 2.0,
                 address=0x40)

    ina1 = INA219(shunt_ohms=0.1,
                 max_expected_amps = 2.0,
                 address=0x44)

    ina2 = INA219(shunt_ohms=0.1,
                 max_expected_amps = 2.0,
                 address=0x41)

    ina3 = INA219(shunt_ohms=0.1,
                 max_expected_amps = 2.0,
                 address=0x45)

    ina.configure(voltage_range=ina.RANGE_32V,
                  gain=ina.GAIN_AUTO,
                  bus_adc=ina.ADC_128SAMP,
                  shunt_adc=ina.ADC_128SAMP)

    ina1.configure(voltage_range=ina.RANGE_32V,
                  gain=ina.GAIN_AUTO,
                  bus_adc=ina.ADC_128SAMP,
                  shunt_adc=ina.ADC_128SAMP)

    ina2.configure(voltage_range=ina.RANGE_32V,
                  gain=ina.GAIN_AUTO,
                  bus_adc=ina.ADC_128SAMP,
                  shunt_adc=ina.ADC_128SAMP)

    ina3.configure(voltage_range=ina.RANGE_32V,
                  gain=ina.GAIN_AUTO,
                  bus_adc=ina.ADC_128SAMP,
                  shunt_adc=ina.ADC_128SAMP)
except:
    time.sleep(0.1)



def adquisicion1 (i):
	global sw,S_2, PRtotal, PStotal, S_4, S_5

	while True:     
		## Potencia de la red
		pred = ina.power()/1000
        	pred1 = ina1.power()/1000
     		pred2 = ina2.power()/1000
        	pred3 = ina3.power()/1000
		PRtotal=pred+pred1+pred2+pred3
		PRtotal=round(PRtotal,3)
		
		
		#tic = tm.default_timer()
		A2 = mcp.read_adc(7)  ## Corriente del panel solar
		S_2m=((A2)*(5.15/1023))
		S_2=(-25.3+10*S_2m)-0.2
		
		V1 = mcp.read_adc(4)
		V1 = V1*(5.15/1023)*(37.5/7.5)  ## voltaje del panel solar
 		PStotal=S_2*V1 ## potencia del panel solar
		#toc = tm.default_timer()
    		
		
		## potencia de la bateria
		
		A4 = mcp.read_adc(1)  ## corriente de la bateria
		S_4m=(A4*(5.15/1023))
    		#S_4=-25.3+10*S_4m
		S_4=43.4613-47.717*S_4m + 12.0923*S_4m*S_4m
		V2 = mcp.read_adc(5)
		S_7 = (V2*(5.15/1023))*(37.5/7.5) ##voltaje de la bateria
		
		##potencia de la carga
		
		V3 = mcp.read_adc(6)
		S_8 = ((V3)*(5.15/1023))*(37000.0/7500.0) 
   	        A5 = mcp.read_adc(0)
		S_5m=((A5)*(5.15/1023))
   		S_5=-25.3+10*S_5m

		
		sw=1
		time.sleep(0.00080)
		
		#print(toc-tic)
		#g=g+1
		
		#print("Potencia del panel = "+Pp)
		#print("Voltaje del panel = "+Vpanel)
	
	#A2=A2/20
	
def powerred(i):
	global Ptotal
	
	while True:
		#tic = tm.default_timer()
        	pred = ina.power()/1000
        	pred1 = ina1.power()/1000
     		pred2 = ina2.power()/1000
        	pred3 = ina3.power()/1000
		Ptotal=pred+pred1+pred2+pred3
		Ptotal=round(Ptotal,3)
		time.sleep(0.00080)
		#toc = tm.default_timer()
		#print(ired1)
		
  

def main():
	global sw, PRtotal, PStotal
	i=1
	thread.start_new_thread(adquisicion1,(i,))
	#thread.start_new_thread(adquisicion2,(i,))
	while True:
		
		#tic = tm.default_timer()
		time.sleep(0.00000050)
		if sw==1: #dato nuevo 
			#print(A2)
			
			bufred[1:N]=bufred[0:N-1]
			bufred[0]=PRtotal
			pred=np.mean(bufred)
			pred=6.8807+1.06223*pred+0.00221977*pred*pred
			
			bufsol[1:N]=bufsol[0:N-1]
			bufsol[0]=PStotal
			psol=np.mean(bufsol)
			
			bufbat[1:N]=bufbat[0:N-1]
			bufbat[0]=S_4
			pbat=np.mean(bufbat)
			
			bufload[1:N]=bufload[0:N-1]
			bufload[0]=S_5
			pload=np.mean(bufload)
			sw=0
			#toc = tm.default_timer()
			#print(toc-tic)
			print(pload)
			
			
		#print(Itotal)
		

main()
	
	
