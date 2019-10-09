import os
import sys
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
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import xlsxwriter


#Configuracion puerto SPI
SPI_PORT   = 0
SPI_DEVICE = 0
sw=0



mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

j=0

#Configuration pin output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)  ## 1
GPIO.setup(19, GPIO.OUT)  ## 2
GPIO.setup(26, GPIO.OUT)  ## 3
GPIO.output(13, False)
GPIO.output(19, False)
GPIO.output(26, False)



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


client = ModbusClient(method='rtu', port= '/dev/ttyUSB0', bytesize=8, timeout=1, baudrate= 19200)

def adquisicion():
	
	
	while True:
	#	tic = tm.default_timer()
		#Inicializacion de variables antes de entrar al loop y obtener los promedios
		IpanelT=0
		VpanelT=0
		VpanelV=0
		
		IcargaT=0
		VcargaT=0
		
		IbatT=0
		VbatT=0
		
		Vsensor=0
					
		for j in range(501):
			
			##potencia del panel solar
		
			Ipanel = mcp.read_adc(7)  ## Corriente del panel solar
			Ipanel=((Ipanel)*(5.15/1023))
			#IpanelV=IpanelV+Ipanel
			Ipanel=Ipanel+0.03
			#Ipanel=(-25.3+10*Ipanel)-0.2
			Ipanel=(-2.6+Ipanel)*(1/0.09693)
			if Ipanel>0:
				IpanelT=IpanelT+Ipanel   ## Suma de corriente del panel solar sin promediar
		
			Vpanel = mcp.read_adc(4)
			Vpanel = Vpanel*(5.15/1023)
			VpanelV=VpanelV+Vpanel
			#Vpanel=Vpanel*(37.5/7.5)  ## voltaje del panel solar
			Vpanel=4.093*Vpanel+3.4444
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
		
			## potencia de la bateria
			Ibat = mcp.read_adc(1)
			Ibat=((Ibat)*(5.15/1023))
			#Vsensor=Vsensor+Ibat
			#Ibat=(-2.54+Ibat)*(1/0.1852)
			IbatT=IbatT+Ibat
			Vbat = mcp.read_adc(5)
			Vbat = ((Vbat)*(5.15/1023))*(37000.0/7500.0) 
			VbatT=VbatT+Vbat
		
			#j=j+1
		
	#	toc = tm.default_timer()
		## potencia del panel solar			
		PStotal=round(((IpanelT)*((VpanelT)+0.5)/j)/j,2) ## potencia del panel solar promedio
		
		
		## potencia de la carga 
		IcargaT=(IcargaT/j)-0.2
		PLtotal=(VcargaT/j)*IcargaT
		#PLtotal=round((-6.96327 + 0.742732*PLtotal + 0.00062677*PLtotal*PLtotal)+2,2)
		PLtotal=round((4.80352 + 0.624629*PLtotal+ 0.000745302*PLtotal*PLtotal),2)
		
		## potencia de la bateria
		IbatT=IbatT/j
		
		if IbatT<2.4:
			IbatT=6*IbatT-14.28
		elif IbatT>2.46:
			IbatT=5*IbatT-11.86
		else:
			Ibat=0
		
		PBtotal=round((IbatT*VbatT)/(j),2)-13
		#print(IbatT/j)
		
		if PLtotal<2: 
			PLtotal=0
			
		elif PStotal <2:
			PStotal=0
			
		result = client.read_holding_registers(11729, 2, unit=1)#Current A 1100
		decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big )
		PTred=decoder.decode_32bit_float()
		sw=1
		
		return  PStotal 

print(adquisicion())
	
		

