import socket
from n611_adquisicion import *
from FuzzyControl4 import Estados
print("Pase por Fuzzy")
import time
from datetime import datetime
from datetime import timedelta

state=1
to5=True
UDP_IP = "3.89.222.210"
UDP_PORT = 5000
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

def SendData():
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP

#    MESSAGE = str(adquisicion())
    try:
        now = datetime.now()
        fecha = now.strftime('%Y-%m-%d')
        hora = time.strftime("%H:%M:%S")
        ADQ=adquisicion()
        ADQ=str(ADQ)
        ADQ=ADQ[1:len(ADQ)-1]
        MESSAGE = ADQ+', ' + fecha +', '+ hora + state
        MESSAGE = bytes(MESSAGE)
        print("message:", MESSAGE)
	print("Si es")
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    except socket.error:
        print "Error de Conexion, reintentando..."
        time.sleep(1)
    time.sleep(5)
    
    return sock
        
def ReceiveData(sock):
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print ("received message:", data)

    if (data=="True"):
        to5=True
    else:
        to5=False
    
while True:
    Estados(state,to5)	
    print("send")	
    sock=SendData()
    ReceiveData(sock)
    
