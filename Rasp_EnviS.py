

from FuzzyControl4P import *
import time
from datetime import datetime
from datetime import timedelta
import threading

state1='1'
to5=True

import mysql.connector
        
mydb = mysql.connector.connect(
  host="db4free.net",
  user="baenav",
  passwd="qwertyuiop",
  database="proyecto_diseno"
)

mycursor = mydb.cursor()

def SendData(state1,mycursor,mydb):         
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d')
    hora = time.strftime("%H:%M:%S")
    sql = "INSERT INTO datos (P1, P2, P3, P4, fecha, hora, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    state1=state1
    ADQ=adquisicion()  
    val = (ADQ[0], ADQ[1], ADQ[2], ADQ[3],fecha, hora, state1)
    
    mycursor.execute(sql, val)
    
    mydb.commit()
    print("Subido")
    time.sleep(5)
    
        
def ReceiveData(mycursor):
    mycursor.execute("SELECT To5 FROM ToCinco ORDER BY id DESC LIMIT 1")
    data = mycursor.fetchone()
    data=str(data[0])
    print("To5= "+data)
    
    if data == '1':
        to5=True
    else:
        to5=False
    return to5
    
#x.start()    
while True:
    state1=Estados(state1,to5)    
    print("Sending")    
    SendData(state1,mycursor,mydb)
    to5=ReceiveData(mycursor)
