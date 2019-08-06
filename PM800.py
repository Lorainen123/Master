from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu', port= '/dev/ttyUSB09', bytesize=8, timeout=1, baudrate= 19600)
client.connect()
print(client)
