import spidev
import os
import sys
from math import *
import time
from time import sleep
import serial
import requests
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI
from ina219 import INA219
import RPi.GPIO as GPIO


#Configuration SPI Port and device
SPI_PORT   = 0
SPI_DEVICE = 0
Sw=0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
#Configuration pin output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
a=0
t=0
#Cycle for to take measures
vr=True

    #Initialization of sensors
    
      #Reading of each adc channel
A1 = mcp.read_adc(2)
A2 = mcp.read_adc(7)
A3 = mcp.read_adc(3)
A4 = mcp.read_adc(1)
A5 = mcp.read_adc(0)
V1 = mcp.read_adc(4)
V2 = mcp.read_adc(5)
V3 = mcp.read_adc(6)
       
     #Sum of each measure
     
   

    #Value for zero adjustment of the sensors
    
    #Conversion of digital value to analog
    #current sensors	
S_1m = ((A1)*(5.15/1023))
S_1=-25.3+10*S_1m

S_2m=((A2)*(5.15/1023))
S_2=-25.3+10*S_2m
S_2=round(S_2,3)
 
S_3m=((A3)*(5.15/1023))
S_3=-25.3+10*S_3m
 
S_4m=((A4)*(5.15/1023))
S_4=-25.3+10*S_4m
    
S_5m=((A5)*(5.15/1023))
S_5=-25.3+10*S_5m
    
    #voltage sensors
S_6_temp = ((V2)*(5.15/1023))
S_6 = 5.936*(S_6_temp-3.155)+32.8
    
S_7 = ((V2)*(5.15/1023))*(37.5/7.5)
S_7 = round(S_7,3)
    
S_8 = ((V3)*(5.15/1023))*(37000.0/7500.0)      

    #Calculation of panel voltage
    #Vp = ((2.5+S_2*0.1)*6)
Vp=round(0.0326*log(S_2)+0.7812,3)
Vpanel=1.1+S_7
    #Power of the panel
Pp = round((Vpanel)*S_2,3)
    #Calculation of battery current
Ib = S_5-S_3+S_4
    
if(Ib<=0.5):
	Ib=0.0001
    #Power of the battery
vbatt=round(0.0326*log(Ib)+0.7812,3)
Pb = str(round((vbatt)*Ib,2))
    #Conversion to string
Vpanel=str(Vpanel)
S_1=str(round(S_1,2))
S_2=str(round(S_2,1))
S_3=str(round(S_3,2))
S_4=str(round(S_4,2))
S_5=str(round(S_5,2))
S_6=str(round(S_6,2))
S_7=str(round(S_7,3))
S_8=str(round(S_8,2))
    #Print values of each sensor
    #Sensors viewed from left to right and from bottom to top
    #print("Corriente sensor 1 = "+i)   ## Sensor de corriente 1 de I2C
    #print("Corriente sensor 2 = "+i1)	## Sensor de corriente 2 de I2C
    #print("Corriente sensor 3 = "+i2)	## Sensor de corriente 3 de I2C
    #print("Corriente sensor 4 = "+i3)	## Sensor de corriente 4 de I2C

    #print("Voltaje sensor 1 = "+S_6)	## Sensor 1 de ADC  Canal 4
    #print("Corriente sensor 5 = "+S_1)	## Sensor 2 de ADC  Canal 2
print("Corriente sensor panel solar = "+S_2)	## Sensor 3 de ADC  Canal 7
    #print("Voltaje sensor 2 = "+S_7)	## Sensor 4 de ADC  Canal 5
    #print("Corriente sensor 7 = "+S_3)	## Sensor 5 de ADC  Canal 3
    #print("Corriente sensor 8 = "+S_4)	## Sensor 6 de ADC  Canal 1
    #print("Corriente sensor 9 = "+S_5)	## Sensor 7 de ADC  Canal 0
    #print("Voltaje sensor 3 = "+S_8)	## Sensor 8 de ADC  Canal 6
    #print("Potencia de la fuente = "+Pf)
print("Potencia del panel = "+Pp)
print("Voltaje del panel = "+Vpanel)
print("Voltaje de referencia = "+v)
    #print("Potencia de la bateria = "+Pb)
  
	
  #  vr=not vr
 #   time.sleep(0.01)

