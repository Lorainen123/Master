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
Pred=0

Itotal=0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)  ## 1
GPIO.setup(19, GPIO.OUT)  ## 2
GPIO.setup(26, GPIO.OUT)  ## 3



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

    ina.configure(voltage_range=ina.RANGE_16V,
                  gain=ina.GAIN_AUTO,
                  bus_adc=ina.ADC_128SAMP,
                  shunt_adc=ina.ADC_128SAMP)

    ina1.configure(voltage_range=ina.RANGE_16V,
                  gain=ina.GAIN_AUTO,
                  bus_adc=ina.ADC_128SAMP,
                  shunt_adc=ina.ADC_128SAMP)

    ina2.configure(voltage_range=ina.RANGE_16V,
                  gain=ina.GAIN_AUTO,
                  bus_adc=ina.ADC_128SAMP,
                  shunt_adc=ina.ADC_128SAMP)

    ina3.configure(voltage_range=ina.RANGE_16V,
                  gain=ina.GAIN_AUTO,
                  bus_adc=ina.ADC_128SAMP,
                  shunt_adc=ina.ADC_128SAMP)
except:
    time.sleep(0.1)


#Fuzzy Controller 

Vrefd = ctrl.Consequent(np.arange(-0.9, 0.9, 0.1), 'Vrefd')
dIdv = ctrl.Antecedent(np.arange(-500, 500, 0.01),'dIdv')

#Membership functions

#Dired 
#dIdv['NB'] = fuzz.trapmf(dIdv.universe, [-200, -1.05, -0.5, -0.24])
#dIdv['NS'] = fuzz.trimf(dIdv.universe, [-0.5, -0.24, -0.02])
#dIdv['Z'] = fuzz.trapmf(dIdv.universe, [-0.24, -0.05, 0.05, 0.24])
#dIdv['PS'] = fuzz.trimf(dIdv.universe, [0.02, 0.24, 0.5])
#dIdv['PB'] = fuzz.trapmf(dIdv.universe, [0.24, 0.5, 1.05, 200])

dIdv['NB'] = fuzz.trapmf(dIdv.universe, [-500, -21, -15, -10])
dIdv['NS'] = fuzz.trimf(dIdv.universe, [-15, -8, -1])
dIdv['Z'] = fuzz.trapmf(dIdv.universe, [-8, -0.4, 0.4, 8])
dIdv['PS'] = fuzz.trimf(dIdv.universe, [1, 8, 15])
dIdv['PB'] = fuzz.trapmf(dIdv.universe, [10, 15, 21, 500])

#dIdv['NB'] = fuzz.trapmf(dIdv.universe, [-500, -21, -10, -4.8])
#dIdv['NS'] = fuzz.trimf(dIdv.universe, [-10, -4.8, -0.4])
#dIdv['Z'] = fuzz.trapmf(dIdv.universe, [-2, -0.4, 0.4, 2])
#dIdv['PS'] = fuzz.trimf(dIdv.universe, [0.4, 4.8, 10])
#dIdv['PB'] = fuzz.trapmf(dIdv.universe, [4.8, 10, 21, 500])


#Vref

Vrefd['NB'] = fuzz.trapmf(Vrefd.universe, [-0.87, -0.63, -0.5, -0.29])
Vrefd['NS'] = fuzz.trimf(Vrefd.universe, [-0.3, -0.145, -0.001])
Vrefd['Z'] = fuzz.trimf(Vrefd.universe, [-0.002, 0, 0.002])
Vrefd['PS'] = fuzz.trimf(Vrefd.universe, [0.001, 0.145, 0.3])
Vrefd['PB'] = fuzz.trapmf(Vrefd.universe, [0.29, 0.5, 0.63, 0.87])

##Rules

#rule1=ctrl.Rule(Pdif['P'],Vrefd['P'])
#rule2=ctrl.Rule(Pdif['N'],Vrefd['N'])
#rule3=ctrl.Rule(Pdif['Z'],Vrefd['Z'])
rule1=ctrl.Rule(dIdv['PB'],Vrefd['NB'])
rule2=ctrl.Rule(dIdv['NB'],Vrefd['PB'])
rule3=ctrl.Rule(dIdv['PS'],Vrefd['NS'])
rule4=ctrl.Rule(dIdv['NS'],Vrefd['PS'])
rule5=ctrl.Rule(dIdv['Z'],Vrefd['Z'])

vref_ctrl = ctrl.ControlSystem([rule1, rule2, rule3,rule4, rule5])
vrefout = ctrl.ControlSystemSimulation(vref_ctrl)


def adquisicion():
	global PStotal, PLtotal, sw, Pred
		
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
			
		
		sw=1
		#print("Potencia del panel = "+str(PStotal))
		#print("Potencia de la bat = "+str(PBtotal))
		#print("Potencia de la carga = "+str(PLtotal))
		
		time.sleep(0.001)




