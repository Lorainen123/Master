import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import Node611
import excel
import mcpras 
import time
from ina219 import INA219
#configuration of low current sensors
Itotal=0
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
dired = ctrl.Antecedent(np.arange(-200, 200, 0.01),'dired')
Vdif = ctrl.Antecedent(np.arange(-0.9, 0.9, 0.1),'Vdif')

#Membership functions

#Dired 
dired['NB'] = fuzz.trapmf(dired.universe, [-0.725, -0.525, -0.07, -0.04])
dired['NS'] = fuzz.trimf(dired.universe, [-0.05, -0.024, -0.002])
dired['Z'] = fuzz.trimf(dired.universe, [-0.003, 0, 0.003])
dired['PS'] = fuzz.trimf(dired.universe, [0.002, 0.024, 0.05])
dired['PB'] = fuzz.trapmf(dired.universe, [0.04, 0.05, 0.525, 0.725])

#Vdif

Vdif['NB'] = fuzz.trapmf(Vdif.universe, [-0.87, -0.63, -0.5, -0.29])
Vdif['NS'] = fuzz.trimf(Vdif.universe, [-0.3, -0.145, -0.001])
Vdif['Z'] = fuzz.trimf(Vdif.universe, [-0.002, 0, 0.002])
Vdif['PS'] = fuzz.trimf(Vdif.universe, [0.01, 0.145, 0.3])
Vdif['PB'] = fuzz.trapmf(Vdif.universe, [0.29, 0.5, 0.63, 0.87])

#Vref

Vrefd['NB'] = fuzz.trapmf(Vrefd.universe, [-0.87, -0.63, -0.5, -0.29])
Vrefd['NS'] = fuzz.trimf(Vrefd.universe, [-0.3, -0.145, -0.001])
Vrefd['Z'] = fuzz.trimf(Vrefd.universe, [-0.002, 0, 0.002])
Vrefd['PS'] = fuzz.trimf(Vrefd.universe, [0.01, 0.145, 0.3])
Vrefd['PB'] = fuzz.trapmf(Vrefd.universe, [0.29, 0.5, 0.63, 0.87])

##Rules

#rule1=ctrl.Rule(Pdif['P'],Vrefd['P'])
#rule2=ctrl.Rule(Pdif['N'],Vrefd['N'])
#rule3=ctrl.Rule(Pdif['Z'],Vrefd['Z'])
rule1=ctrl.Rule(dired['PB']&Vdif['PS'],Vrefd['NB'])
rule2=ctrl.Rule(dired['NB']&Vdif['NS'],Vrefd['NB'])
rule3=ctrl.Rule(dired['NB']&Vdif['NB'],Vrefd['NS'])
rule4=ctrl.Rule(dired['NS']&Vdif['NS'],Vrefd['NS'])
rule5=ctrl.Rule(dired['NS']&Vdif['NB'],Vrefd['NS'])
rule6=ctrl.Rule(dired['PS']&Vdif['NB'],Vrefd['PS'])
rule7=ctrl.Rule(dired['Z'],Vrefd['Z'])


vref_ctrl = ctrl.ControlSystem([rule1, rule2, rule3,rule4, rule5,rule6,rule7])
vrefout = ctrl.ControlSystemSimulation(vref_ctrl)


def adquisicion2():   
	#global Itotal
	
	#while True:  #adquisicion of low current sensors
		#tic = tm.default_timer()
        	ired = ina.current()/1000
        	ired1 = ina1.current()/1000
     		ired2 = ina2.current()/1000
        	ired3 = ina3.current()/1000
	      	Itotal=ired+ired1+ired2+ired3
	      	Itotal=round(Itotal,3)
	      	#time.sleep(0.00080)
         	return Itotal
		#toc = tm.default_timer()
		#print(toc-tic)
		


def main(): 
    i= True
    #thread.start_new_thread(adquisicion2,(i,))
    dired=0.1
    Vdif=0.2
    v2=18.6

    n = excel.main(float(v2),0)
    n = int(n)
    mcpras.set_value(n)
    Ired2=adquisicion2()

    while True:
  
   	 if v2<=14.6 :
     	 	v2=14.5
 	 elif v2>=18.5:
      		v2=18.6
      
   	 vrefout.input['dired']=dired
    	 vrefout.input['Vdif']=Vdif
    	 vrefout.compute()
    	 Vrefin=round(vrefout.output['Vrefd'],2)
    
    
    #if Vrefin==0:
       #n = excel.main(float(v2),0)
       #n = int(n)
       #mcpras.set_value(n)
       #time.sleep(1)
       #P2=Node611.sensorm()
       
       
        
       #n = excel.main(float(v2-0.3),0)
       #n = int(n)
       #mcpras.set_value(n)
       #time.sleep(1)
       #P1=Node611.sensorm() 
       
       #Pdif=P2-P1
       #Vdif=0.2
      
    #else:
   	 v=v2
    	 v2=v2+Vrefin
    	 Vdif=v2-v
    	 Ired=Ired2
    	 n = excel.main(float(v2),0)
   	 n = int(n)
    	 mcpras.set_value(n)
    	 time.sleep(1)
    	 Ired2=adquisicion2()
    	 dired=Ired2-Ired
       

    	 print("Corriente de la red t= "+str(Ired))
    	 print("Corriente de la red t+1 = "+str(Ired2))
	 print("Cambio de corriente ="+str(dired))
   	 print("Vref = "+str(v2))
   # print("Cambio de potencia/voltaje = "+str(dpdv))
   	 print("Cambio de voltaje = "+str(Vrefin))
 
  
  


main()
    
   
   # dpdv=Pdif/Vdif
       
   # if (abs(Pdif)<1): 
   #   dpdv=0
     
    
       
  #  n = excel.main(float(v+0.2),0)
  #  n = int(n)
  #  mcpras.set_value(n)
  #  P2=Node611.sensorm()
    
    
    
         
    
