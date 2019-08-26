# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 13:43:09 2019

@author: jzapa
"""

import socket
from n611_adquisicion import *

HOST = '10.20.14.106' # Enter IP or Hostname of your server
PORT = 5040 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#Lets loop awaiting for your input
while True:
	#command = input('Ent1er your command: ')
    Datos="b"+str(adquisicion())
	s.sendall(Datos)
	reply = s.recv(1024)
	if reply == 'Terminate':
		break
	print (reply)