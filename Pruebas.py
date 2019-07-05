import Node611
import excel
import mcpras 
import time

i=0
v=14.5
archivo=open("prueba4.txt","w")

while i<41:
  
   
    n = excel.main(float(v+0.1*i),0)
    n = int(n)
    mcpras.set_value(n)
    P1=Node611.sensorm()
    archivo.write(str(P1)+'\n')
    i=i+1
    time.sleep(1)
    
    
    
archivo.close()

                  
