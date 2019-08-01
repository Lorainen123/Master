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
#Configuration SPI Port and device
SPI_PORT   = 0
SPI_DEVICE = 0

v=14.5
#archivo=open("prueba1.txt","w")
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
    

def adquisicion2(): 
	try:
		i=0
		ItotalT=0
		while i<5:
			
        		ired = ina.power()/1000
        		ired1 = ina1.power()/1000
     			ired2 = ina2.power()/1000
        		#ired3 = ina3.current()/1000
	      		Itotal=ired+ired1+ired2+ired2
	      		Itotal=round(Itotal,3)
			#Pred=round(6.8807+1.06223*Itotal+0.00221977*Itotal*Itotal,3)
			i=i+1
			ItotalT=ItotalT+Itotal
	except:
			try:
				time.sleep(0.2)
				i=0
				ItotalT=0
				while i<3:
			
        				ired = ina.power()/1000
        				ired1 = ina1.power()/1000
     					ired2 = ina2.power()/1000
        				#ired3 = ina3.current()/1000
	      				Itotal=ired+ired1+ired2+ired2
	      				Itotal=round(Itotal,3)
			#Pred=round(6.8807+1.06223*Itotal+0.00221977*Itotal*Itotal,3)
					i=i+1
					ItotalT=ItotalT+Itotal
			except:
				time.sleep(0.2)
				i=0
				ItotalT=0
				while i<3:
				
        				ired = ina.power()/1000
        				ired1 = ina1.power()/1000
     					ired2 = ina2.power()/1000
        				#ired3 = ina3.current()/1000
	      				Itotal=ired+ired1+ired2+ired2
	      				Itotal=round(Itotal,3)
					Pred=round(6.8807+1.06223*Itotal+0.00221977*Itotal*Itotal,3)
					i=i+1
					ItotalT=ItotalT+Itotal
			
	return ItotalT/5
	


def main():
	#global Pred
	i=0
	#thread.start_new_thread(adquisicion2,(i,))
	while i<41:
  
   
    		n = excel.main(float(v+0.1*i),0)
   		n = int(n)
    		mcpras.set_value(n)
    		time.sleep(0.3)
   # P1=Node611.sensorm()
     		
		try:
			Pred=adquisicion2()
    		
		except:
			time.sleep(0.1)
			Pred=adquisicion2()
			
		print(Pred)	
		#archivo.write(str(Pred)+'\n')
   		i=i+1
    
 #   n = excel.main(float(16.2),0)
 #   n = int(n)
 #   mcpras.set_value(n)
 #   time.sleep(1)
 #   P1=Node611.sensorm()
 #   archivo.write(str(P1)+'\n')
   		
#while True:
#	ired=adquisicion2()
#	print(ired)
main()  
#archivo.close()

                  
