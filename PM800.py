from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusSerialClient as ModbusClient




client = ModbusClient(method='rtu', port= '/dev/ttyUSB0', bytesize=8, timeout=1, baudrate= 9600)
if client.connect():
    
    print("puerto abierto")
else:
    print("puerto no abierto")

result = client.read_holding_registers(11729, 2, unit=1)#Current A 1100
decoder = BinaryPayloadDecoder.fromRegisters(result.registers,  Endian.Big, wordorder=Endian.Big)
print(decoder.decode_32bit_float())


#C1 = pmC1.registers[0]
#C2 = pmC1.registers[1]
#C3 = pmC1.registers[2]
#C4 = pmC1.registers[3]
#C5 = pmC1.registers[4]
#C6 = pmC1.registers[5]
#C7 = pmC1.registers[6]
#C8 = pmC1.registers[7]
#C9 = pmC1.registers[8]
#C10 = pmC1.registers[9]

#print(C1)
#print(C2)
#print(C3)
#print(C4)
#print(C5)
#print(C6)
#print(C7)
#print(C8)
#print(C9)
#print(C10)
