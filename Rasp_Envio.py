import socket
from n611_adquisicion import *
import time
from datetime import datetime


UDP_IP = "190.143.58.202"
UDP_PORT = 5013

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
while True:
#    MESSAGE = str(adquisicion())    
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d')
    hora = time.strftime("%H:%M:%S")

    MESSAGE = str(adquisicion())+', ' + fecha +', '+ hora
    MESSAGE = bytes(MESSAGE,'utf-8')
    print("message:", MESSAGE)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    
