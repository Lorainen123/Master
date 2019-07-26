#import Node611
import excel
import mcpras 
import time
import numpy as np
import thread
from ina219 import INA219
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

v=14.5
archivo=open("prueba1.txt","w")
Pred=0
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
    

def adquisicion2(j):
  
	  global Pred
	
	  while True:
      
	
                 	pred = ina.power()/1000   ##se leen los 4 sensores por I2C 
       			pred1 = ina1.power()/1000
     			pred2 = ina2.power()/1000
       			pred3 = ina3.power()/1000
			PRtotal=pred+pred1+pred2+pred3  ## se suma la potencia de cada sensor PRtotal= potencia de la red despues de los rectificadores
			#PRtotal=round(PRtotal,2)
			##potencia de la red
			Pred=round(6.8807+1.06223*PRtotal+0.00221977*PRtotal*PRtotal,3)
		


def main():
	global Pred
	i=0
	thread.start_new_thread(adquisicion2,(i,))
	while i<41:
  
   
    		n = excel.main(float(v+0.1*i),0)
   		n = int(n)
    		mcpras.set_value(n)
    		time.sleep(1)
   # P1=Node611.sensorm()
     
    		archivo.write(str(Pred)+'\n')
   		i=i+1
    
 #   n = excel.main(float(16.2),0)
 #   n = int(n)
 #   mcpras.set_value(n)
 #   time.sleep(1)
 #   P1=Node611.sensorm()
 #   archivo.write(str(P1)+'\n')
   		
    
main()  
archivo.close()

                  
