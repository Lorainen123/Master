import Node611
import excel
import mcpras 
import time
import numpy as np
import thread


i=0
v=14.5
archivo=open("prueba1.txt","w")
itotal=0
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
    

def adquisicion2(i):
  
	  global itotal
	
	  while True:
      
	
                 	ired = ina.current()/1000
        	        ired1 = ina1.current()/1000
     		        ired2 = ina2.current()/1000
                 	ired3 = ina3.current()/1000
	              	itotal=ired+ired1+ired2+ired3
              		itotal=round(itotal,3)
		


def main():
	global itotal
	thread.start_new_thread(adquisicion2,(i,))
	while i<41:
  
   
    		n = excel.main(float(v+0.1*i),0)
   		n = int(n)
    		mcpras.set_value(n)
    		time.sleep(1)
   # P1=Node611.sensorm()
     
    		archivo.write(str(itotal)+'\n')
   
    
 #   n = excel.main(float(16.2),0)
 #   n = int(n)
 #   mcpras.set_value(n)
 #   time.sleep(1)
 #   P1=Node611.sensorm()
 #   archivo.write(str(P1)+'\n')
   		 i=i+1
    
main()  
archivo.close()

                  
