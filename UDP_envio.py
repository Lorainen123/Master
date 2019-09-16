# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 23:41:53 2019

@author: jzapa
"""

import socket
from n611_adquisicion import *

UDP_IP = "3.222.161.155"
UDP_PORT = 5000

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
while True:
    MESSAGE = str(adquisicion())
    print "message:", MESSAGE
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
