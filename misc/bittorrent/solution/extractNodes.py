from datetime import datetime
import socket

with open("dht.dat","rb") as f:
    data = f.read()

timestamp = int.from_bytes(data[0x8:0x8+8],'big')

print("File info")
print("Date: %u (%s)" % (timestamp, datetime.fromtimestamp(timestamp)))
print("Node count:", data[0x33])

ip = [] # str list
port =[] # int list

node_data = data[0x38:]
for i in range(0,len(node_data),0x70-0x38):
    if node_data[i] != 6:
        raise Exception("error")
    ip.append(socket.inet_ntop(socket.AF_INET, node_data[i+8:i+12]))
    port.append(int.from_bytes(node_data[i+12:i+14],"big"))

#print(ip)
#print(port)
print("Exporting nodes to ip.txt as nmap format")

with open("ip.txt",'w+') as f:
    for i in range(data[0x33]):
        f.write(str.format("%s -p %u\n" % (ip[i], port[i])))

print("Done")