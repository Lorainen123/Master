from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu', port= '/dev/ttyUSB09', bytesize=8, timeout=1, baudrate= 9600)

if client.connect():
    
    print("puerto abierto")
