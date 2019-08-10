import os
import sys
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
#import Node611
import excel
import mcpras 
import time
import threading
from ina219 import INA219
import RPi.GPIO as GPIO
from math import *
from time import sleep
import serial
import requests
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI
import timeit as tm
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


#configuration of low current sensors
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

j=0
IpanelT=0
VpanelT=0
VcargaT=0
IcargaT=0
PStotal=0
PLtotal=0
PBtotal=0
sw=0

Pred = 0
Predv=  np.zeros(3,)
Itotal=0
state=1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)  ## 1
GPIO.setup(19, GPIO.OUT)  ## 2
GPIO.setup(26, GPIO.OUT)  ## 3
GPIO.output(13, False)
GPIO.output(19, False)
GPIO.output(26, False)



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


#Fuzzy Controller 

Vrefd = ctrl.Consequent(np.arange(-0.9, 0.9, 0.1), 'Vrefd')
dpdv = ctrl.Antecedent(np.arange(-500, 500, 0.01),'dpdv')

#Membership functions

#Dired 
#dIdv['NB'] = fuzz.trapmf(dIdv.universe, [-200, -1.05, -0.5, -0.24])
#dIdv['NS'] = fuzz.trimf(dIdv.universe, [-0.5, -0.24, -0.02])
#dIdv['Z'] = fuzz.trapmf(dIdv.universe, [-0.24, -0.05, 0.05, 0.24])
#dIdv['PS'] = fuzz.trimf(dIdv.universe, [0.02, 0.24, 0.5])
#dIdv['PB'] = fuzz.trapmf(dIdv.universe, [0.24, 0.5, 1.05, 200])

#dIdv['NB'] = fuzz.trapmf(dIdv.universe, [-500, -21, -15, -10])
#dIdv['NS'] = fuzz.trimf(dIdv.universe, [-15, -8, -1])
#dIdv['Z'] = fuzz.trapmf(dIdv.universe, [-8, -0.4, 0.4, 8])
#dIdv['PS'] = fuzz.trimf(dIdv.universe, [1, 8, 15])
#dIdv['PB'] = fuzz.trapmf(dIdv.universe, [10, 15, 21, 500])

#dpdv['NB'] = fuzz.trapmf(dpdv.universe, [-500, -21, -10, -4.8])
#dpdv['NS'] = fuzz.trimf(dpdv.universe, [-10, -4.8, -0.4])
#dpdv['Z'] = fuzz.trapmf(dpdv.universe, [-4.8, -0.4, 0.4, 4.8])
#dpdv['PS'] = fuzz.trimf(dpdv.universe, [0.4, 4.8, 10])
#dpdv['PB'] = fuzz.trapmf(dpdv.universe, [4.8, 10, 21, 500])
dpdv['NB'] = fuzz.trapmf(dpdv.universe, [-500, -52.5, -50, -25])
dpdv['NS'] = fuzz.trimf(dpdv.universe, [-50, -25, 0])
dpdv['Z'] = fuzz.trapmf(dpdv.universe, [-16.6, -1, 1, 16.6])
dpdv['PS'] = fuzz.trimf(dpdv.universe, [0, 25, 50])
dpdv['PB'] = fuzz.trapmf(dpdv.universe, [25, 50, 52.5, 500])

#Vref

Vrefd['NB'] = fuzz.trapmf(Vrefd.universe, [-0.87, -0.63, -0.4, -0.2])
Vrefd['NS'] = fuzz.trimf(Vrefd.universe, [-0.4, -0.2, -0.001])
Vrefd['Z'] = fuzz.trimf(Vrefd.universe, [-0.15, 0, 0.15])
Vrefd['PS'] = fuzz.trimf(Vrefd.universe, [0.001, 0.2, 0.4])
Vrefd['PB'] = fuzz.trapmf(Vrefd.universe, [0.2, 0.4, 0.63, 0.87])

##Rules