def corrienteRed(): 
	try:
		i=0
		PtotalT=0
	#	while i<1:
			
        	ired = ina.power()/1000
        	ired1 = ina1.power()/1000
     		ired2 = ina2.power()/1000
        	ired3 = ina3.power()/1000
	      	Itotal=ired+ired1+ired2+ired3
	      	Itotal=round(Itotal,3)
		Pred=round(6.8807+1.06223*Itotal+0.00221977*Itotal*Itotal,3)
			
		#PtotalT=PtotalT+Pred
		#i=i+1
	except:
			try:
				time.sleep(0.2)
				i=0
				PtotalT=0
				
			
        			ired = ina.power()/1000
        			ired1 = ina1.power()/1000
     				ired2 = ina2.power()/1000
        			ired3 = ina3.power()/1000
	      			Itotal=ired+ired1+ired2+ired3
	      			Itotal=round(Itotal,3)
				Pred=round(6.8807+1.06223*Itotal+0.00221977*Itotal*Itotal,3)
					
				#PtotalT=PtotalT+Pred
				#i=i+1
			except:
				time.sleep(0.2)
				i=0
				PtotalT=0
				#while i<5:
				
        			ired = ina.power()/1000
        			ired1 = ina1.power()/1000
     				ired2 = ina2.power()/1000
        			ired3 = ina3.power()/1000
	      			Itotal=ired+ired1+ired2+ired3
	      			Itotal=round(Itotal,3)
				Pred=round(6.8807+1.06223*Itotal+0.00221977*Itotal*Itotal,3)
					
				#	PtotalT=PtotalT+Pred
				#	i=i+1
	
	return Pred


def fuzzy():
    sw=0
    i= True
    #thread.start_new_thread(adquisicion2,(i,))
    dIdv=5
    v2=18.5
    dired=0

    n = excel.main(float(v2),0)
    n = int(n)
    mcpras.set_value(n)
    time.sleep(0.2)
    Ired2=corrienteRed()

    while True:
         if sw==0:
      	 
   	 	vrefout.input['dIdv']=dIdv
    	 	vrefout.compute()
    		Vrefin=round(vrefout.output['Vrefd'],3)
   	 	Vrefinabs=abs(Vrefin)
		
	 elif sw==1:
		Vrefin=0.1
		sw=0
	 
	# print("Corriente de la red t= "+str(Ired))
    	 print("Corriente de la red t+1 = "+str(Ired2))
	 print("Cambio de corriente ="+str(dired))
	# print("Vref1"+str(v))
   	 print("Vref2 = "+str(v2))
	
	# print("diferencia de voltaje v2-v"+str(Vdif))
	 	
         print("Cambio de corriente/voltaje = "+str(dIdv))
   	 print("Cambio de voltaje= "+str(Vrefin)+"\n")
					
	 v2=v2+Vrefin
	 Ired=Ired2
	# print(v2)
	
	 if v2<14.6:
		v2=14.5	
	 elif v2>18.5:
		v2=18.6
			
	 n = excel.main(float(v2),0)
   	 n = int(n)
    	 mcpras.set_value(n)
	 
	 time.sleep(0.2)
	  
	# try:
    	 Ired2=corrienteRed()
	#except:
	#	try:	
    	#		time.sleep(0.5)
	#		Ired2=corrienteRed()
	#	except:
	#		time.sleep(0.5)
	#		Ired2=corrienteRed()
  		
	 
	 dired=Ired2-Ired
	
	 try:
	 	dIdv=dired/Vrefin
	 except:
		if dired>0.05*Ired2:
			Iredbck=corrienteRed()
			
			if Iredbck>0.9*Ired2 and Iredbck<1.1*Ired2:
				dIdv=1.5
				Ired2=Iredbck
				dired=Ired-Ired
		else:
			sw=1
			

	 if abs(Vrefin)<0.2 and abs(dIdv)>15:
		dIdv=1.5
	
	
	 if dIdv>=500:
		dIdv=500
	 elif dIdv<=-500:
		dIdv=-500
	

		#dired=abs(dired)
		#if dired<=0.01:
		#	dIdv=0
		#else:
		#	dIdv=2
		
	# print (v2)
    	
	 
#	

def main():
	
	while True:
		print('Ingrese el siguiente estado del sistema:')
		x = input()
		if x==1:
			GPIO.output(13, False)
			GPIO.output(19, False)
			GPIO.output(26, False)
		elif x==2:
			GPIO.output(13, False)
			GPIO.output(19, False)
			GPIO.output(26, True)
		elif x==3:
			GPIO.output(13, False)
			GPIO.output(19, True)
			GPIO.output(26, False)
		elif x==4:
			GPIO.output(13, False)
			GPIO.output(19, True)
			GPIO.output(26, True)
		elif x==5:
			GPIO.output(13, True)
			GPIO.output(19, False)
			GPIO.output(26, False)
			
			
	  
  


#main()
hilo1=threading.Thread(target=fuzzy)
#hilo2=threading.Thread(target=main)
#hilo3=threading.Thread(target=adquisicion)
hilo1.start()
#hilo2.start()
#hilo3.start()
   
   # dpdv=Pdif/Vdif
       
   # if (abs(Pdif)<1): 
   #   dpdv=0
     
    
       
  #  n = excel.main(float(v+0.2),0)
  #  n = int(n)
  #  mcpras.set_value(n)
  #  P2=Node611.sensorm()
