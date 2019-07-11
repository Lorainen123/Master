import Node611
import excel
import mcpras 
import time
import numpy as np
import thread


i=0
v=14.5
archivo=open("prueba1.txt","w")

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
  
	  global Ired
	
	  while True:
      
	
                 	i = ina.current()/1000
        	        i1 = ina1.current()/1000
     		          i2 = ina2.current()/1000
                 	i3 = ina3.current()/1000
	              	Ired=i+i1+i2+i3
              		Ired=round(Ired,3)
		


    
thread.start_new_thread(adquisicion2,(i,))
while i<41:
  
   
    n = excel.main(float(v+0.1*i),0)
    n = int(n)
    mcpras.set_value(n)
    time.sleep(1)
   # P1=Node611.sensorm()
     
    archivo.write(str(Ired)+'\n')
   
    
 #   n = excel.main(float(16.2),0)
 #   n = int(n)
 #   mcpras.set_value(n)
 #   time.sleep(1)
 #   P1=Node611.sensorm()
 #   archivo.write(str(P1)+'\n')
    i=i+1
    
    
archivo.close()

                  
