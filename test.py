import sys
import binascii
import struct
import time
from bluepy.btle import UUID, Peripheral

env_sens_service_uuid = "42821a40-e477-11e2-82d0-0002a5d5c51b"
temp_char_uuid = "a32e5520-e477-11e2-a9e3-0002a5d5c51b"
hum_char_uuid    = "01c50b60-e48c-11e2-a073-0002a5d5c51b"

time_service_uuid = "08366e80-cf3a-11e1-9ab4-0002a5d5c51b"
time_char_uuid = "09366e80-cf3a-11e1-9ab4-0002a5d5c51b"
minute_char_uuid = "0a366e80-cf3a-11e1-9ab4-0002a5d5c51b"

if len(sys.argv) != 2:
  print("Fatal, must pass device address:", sys.argv[0], "<device address="">")
  quit()

p = Peripheral(sys.argv[1], "public")
EnvSensService=p.getServiceByUUID(env_sens_service_uuid)
TimeService=p.getServiceByUUID(time_service_uuid)

try:
    ch = EnvSensService.getCharacteristics(temp_char_uuid)[0]
    ch2 = EnvSensService.getCharacteristics(hum_char_uuid)[0]

    ch3 = TimeService.getCharacteristics(time_char_uuid)[0]
    ch4 = TimeService.getCharacteristics(minute_char_uuid)[0]
    if (ch.supportsRead() and ch2.supportsRead()):
        while 1:
            val =  binascii.b2a_hex(ch.read())
            val = val.decode("utf-8")
            val = val[:2]
            val = int(val, 16)
            print("Temperature : " + str(val) + "°C")
            val2 =  binascii.b2a_hex(ch2.read()) 
            val2 = val2.decode("utf-8")
            val2 = val2[:2]
            val2 = int(val2, 16)
            print("Humidity : " + str(val2) + "%")
            val3 = binascii.b2a_hex(ch3.read())
            val3 = val3.decode("utf-8")
#val3 = val3[5:]
            val3 = int(val3, 16)
            print("Active time : " + str(val3) + "s")
            val4 = binascii.b2a_hex(ch4.read())
            val4 = val4.decode("utf-8")
#val4 = val4[5:]
            val4 = int(val4, 16)
            print("Active minute : " + str(val4) + "m")
            time.sleep(1)

finally:
    p.disconnect()
