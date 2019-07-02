import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import Node611
import excel
import mcpras 
import time


#Fuzzy Controller 

Vrefd = ctrl.Consequent(np.arange(-2, 2, 0.1), 'Vrefd')
Pdif = ctrl.Antecedent(np.arange(-200, 200, 0.01),'Pdif')

#Membership functions

#Pdif

Pdif['N'] = fuzz.trapmf(Pdif.universe, [-100,-2, -0.2, -0.01])
Pdif['P'] = fuzz.trapmf(Pdif.universe, [0.01, 0.2, 2, 100])
Pdif['Z'] = fuzz.trimf(Pdif.universe, [-0.01,0,0.01])


#Vref

Vrefd['N'] = fuzz.trimf(Vrefd.universe, [-0.2, -0.1, 0])
Vrefd['P'] = fuzz.trimf(Vrefd.universe, [0, 0.1, 0.2])
Vrefd['Z'] = fuzz.trimf(Vrefd.universe, [-0.01, 0, 0.01])

##Rules

rule1=ctrl.Rule(Pdif['P'],Vrefd['P'])
rule2=ctrl.Rule(Pdif['N'],Vrefd['N'])
rule3=ctrl.Rule(Pdif['Z'],Vrefd['Z'])

vref_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
vrefout = ctrl.ControlSystemSimulation(vref_ctrl)

i= True
v=17
while True:
  
    n = excel.main(float(v),0)
    n = int(n)
    mcpras.set_value(n)
    P1=Node611.sensorm()
   
    time.sleep(1)
    
    n = excel.main(float(v),0)
    n = int(n)
    mcpras.set_value(n)
    P2=Node611.sensorm()
    
    
    Pdif=P2-P1
    
      
    vrefout.input['Pdif']=Pdif
    vrefout.compute()
    Vrefin=round(vrefout.output['Vrefd'],2)
   # v=v+Vrefin
  
    print("Potencia del panel t= "+str(P1))
    print("Potencia del panel  t+1 = "+str(P2))
    print("Vref = "+str(v))
    print("Cambio de potencia = "+str(Pdif))
    print("Cambio de voltaje = "+str(Vrefin))
 
  
  
