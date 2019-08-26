# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 23:41:53 2019

@author: jzapa
"""

import socket
from n611_adquisicion import *

UDP_IP = "10.20.59.8"
UDP_PORT = 5040
MESSAGE = str(adquisicion())

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))