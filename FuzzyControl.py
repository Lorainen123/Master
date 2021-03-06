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

dpdv['N'] = fuzz.trapmf(dpdv.universe, [-300,-2, -0.2, -0.01])
dpdv['P'] = fuzz.trapmf(dpdv.universe, [0.01, 0.2, 2, 300])
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


vref_ctrl = ctrl.ControlSystem([rule1, rule2, rule3,rule4, rule5])
vrefout = ctrl.ControlSystemSimulation(vref_ctrl)

i= True
dpdv=-1
Vdif=-0.2
v2=18.6

n = excel.main(float(v2),0)
n = int(n)
mcpras.set_value(n)
P2=Node611.sensorm()

while True:
  
    if v2<=14.6 :
      v2=14.5
    elif v2>=18.5:
      v2=18.6
      
    vrefout.input['dpdv']=dpdv
    vrefout.input['Vdif']=Vdif
    vrefout.compute()
    Vrefin=round(vrefout.output['Vrefd'],2)
    
    
    if Vrefin==0:
       n = excel.main(float(v2),0)
       n = int(n)
       mcpras.set_value(n)
       time.sleep(1)
       P2=Node611.sensorm()
       
       
        
       n = excel.main(float(v2-0.3),0)
       n = int(n)
       mcpras.set_value(n)
       time.sleep(1)
       P1=Node611.sensorm() 
       
       Pdif=P2-P1
       Vdif=0.2
      
    else:
       v=v2
       v2=v2+Vrefin
       Vdif=v2-v
       P1=P2
       n = excel.main(float(v2),0)
       n = int(n)
       mcpras.set_value(n)
       time.sleep(1)
       P2=Node611.sensorm()
       Pdif=P2-P1
       

 
    
   
    dpdv=Pdif/Vdif
       
    if (abs(Pdif)<1): 
      dpdv=0
     
    
       
  #  n = excel.main(float(v+0.2),0)
  #  n = int(n)
  #  mcpras.set_value(n)
  #  P2=Node611.sensorm()
    
    
    
         
    
    print("Potencia del panel t= "+str(P1))
    print("Potencia del panel  t+1 = "+str(P2))
    print("Vref = "+str(v2))
    print("Cambio de potencia/voltaje = "+str(dpdv))
    print("Cambio de voltaje = "+str(Vrefin))
 
  
  
