import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import Node611
import excel
import mcpras 
import time


#Fuzzy Controller 

Vrefd = ctrl.Consequent(np.arange(-2, 2, 0.1), 'Vrefd')
dpdv = ctrl.Antecedent(np.arange(-200, 200, 0.01),'dpdv')
Vdif = ctrl.Antecedent(np.arange(-2, 2, 0.1),'Vdif')

#Membership functions

#Pdif

dpdv['N'] = fuzz.trapmf(dpdv.universe, [-100,-2, -0.2, -0.01])
dpdv['P'] = fuzz.trapmf(dpdv.universe, [0.01, 0.2, 2, 100])
dpdv['Z'] = fuzz.trimf(dpdv.universe, [-0.01,0,0.01])

#Vdif

Vdif['N'] = fuzz.trimf(Vdif.universe, [-0.3, -0.2, -0.1])
Vdif['P'] = fuzz.trimf(Vdif.universe, [0.1, 0.2, 0.3])
Vdif['Z'] = fuzz.trimf(Vdif.universe, [-0.01, 0, 0.01])



#Vref

Vrefd['N'] = fuzz.trimf(Vrefd.universe, [-0.3, -0.2, -0.1])
Vrefd['P'] = fuzz.trimf(Vrefd.universe, [0.1, 0.2, 0.3])
Vrefd['Z'] = fuzz.trimf(Vrefd.universe, [-0.01, 0, 0.01])

##Rules

#rule1=ctrl.Rule(Pdif['P'],Vrefd['P'])
#rule2=ctrl.Rule(Pdif['N'],Vrefd['N'])
#rule3=ctrl.Rule(Pdif['Z'],Vrefd['Z'])
rule1=ctrl.Rule(dpdv['N']&Vdif['P'],Vrefd['N'])
rule2=ctrl.Rule(dpdv['N']&Vdif['N'],Vrefd['N'])
rule3=ctrl.Rule(dpdv['P']&Vdif['N'],Vrefd['P'])
rule4=ctrl.Rule(dpdv['P']&Vdif['P'],Vrefd['P'])
rule5=ctrl.Rule(dpdv['Z'],Vrefd['Z'])
rule6=ctrl.Rule(dpdv['Z'],Vrefd['Z'])

vref_ctrl = ctrl.ControlSystem([rule1, rule2, rule3,rule4, rule5, rule6])
vrefout = ctrl.ControlSystemSimulation(vref_ctrl)

i= True
dpdv=-1
Vrefin=-0.2
v2=18.6

n = excel.main(float(v2),0)
n = int(n)
mcpras.set_value(n)
P2=Node611.sensorm()

while True:
  
    if v2<14.6 :
      v2=14.5
    elif v2>18.5:
      v2=18.6
      
    vrefout.input['Pdif']=dpdv
    vrefout.input['Vdif']=Vrefin
    vrefout.compute()
    Vrefin=round(vrefout.output['Vrefd'],2)
    
    v=v2
    v2=v2+Vrefin
    Vdif=v2-v
    P1=P2
    
    n = excel.main(float(v2),0)
    n = int(n)
    mcpras.set_value(n)
    P2=Node611.sensorm()
  
    Pdif=P2-P1
    
    dpdv=Pdif/Vdif
    
    time.sleep(0.5)
    
  #  n = excel.main(float(v+0.2),0)
  #  n = int(n)
  #  mcpras.set_value(n)
  #  P2=Node611.sensorm()
    
    
    
    if (abs(Pdif)<0.2): 
       Pdif=0
         
    
    print("Potencia del panel t= "+str(P1))
    print("Potencia del panel  t+1 = "+str(P2))
    print("Vref = "+str(v2))
    print("Cambio de potencia = "+str(Pdif))
    print("Cambio de voltaje = "+str(Vrefin))
 
  
  
