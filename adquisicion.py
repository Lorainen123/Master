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
import threading
import timeit as tm

#Configuration SPI Port and device
SPI_PORT   = 0
SPI_DEVICE = 0
sw=0
N=50
S_2=0
j=0
bufred = np.zeros((N,))
bufsol = np.zeros((N,))
bufbat = np.zeros((N,))
bufload = np.zeros((N,))
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
Itotal=0
j=0
IpanelT=0
VpanelT=0
VcargaT=0
IcargaT=0
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


def adquisicion():
	global PRtotal, IpanelT, VpanelT, IcargaT, VcargaT,j
		
	while True:
		tic = tm.default_timer()
		#Inicializacion de variables antes de entrar al loop y obtener los promedios
		Ipanel=0
		Vpanel=0
		
		IcargaT=0
		VcargaT=0
		
		for j in range(501):
			
			##potencia del panel solar
		
			Ipanel = mcp.read_adc(2)  ## Corriente del panel solar
			Ipanel=((Ipanel)*(5.15/1023))
			Ipanel=(-25.3+10*Ipanel)-0.2
			IpanelT=IpanelT+Ipanel   ## Suma de corriente del panel solar sin promediar
		
			Vpanel = mcp.read_adc(4)
			Vpanel = Vpanel*(5.15/1023)*(37.5/7.5)  ## voltaje del panel solar
			VpanelT= VpanelT+Vpanel #  Suma de voltaje del panel solar sin promediar
		
			## potencia de la carga
			Vcarga = mcp.read_adc(6)
			Vcarga = ((Vcarga)*(5.15/1023))*(37000.0/7500.0) 
			VcargaT=VcargaT+Vcarga
   	       		Icarga = mcp.read_adc(0)   ## 
			Icarga=round(((Icarga)*(5.15/1023)),2)  ## voltaje desde el MCP
   			#S_5=(-25.3+10*S_5m)-0.2
			Icarga=(-2.54+Icarga)*(1/0.095)  ## calculo de corriente de la carga
			IcargaT=IcargaT+Icarga
		
			
		
			#j=j+1
		time.sleep(0.001)
		toc = tm.default_timer()
		## potencia del panel solar			
		PStotal=(IpanelT*VpanelT)/(j*j) ## potencia del panel solar promedio
			
		## potencia de la carga 
		IcargaT=(IcargaT/j)-0.2
		PLtotal=(VcargaT/j)*IcargaT
		PLtotal=-6.96327 + 0.742732*PLtotal + 0.00062677*PLtotal*PLtotal
		#print(PLtotal)
		
		print(j)
		
			#time.sleep(0.00005)
def adquisicion2():
		
		pred = ina.power()/1000   ##se leen los 4 sensores por I2C 
       		pred1 = ina1.power()/1000
     		pred2 = ina2.power()/1000
       		pred3 = ina3.power()/1000
		PRtotal=pred+pred1+pred2+pred3  ## se suma la potencia de cada sensor PRtotal= potencia de la red despues de los rectificadores
		PRtotal=round(PRtotal,3)
		##potencia de la red
		Pred=6.8807+1.06223*PRtotal+0.00221977*PRtotal*PRtotal


		
  

def main():
	global sw, PRtotal, PStotal,j, IcargaT, VcargaT, VpanelT, IpanelT
	i=1
	
	#thread.start_new_thread(adquisicion1,(i,))
#	thread.start_new_thread(adquisicion2,(i,))
	
	hilo1=threading.Thread(target=adquisicion)
	hilo2=threading.Thread(target=adquisicion2)
	hilo1.start()
	hilo2.start()
		
	while True:
		
		#tic = tm.default_timer()
	#	time.sleep(0.00000005)
		#if sw==1: #dato nuevo 
			#print(A2)
			
		#	bufred[1:N]=bufred[0:N-1]
		#	bufred[0]=PRtotal
		#	pred=np.mean(bufred)
		#	pred=6.8807+1.06223*pred+0.00221977*pred*pred
		#	
		#	bufsol[1:N]=bufsol[0:N-1]
		#	bufsol[0]=PStotal
		#	psol=np.mean(bufsol)
			
		#	bufbat[1:N]=bufbat[0:N-1]
		#	bufbat[0]=S_4
		#	pbat=np.mean(bufbat)
			
		#	bufload[1:N]=bufload[0:N-1]
		#	bufload[0]=PLtotal
		#	pload=np.mean(bufload)
		#	sw=0
			#toc = tm.default_timer()
			#print(toc-tic)
			#print(pload)
			
		if j==500: 
			print(j)
	#		## potencia del panel solar			
	#		PStotal=(IpanelT*VpanelT)/(j*j) ## potencia del panel solar promedio
	#		Ipanel=0
	#		Vpanel=0
	#		## potencia de la carga 
	#		IcargaT=(IcargaT/j)-0.2
	#		PLtotal=(VcargaT/j)*IcargaT
	#		PLtotal=-6.96327 + 0.742732*PLtotal + 0.00062677*PLtotal*PLtotal
	#		IcargaT=0
	#		VcargaT=0
			##potencia de la red
	#		Pred=6.8807+1.06223*PRtotal+0.00221977*PRtotal*PRtotal
			#print(PLtotal)
	#		j=0
			
			
			
		

main()
	
	
