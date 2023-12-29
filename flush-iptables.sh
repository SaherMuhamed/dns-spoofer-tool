#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "[-] Please run this script as root"
    exit 1
fi

# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Flush all existing rules
iptables --flush
iptables --table nat --flush

# Delete user-defined chains
iptables -t filter -X
iptables -t nat -X

# Delete all rules in the filter and nat tables
iptables -t filter --delete-chain
iptables -t nat --delete-chain

# Set default policies
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

echo "[+] All iptables rules and chains have been properly deleted."
