from scapy.all import IP, sr1, ICMP, ARP, Ether, srp, getmacbyip, TCP, sr
import random
import datetime
import time
import tqdm

date_time = datetime.datetime.now()
file_name = "Rapport du {}".format(date_time)
print(file_name)
#fichier = open("data.txt", "a")

for i in tqdm(range(100)):
    time.sleep(0.001)

for ping in range(3, 7):
    print("__________________________")
    address = "192.168.121." + str(ping)
    print(str(address))
    arp_request = ARP(pdst=address)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    print(str(answered_list))
    mac = getmacbyip(address)
    print(str(mac))
    res = sr1(IP(dst=address, src='192.168.121.4')/ICMP(), timeout=5)
    if res: 
        print("Host is up")
        port_range = [22, 23, 80, 443, 3389]

        for dst_port in port_range:
            src_port = random.randint(1025,65534)
            resp = sr1(
            IP(dst=address)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=1,
            verbose=0,
        )

            if resp is None:
                print(f"{address}:{dst_port} is filtered (silently dropped).")

            elif(resp.haslayer(TCP)):
                if(resp.getlayer(TCP).flags == 0x12):
                    send_rst = sr(
                        IP(dst=address)/TCP(sport=src_port,dport=dst_port,flags='R'),
                        timeout=1,
                        verbose=0,
                    )
                    print(f"{address}:{dst_port} is open.")

                elif (resp.getlayer(TCP).flags == 0x14):
                    print(f"{address}:{dst_port} is closed.")

            elif(resp.haslayer(ICMP)):
                if(
                    int(resp.getlayer(ICMP).type) == 3 and
                    int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]
                ):
                    print(f"{address}:{dst_port} is filtered (silently dropped).")

# if address == address src ne pas faire l'itération