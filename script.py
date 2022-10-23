from scapy.all import IP, sr1, ICMP, ARP, Ether, srp, getmacbyip, TCP, sr
import random
import datetime

# Log file
date_time = datetime.datetime.now()
file_name = "Report of {}".format(date_time)
print(file_name)
file = open(file_name+".txt", "w")

# Dest address
# start_address = input("Please enter the host address : ")
''' if start_address[-1] != ".":
    start_address += "." '''
start_address = '192.168.121.0'
#src_address = input("Please enter the source address (the address must be in the specified network) : ")
src_address = "192.168.121.4"

# Dest network mask
mask = 0
while mask <= 0 or mask >= 32:
    mask = int(
        input("Please enter the remote newtork mask value (e.g 16 for X.X.X.X/16) : "))

# Ports to test
input_range = input(
    "Please enter a list of ports to test separated by space : ")
str_range = input_range.split()
port_range = [int(i) for i in str_range]

# 4 parts of an IP (i.j.k.l)
splitted = start_address.split(".")
i = int(splitted[0])
j = int(splitted[1])
k = int(splitted[2])
l = int(splitted[3]) +1

for iteration in range(l, 1012*(1-(mask/32))+1):
    address = f"{i}.{j}.{k}.{l}"
    print(address)

    if address != src_address:
        file.write("\n__________________________\n")
        file.write("Adresse IP : " + address + "\n")
        arp_request = ARP(pdst=address)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        file.write(str(answered_list) + "\n")
        mac = getmacbyip(address)
        file.write("Address MAC : " + str(mac))
        res = sr1(IP(dst=address, src=src_address)/ICMP(), timeout=5)
        if res:
            file.write("\nHost is up")

            # OS Detection
            osPacket = sr1(IP(dst=address, src=src_address)/TCP())
            if (osPacket.haslayer("IP")):
                ttl = osPacket["IP"].ttl
                if (ttl == 60):
                    file.write("OS : MacOS\n")
                elif (ttl == 64):
                    file.write("OS : Linux\n")
                elif (ttl == 128):
                    file.write("OS : Windows\n")

            # Opened ports detection
            file.write("\nMain port states :\n")
            for dst_port in port_range:
                os = ""
                src_port = random.randint(1025, 65534)
                resp = sr1(
                    IP(dst=address)/TCP(sport=src_port, dport=dst_port, flags="S"), timeout=1,
                    verbose=0,
                )

                if resp is None:
                    file.write(
                        f"{address}:{dst_port} is filtered (silently dropped).\n")
                    res = "dropped"

                elif(resp.haslayer(TCP)):
                    if(resp.getlayer(TCP).flags == 0x12):
                        send_rst = sr(
                            IP(dst=address)/TCP(sport=src_port,
                                                dport=dst_port, flags='R'),
                            timeout=1,
                            verbose=0,
                        )
                        file.write(f"{address}:{dst_port} is open.\n")
                        res = "open"

                    elif (resp.getlayer(TCP).flags == 0x14):
                        file.write(f"{address}:{dst_port} is closed.\n")
                        res = "closed"

                elif(resp.haslayer(ICMP)):
                    if(
                        int(resp.getlayer(ICMP).type) == 3 and
                        int(resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]
                    ):
                        file.write(
                            f"\n{address}:{dst_port} is filtered (silently dropped).")
        else:
            file.write("\nHost is down")
    l += 1
    if (l >= 253):
        l = 0
        k += 1
    if (k >= 255):
        k = 0
        j += 1
    if (j >= 255):
        j = 0
        i += 1

file.close()