#rule1=ctrl.Rule(Pdif['P'],Vrefd['P'])
#rule2=ctrl.Rule(Pdif['N'],Vrefd['N'])
#rule3=ctrl.Rule(Pdif['Z'],Vrefd['Z'])
rule1=ctrl.Rule(dpdv['PB'],Vrefd['NB'])
rule2=ctrl.Rule(dpdv['NB'],Vrefd['PB'])
rule3=ctrl.Rule(dpdv['PS'],Vrefd['NS'])
rule4=ctrl.Rule(dpdv['NS'],Vrefd['PS'])
rule5=ctrl.Rule(dpdv['Z'],Vrefd['Z'])

vref_ctrl = ctrl.ControlSystem([rule1, rule2, rule3,rule4, rule5])
vrefout = ctrl.ControlSystemSimulation(vref_ctrl)

client = ModbusClient(method='rtu', port= '/dev/ttyUSB0', bytesize=8, timeout=1, baudrate= 9600)
if client.connect():
    
    print("puerto abierto")
else:
    print("puerto no abierto")


def adquisicion():
	global PStotal, PLtotal, Pred, PBtotal, sw, state
		
	while True:
		#tic = tm.default_timer()
		#Inicializacion de variables antes de entrar al loop y obtener los promedios
		IpanelT=0
		VpanelT=0
		
		IcargaT=0
		VcargaT=0
		
		IbatT=0
		VbatT=0
		
		for j in range(501):
			
			##potencia del panel solar
		
			Ipanel = mcp.read_adc(7)  ## Corriente del panel solar
			Ipanel=((Ipanel)*(5.15/1023))
			#Ipanel=(-25.3+10*Ipanel)-0.2
			Ipanel=(-2.6+Ipanel)*(1/0.09693)
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
		
			## potencia de la bateria
			Ibat = mcp.read_adc(1)
			Ibat=((Ibat)*(5.15/1023))
			Ibat=(-2.55+Ibat)*(1/0.068)
			IbatT=IbatT+Ibat
			Vbat = mcp.read_adc(5)
			Vbat = ((Vbat)*(5.15/1023))*(37000.0/7500.0) 
			VbatT=VbatT+Vbat
		
			#j=j+1
		
		#toc = tm.default_timer()
		## potencia del panel solar			
		PStotal=round((IpanelT*VpanelT)/(j*j),2) ## potencia del panel solar promedio
		
		
		## potencia de la carga 
		IcargaT=(IcargaT/j)-0.2
		PLtotal=(VcargaT/j)*IcargaT
		PLtotal=round((-6.96327 + 0.742732*PLtotal + 0.00062677*PLtotal*PLtotal)+2,2)
		
		## potencia de la bateria
		PBtotal=round((IbatT*VbatT)/(j*j),2)
		#print(PBtotal)
		
		if PLtotal<2: 
			PLtotal=0
			
		elif PStotal <2:
			PStotal=0
			
		
		
		result = client.read_holding_registers(11729, 2, unit=1)#Current A 1100
		decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big )
		Pred=decoder.decode_32bit_float()
		sw=1
		print("Potencia de la red = "+str(Pred))
		print("Potencia del panel = "+str(PStotal))
		print("Potencia de la bat = "+str(PBtotal))
		print("Potencia de la carga = "+str(PLtotal))
		print(state)
		Estados(state)
		
	#	time.sleep(0.001)

#		if PStotal>0 and Pred<PLtotal:
#				GPIO.output(13, False)
#				GPIO.output(19, False)
#				GPIO.output(26, False)
#				
#		elif Pred<=8:
#				GPIO.output(13, False)
#				GPIO.output(19, False)
#				GPIO.output(26, True)
#		elif PStotal<=0 and Pred<=0:
#				GPIO.output(13, False)
#				GPIO.output(19, True)
#				GPIO.output(26, False)
				



def potenciaRed(): 
	try:
		i=0
		#totalT=0
		while i<3:
			
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
				while i<3:	
			
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
				while i<3:
				
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


