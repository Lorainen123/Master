
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

#import os.path






#Sensor and I2C configuration
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

#Configuration SPI Port and device
SPI_PORT   = 0
SPI_DEVICE = 0
Sw=0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
#Configuration pin output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
a=0
GPIO.output(20,False)
GPIO.output(26,True)  
t=0
#Cycle for to take measures
vr=True
def sensorm():	
    #Initialization of sensors
    S1 = 0
    S2 = 0
    S3 = 0
    S4 = 0
    S5 = 0
    S6 = 0
    S7 = 0
    S8 = 0
    S_6_temp=0

    t = 0
    while t<800:
	
      
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
      S1 = S1 + A1
      S2 = S2 + A2
      S3 = S3 + A3
      S4 = S4 + A4
      S5 = S5 + A5
      S6 = S6 + V1
      S7 = S7 + V2 
      S8 = S8 + V3

      t = t + 1

    m =100
    #Value for zero adjustment of the sensors
    Aju=4
    #Conversion of digital value to analog
    #current sensors	
    S_1m = ((S1/t)*(5.15/1023))
    S_1=-25.3+10*S_1m

    S_2m=((S2/t)*(5.15/1023))
    S_2=-25.3+10*S_2m
    S_2=round(S_2,1)
 
    S_3m=((S3/t)*(5.15/1023))
    S_3=-25.3+10*S_3m
 
    S_4m=((S4/t)*(5.15/1023))
    S_4=-25.3+10*S_4m
    
    S_5m=((S5/t)*(5.15/1023))
    S_5=-25.3+10*S_5m
    
    #voltage sensors
    S_6_temp = ((S6/t)*(5.15/1023))
    S_6 = 5.936*(S_6_temp-3.155)+32.8
    
    S_7 = ((S7/t)*(5.15/1023))*(37.5/7.5)
    S_7 = round(S_7,1)
    
    S_8 = ((S8/t)*(5.15/1023))*(37000.0/7500.0)      
 

   #Condition that Current sensor of the first buck is zero, the voltage of the sources is zero
   
   # if(S_1<0.5 or S_2<0.5):
   #     Sw = 0
   # if(S_1>0.5 or S_2>0.5):
   #     Sw = 1
    #Condition for disconnection of non-essential load
    #If the current sensor values of the first buck and the solar panel
    # are lower than a set value and the inverter sensor current is greater than a set value
    #you must disconnect the non-essential load
   # if ( (S_5-S_3)>0.5 and Sw==0):
   #	    GPIO.output(16, False)
   #	    print("Carga desconectada")
   #	    ctrl=str(0)
    #If the current sensor values of the first buck or solar panel are higher
    #than a set value and the inverter sensor current is greater than a set value,
    #you must disconnect the non-essential load
   # elif ((S_5-S_3)<0.5 and Sw==1): 
   #	    GPIO.output(16, True)
   #	    print("Carga conectada")
   #	    ctrl=str(1)

   
    #Verification of charge current for the battery.Charging mode
   # if (S_4>=0.35):
     #   GPIO.output(20, True)
     #   GPIO.output(26, False)
    #Condition for change of charging mode to bypass mode
   # elif (S_4<0.35):
    #    GPIO.output(26, False)
     #   GPIO.output(20, True)
   #	if (S_5-S_3<=0.5):
    #   		GPIO.output(26, False)
    #   		GPIO.output(20, True)
    #Condition for change of bypass mode to charging mode
   # if (S_5-S_3>0.5):
    #    GPIO.output(20, False)
     #   GPIO.output(26, True)
    #Change of currents less than 0 to a value close to 0 but positive


    	
    try:
	
        i = round(ina.current()/1000,2)
        i1 = round(ina1.current()/1000,2)
        i2 = round(ina2.current()/1000,2)
        i3 = round(ina3.current()/1000,2)
	
    except:
        i=0.0
        i1=0.0
        i2=0.0
        i3=0.0
	
    if(i<=0.0):
        i=0.0001
    if(i1<=0.0):
        i1=0.0001
    if(i2<=0.0):
        i2=0.0001
    if(i3<=0.0):
        i3=0.0001
    if(S_1<=0.0):
        S_1=0.0001
    if(S_2<=0.0):
        S_2=0.0001
    if(S_3<=0.0):
        S_3=0.0001
    if(S_4<=0.0):
        S_4=0.0001
    if(S_5<=0.0):
        S_5=0.0001
    #Sum of the currents of each source
    If = i+i1+i2+i3
    #Power of the source
    Pf = str(round(If*S_6,2))
    #Calculation of panel voltage
    #Vp = ((2.5+S_2*0.1)*6)
    Vp=round(0.0326*log(S_2)+0.7812,3)
    Vpanel=1.1+S_7
    #Power of the panel
    Pp = round((Vpanel)*S_2,1)
    #Calculation of battery current
    Ib = S_5-S_3+S_4
    
    if(Ib<=0.5):
         Ib=0.0001
    #Power of the battery
    vbatt=round(0.0326*log(Ib)+0.7812,3)
    Pb = str(round((vbatt)*Ib,2))
    #Conversion to string
    i=str(i)
    i1=str(i1)
    i2=str(i2)
    i3=str(i3)
    Vpanel=str(Vpanel)
    S_1=str(round(S_1,2))
    S_2=str(round(S_2,1))
    S_3=str(round(S_3,2))
    S_4=str(round(S_4,2))
    S_5=str(round(S_5,2))
    S_6=str(round(S_6,2))
    S_7=str(round(S_7,1))
    S_8=str(round(S_8,2))
    #Print values of each sensor
    #Sensors viewed from left to right and from bottom to top
    #print("Corriente sensor 1 = "+i)   ## Sensor de corriente 1 de I2C
    #print("Corriente sensor 2 = "+i1)	## Sensor de corriente 2 de I2C
    #print("Corriente sensor 3 = "+i2)	## Sensor de corriente 3 de I2C
    #print("Corriente sensor 4 = "+i3)	## Sensor de corriente 4 de I2C

    #print("Voltaje sensor 1 = "+S_6)	## Sensor 1 de ADC  Canal 4
    #print("Corriente sensor 5 = "+S_1)	## Sensor 2 de ADC  Canal 2
    #print("Corriente sensor panel solar = "+S_2)	## Sensor 3 de ADC  Canal 7
    #print("Voltaje sensor 2 = "+S_7)	## Sensor 4 de ADC  Canal 5
    #print("Corriente sensor 7 = "+S_3)	## Sensor 5 de ADC  Canal 3
    #print("Corriente sensor 8 = "+S_4)	## Sensor 6 de ADC  Canal 1
    #print("Corriente sensor 9 = "+S_5)	## Sensor 7 de ADC  Canal 0
    #print("Voltaje sensor 3 = "+S_8)	## Sensor 8 de ADC  Canal 6
    #print("Potencia de la fuente = "+Pf)
    #print("Potencia del panel = "+Pp)
    #print("Voltaje del panel = "+Vpanel)
    #print("Voltaje de referencia = "+v)
    #print("Potencia de la bateria = "+Pb)
    return Pp
	
  #  vr=not vr
 #   time.sleep(0.01)

