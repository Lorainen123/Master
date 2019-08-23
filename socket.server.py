# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 13:22:35 2019

@author: jzapa
"""

import socket
import random
from n611_adquisicion import *

pot=adquisicion()
HOST = '192.168.1.102' # Server IP or Hostname
PORT = 7680 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

#managing error exception
try:
	s.bind((HOST, PORT))
except socket.error:
	print 'Bind failed '

s.listen(5)
print 'Socket awaiting messages'
(conn, addr) = s.accept()
print 'Connected'

# awaiting for message
while True:
	data = conn.recv(1024)
	print data
    
	reply = ''

	# process your message
	if data == 'Potencia':
		reply = str(pot)
        
	elif data == 'Voltaje':
		reply = 'Tampoco se'

	#and so on and on until...
	elif data == 'quit':
		conn.send('Terminating')
		break
	else:
		reply = 'Unknown command'

	# Sending reply
	conn.send(reply)
conn.close() # Close connections
