from scapy.all import IP, sr1, ICMP, ARP, Ether, srp, getmacbyip, TCP, sr
import random
import datetime

date_time = datetime.datetime.now()
file_name = "Rapport du {}".format(date_time)
print(file_name)
file = open("data.txt", "w")

for ping in range(3, 7):
    file.write("\n__________________________\n")
    address = "192.168.121." + str(ping)
    file.write("Adresse IP : " + str(address) + "\n")
    arp_request = ARP(pdst=address)
    #file.write(str(arp_request)+ "\n")
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    file.write(str(answered_list) + "\n")
    mac = getmacbyip(address)
    file.write( "Adresse MAC : " + str(mac))
    res = sr1(IP(dst=address, src='192.168.121.4')/ICMP(), timeout=5)
    #file.write("\n" + str(res, encoding="utf-8"))
    if res: 
        file.write("\nHost is up")
        port_range = [22, 23, 80, 443, 3389]
        file.write("\nEtats des ports principaux :")

        for dst_port in port_range:
            src_port = random.randint(1025,65534)
            resp = sr1(
            IP(dst=address)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=1,
            verbose=0,
        )

            if resp is None:
                file.write(f"\n{address}:{dst_port} is filtered (silently dropped).")

            elif(resp.haslayer(TCP)):
                if(resp.getlayer(TCP).flags == 0x12):
                    send_rst = sr(
                        IP(dst=address)/TCP(sport=src_port,dport=dst_port,flags='R'),
                        timeout=1,
                        verbose=0,
                    )
                    file.write(f"\n{address}:{dst_port} is open.")

                elif (resp.getlayer(TCP).flags == 0x14):
                    file.write(f"\n{address}:{dst_port} is closed.")

            elif(resp.haslayer(ICMP)):
                if(
                    int(resp.getlayer(ICMP).type) == 3 and
                    int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]
                ):
                    file.write(f"\n{address}:{dst_port} is filtered (silently dropped).")
    else :
        file.write("\nHost is down")



#print(file.read())
file.close()

# if address == address src ne pas faire l'itération