def fuzzy():
    sw=0
    i= True
    #thread.start_new_thread(adquisicion2,(i,))
    dpdv=100
    v2=18.5
    dpred=0

    n = excel.main(float(v2),0)
    n = int(n)
    mcpras.set_value(n)
    time.sleep(0.2)
    Pred2= potenciaRed()

    while True:
         if sw==0:
      	 
   	 	vrefout.input['dpdv']=dpdv
    	 	vrefout.compute()
    		Vrefin=round(vrefout.output['Vrefd'],3)
   	 	Vrefinabs=abs(Vrefin)
		
	 elif sw==1:
		Vrefin=0.1
		sw=0
	 elif sw==2:
		Vrefin=-0.1
		sw=0
		
	 
	# print("Corriente de la red t= "+str(Ired))
    	# print("Corriente de la red t+1 = "+str(Pred2))
	# print("Cambio de corriente ="+str(dpred))
	# print("Vref1"+str(v))
   	# print("Vref2 = "+str(v2))
	
	# print("diferencia de voltaje v2-v"+str(Vdif))
	 	
        # print("Cambio de corriente/voltaje = "+str(dpdv))
   	# print("Cambio de voltaje= "+str(Vrefin)+"\n")
					
	 v2=v2+Vrefin
	 Pred=Pred2
	# print(v2)
	
	 if v2<14.6:
		v2=14.5	
	 elif v2>18.5:
		v2=18.5
			
	 n = excel.main(float(v2),0)
   	 n = int(n)
    	 mcpras.set_value(n)
	 
	 time.sleep(0.2)
	  
	# try:
    	 Pred2=potenciaRed()
	#except:
	#	try:	
    	#		time.sleep(0.5)
	#		Ired2=corrienteRed()
	#	except:
	#		time.sleep(0.5)
	#		Ired2=corrienteRed()
  		
	 
	 dpred=Pred2-Pred
	
	# try:
	 if Vrefin<0:
		dpdv=dpred*-10
	 elif Vrefin>0:
		dpdv=dpred*10
	 else:
		sw=1
		#dpdv=dpred/Vrefin
	# except:
	#	sw=1
	#	if dpred>0.05*Pred2:
	#		Predbck=potenciaRed()
			
	#		if Predbck<0.9*Pred2 and Predbck>1.1*Pred2:
	#			sw=1
	#			Pred2=Predbck
	#			dpred=Pred2-Pred
	#	else:
	#		sw=1
			

	 if abs(Vrefin)<0.09 and abs(dpdv)>35:
		#dIdv=1.5
		if dpdv<0:
			
			sw=1
		else:
			sw=2
	
	 if dpdv>=500:
		dpdv=500
	 elif dpdv<=-500:
		dpdv=-500
	

		#dired=abs(dired)
		#if dired<=0.01:
		#	dIdv=0
		#else:
		#	dIdv=2
		
	# print (v2)
    	
	 
def state1():
	global state
	
	if (0.57*PStotal+0.41*Pred)<1.1*PLtotal and (0.57*PStotal+0.41*Pred)>0.9*PLtotal and Pred<PLtotal and Pred>7:
		state=1
		GPIO.output(13, False)
		GPIO.output(19, False)
		GPIO.output(26, False)
	elif Pred<7:
		state=2
	
def state2():
        global state
	
	if 0.57*PStotal<1.1*PLtotal and 0.57*PStotal>0.9*PLtotal
		GPIO.output(13, False)
		GPIO.output(19, False)
		GPIO.output(26, True)
		state=2
	else:
		state=1
		
		

def Estados(state):
	#global state
        if state==1:
		state1()
	elif state==2:
		state2()

def main():
	global sw
	while True:
		
			print('Ingrese el siguiente estado del sistema:')
			x = input()
			print(Estados(x))
		
		#if sw==1:
		#	time.sleep(0.000001)
		#	print("Potencia de la red = "+str(Pred))
		#	print("Potencia del panel = "+str(PStotal))
		#	print("Potencia de la bat = "+str(PBtotal))
		#	print("Potencia de la carga = "+str(PLtotal))
		
		
			
			
	  
  


#main()
#hilo1=threading.Thread(target=fuzzy)
#hilo2=threading.Thread(target=main)
hilo3=threading.Thread(target=adquisicion)

#hilo1.start()
#hilo2.start()
hilo3.start()
 
#while True:
#	Pred=potenciaRed()
#	print(Pred)
	
   # dpdv=Pdif/Vdif
       
   # if (abs(Pdif)<1): 
   #   dpdv=0
     
    
       
  #  n = excel.main(float(v+0.2),0)
  #  n = int(n)
  #  mcpras.set_value(n)
  #  P2=Node611.sensorm()
