#import Node611
import excel
import mcpras 
import time
import numpy as np
import thread
from ina219 import INA219
import RPi.GPIO as GPIO
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusSerialClient as ModbusClient




client = ModbusClient(method='rtu', port= '/dev/ttyUSB0', bytesize=8, timeout=1, baudrate= 19200)
if client.connect():
    
    print("puerto abierto")
else:
    print("puerto no abierto")


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#Configuration SPI Port and device
SPI_PORT   = 0
SPI_DEVICE = 0

v=14.5
#archivo=open("prueba1.txt","w")
Predv = np.zeros(5,)
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
		#totalT=0
		while i<5:
			
        		pred_b = ina.power()/1000
        		pred1_b = ina1.power()/1000
     			pred2_b = ina2.power()/1000
        		pred3_b = ina3.power()/1000
	      		Ptotal_b=pred_b+pred1_b+pred2_b+pred2_b
	      		Ptotal_b=round(Ptotal_b,3)
			#print(type(Itotal))
			
			Ptotal_b=6.8807+1.06223*Ptotal_b+0.00221977*Ptotal_b*Ptotal_b
			Predv[i]=Ptotal_b
			#
			#print(Pred[2])
			if i>=1:
				if Predv[i]<0.9*Predv[i-1] or Predv[i]>1.1*Predv[i-1]:
					#print("entre aqui")
					if Predv[i]>Predv[i-1]:
						
						Predv[i]=Predv[i-1]
					else: 
						Predv[i-1]=Predv[i]
			       
			#PtotalT=PtotalT+Pred
			i=i+1
			time.sleep(0.05)
	except:
			try:
				time.sleep(0.2)
				i=0
				PtotalT=0
				while i<5:	
			
        				pred_b = ina.power()/1000
        				pred1_b = ina1.power()/1000
     					pred2_b = ina2.power()/1000
        				pred3_b = ina3.power()/1000
	      				Ptotal_b=pred_b+pred1_b+pred2_b+pred2_b
	      				Ptotal_b=round(Ptotal_b,3)
			#print(type(Itotal))
			
					Ptotal_b=6.8807+1.06223*Ptotal_b+0.00221977*Ptotal_b*Ptotal_b
					Predv[i]=Ptotal_b
			#
			#print(Pred[2])
					if i>=1:
						if Predv[i]<0.9*Predv[i-1] or Predv[i]>1.1*Predv[i-1]:
							#print("entre aqui")
							if Predv[i]>Predv[i-1]:
						
								Predv[i]=Predv[i-1]
							else: 
								Predv[i-1]=Predv[i]
			       
			#PtotalT=PtotalT+Pred
					i=i+1
					time.sleep(0.05)
			except:
				time.sleep(0.2)
				i=0
				PtotalT=0
				while i<5:
				
        				pred_b = ina.power()/1000
        				pred1_b = ina1.power()/1000
     					pred2_b = ina2.power()/1000
        				pred3_b = ina3.power()/1000
	      				Ptotal_b=pred_b+pred1_b+pred2_b+pred2_b
	      				Ptotal_b=round(Ptotal_b,3)
			#print(type(Itotal))
			
					Ptotal_b=6.8807+1.06223*Ptotal_b+0.00221977*Ptotal_b*Ptotal_b
					Predv[i]=Ptotal_b
			#
			#print(Pred[2])
					if i>=1:
						if Predv[i]<0.9*Predv[i-1] or Predv[i]>1.1*Predv[i-1]:
							#print("entre aqui")
							if Predv[i]>Predv[i-1]:
						
								Predv[i]=Predv[i-1]
							else: 
								Predv[i-1]=Predv[i]
							
					i=i+1
					time.sleep(0.05)
					
	PtotalT=np.mean(Predv)
	return PtotalT
	


def main():
	#global Pred
	i=0
	#thread.start_new_thread(adquisicion2,(i,))
	while i<41:
  
   
    		n = excel.main(float(16),0)
   		n = int(n)
    		mcpras.set_value(n)
    		time.sleep(1)
   # P1=Node611.sensorm()
     		
		try:
			Pred=adquisicion2()
 #   		
		except:
			time.sleep(0.1)
			Pred=adquisicion2()
#			
#
#		result = client.read_holding_registers(11729, 2, unit=1)#Current A 1100
#		decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big )
#		print(result.registers)
#		print(decoder.decode_32bit_float())
#		result.registers=0
		#archivo.write(str(Pred)+'\n')
 		print(Pred)
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

                  
