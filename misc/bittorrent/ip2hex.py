# For generating the IP data which could be wrote to the dht.dat
import re
data = input("ip:port> ")
data = re.split('\.|\:',data)
data = list(map(int, data))
if len(data) != 5:
    raise Exception("Data length Error, for ipv4 only")
for i in range(4):
    if data[i] not in range(256):
        raise Exception("invalid IP")
if data[4] not in range(65536):
    raise Exception("invalid port")
print(data)
print("%02x %02x %02x %02x %02x %02x" % (data[0], data[1], data[2], data[3], (data[4]&0xff00)>>8, data[4]&0xff))