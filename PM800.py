from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu', port= '/dev/ttyUSB8', bytesize=8, timeout=1, baudrate= 9600)
client.connect()
print(client)
