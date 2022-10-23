from scapy.all import IP, sr1, ICMP, ARP, Ether, srp, getmacbyip, TCP, sr
import random
import datetime

date_time = datetime.datetime.now()
file_name = "Report of {}".format(date_time)
print(file_name)
file = open("data.txt", "w")
start_address = input("Please enter the address without the bytes you want to iterate over : ")
src_address = input("Please enter the source address (the address must be in the specified network) : ")
#src_address = "192.168.121.4"


def decode_binary_string(s):
    return bytes(s).decode("ascii")


for ping in range(3, 7):

    file.write("\n__________________________\n")
    address = start_address + str(ping)
    if address == src_address:
        file.write("Adresse IP : " + str(address) + "\n")
        arp_request = ARP(pdst=address)
        #file.write(str(arp_request)+ "\n")
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        file.write(str(answered_list) + "\n")
        mac = getmacbyip(address)
        file.write("Address MAC : " + str(mac))
        res = sr1(IP(dst=address, src=src_address)/ICMP(), timeout=5)
        resFr = decode_binary_string(res)
        print(resFr)
        file.write("\n" + str(resFr))
        if res:
            file.write("\nHost is up")
            #port_range = [22, 23, 80, 443, 3389]
            input_range = input("Please enter a list of ports to test separated by space :")
            port_range  = input_range.split()
            file.write("\nMain port states :\n")

            for dst_port in port_range:
                res = ""
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
                        file.write(f"{address}'s OS is Windows")

                elif(resp.haslayer(ICMP)):
                    if(
                        int(resp.getlayer(ICMP).type) == 3 and
                        int(resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]
                    ):
                        file.write(
                            f"\n{address}:{dst_port} is filtered (silently dropped).")
                elif (dst_port == 22) and (res == "dropped"):
                    file.write(f"{address}'s is Linux.")
        else:
            file.write("\nHost is down")


# print(file.read())
file.close()

# if address == address src ne pas faire l'itération
