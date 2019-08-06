from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu', port= '/dev/ttyUSB0', bytesize=8, timeout=1, baudrate= 9600)

if client.connect():
    
    print("puerto abierto")
else:
    print("puerto no abierto")
