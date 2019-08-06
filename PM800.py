from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu', port= '/dev/ttyUSB0', baudrate= 19200)

if client.connect():
    
    print("puerto abierto")
else:
    print("puerto no abierto")

pmC1 = client.read_holding_registers(1100, 1, unit=2)#Current A 1100

C1 = pmC1.registers[0]/1000

print(C1)
