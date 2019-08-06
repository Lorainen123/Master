from pymodbus.client.sync import ModbusSerialClient as ModbusClient


client = ModbusClient(method='rtu', port= '/dev/ttyUSB0', bytesize=8, timeout=1, baudrate= 9600)
if client.connect():
    
    print("puerto abierto")
else:
    print("puerto no abierto")

pmC1 = client.read_holding_registers(11730, 2, unit=1)#Current A 1100

C1 = pmC1.registers[0]

print(C1)
