from scapy.all import IP, sr1, ICMP, ARP, Ether, srp

for ping in range(3, 5):
    print("__________________________")
    address = "192.168.121." + str(ping)
    print(str(address))
    arp_request = ARP(pdst=address)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    print(str(answered_list))
    res = sr1(IP(dst=address, src='192.168.121.6')/ICMP(), timeout=5)

