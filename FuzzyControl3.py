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
dIdv = ctrl.Antecedent(np.arange(-200, 200, 0.01),'dIdv')

#Membership functions

#Dired 
dIdv['NB'] = fuzz.trapmf(dIdv.universe, [-10, -1.05, -0.5, -0.24])
dIdv['NS'] = fuzz.trimf(dIdv.universe, [-0.5, -0.24, -0.02])
dIdv['Z'] = fuzz.trapmf(dIdv.universe, [-0.1, -0.02, 0.02, 0.1])
dIdv['PS'] = fuzz.trimf(dIdv.universe, [0.02, 0.24, 0.5])
dIdv['PB'] = fuzz.trapmf(dIdv.universe, [0.24, 0.5, 1.05, 10])

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
rule1=ctrl.Rule(dIdv['PB'],Vrefd['NB'])
rule2=ctrl.Rule(dIdv['NB'],Vrefd['PB'])
rule3=ctrl.Rule(dIdv['PS'],Vrefd['NS'])
rule4=ctrl.Rule(dIdv['NS'],Vrefd['PS'])
rule5=ctrl.Rule(dIdv['Z'],Vrefd['Z'])

vref_ctrl = ctrl.ControlSystem([rule1, rule2, rule3,rule4, rule5])
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
    dIdv=1 
    v2=18.6

    n = excel.main(float(v2),0)
    n = int(n)
    mcpras.set_value(n)
    Ired2=adquisicion2()

    while True:
  
      	 
   	 vrefout.input['dIdv']=dIdv
    	 vrefout.compute()
    	 Vrefin=round(vrefout.output['Vrefd'],2)
   
  	 v=v2
    	 v2=v2+Vrefin
    	 Vdif=v2-v
    	 Ired=Ired2
	 try:	
    	 	n = excel.main(float(v2),0)
   	 	n = int(n)
    	 	mcpras.set_value(n)
    	 except:
		n = excel.main(float(14.5),0)
   	 	n = int(n)
    	 	mcpras.set_value(n)
		v2=14.5
		
		
	 time.sleep(0.5)
    	 Ired2=adquisicion2()
    	 dired=Ired2-Ired
	 
	 try:
			
	 	dIdv=dired/Vdif
         except:
		if dired<=0.003:
			dIdv=0
		else:
			dIdv=0.2

    	
	 
	 print("Corriente de la red t= "+str(Ired))
    	 print("Corriente de la red t+1 = "+str(Ired2))
	 print("Cambio de corriente ="+str(dired))
	 print("Vref1"+str(v))
   	 print("Vref2 = "+str(v2))
	 print("diferencia de voltaje v2-v"+str(Vdif))
		
         print("Cambio de corriente/voltaje = "+str(dIdv))
   	 print("Cambio de voltaje = "+str(Vrefin))
 
  
  


main()
    
   
   # dpdv=Pdif/Vdif
       
   # if (abs(Pdif)<1): 
   #   dpdv=0
     
    
       
  #  n = excel.main(float(v+0.2),0)
  #  n = int(n)
  #  mcpras.set_value(n)
  #  P2=Node611.sensorm()
    
