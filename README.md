# DNS Spoofer

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  ![Kali](https://img.shields.io/badge/Kali-268BEE?style=for-the-badge&logo=kalilinux&logoColor=white)  ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

This Python script allows you to perform DNS spoofing by intercepting DNS packets and modifying their responses. It utilizes the `netfilterqueue` library to capture and manipulate network traffic

## Prerequisites
Before running the script, make sure you have the following prerequisites installed:
- Python 3.xx
- `scapy` library
- `netfilterqueue` library
You can install the required libraries using pip:
```bash
$ pip install scapy netfilterqueue
```
or if `netfilterqueue` not installed properly, try this:
```bash
$ sudo pip3 install --upgrade -U git+https://github.com/kti/python-netfilterqueue
```
## Usage
```commandline
$ python3 dns_spoofer.py --host <IP_ADDRESS> --queue-num <QUEUE_NUMBER> --domain <DOMAIN_NAME>
```

## Options
- `--host`: Specify the IP address for your fake DNS server.
- `--queue-num`: Specify the queue number to trap the sniffed packets.
- `--domain`: Specify the domain name that you want to spoof its IP.

## Example usage:
- Run your script and provide the `queue-num` to the one that you specified before in the command above:
```commandline
$ python3 dns_spoofer.py --host 192.168.152.157 --queue-num 7 --domain www.bing.com
```

## Screenshots
- **Kali linux (Hacker machine)**<br><br>
![](https://github.com/SaherMuhamed/dns-spoofer-tool/blob/master/screenshots/Screenshot%202023-12-29%20183356.png)<br><br>
![](https://github.com/SaherMuhamed/dns-spoofer-tool/blob/master/screenshots/Screenshot%202023-12-29%20183429.png)<br><br>
- **Ubuntu (Spoofed target)**<br><br>
![](https://github.com/SaherMuhamed/dns-spoofer-tool/blob/master/screenshots/Screenshot%202023-12-29%20183450.png)

## Important Note
To run this script, you need `root privileges` since it involves manipulating network traffic. Make sure to run it with administrative rights.

## Acknowledgments
This script is provided for educational purposes only. Use it responsibly and at your own risk.

**Disclaimer:** This script should only be used on networks that you have permission to test or for educational purposes on your own network. Unauthorized use is illegal and unethical.

---
### Updates
`v1.0.3 - 29/12/2023`
- improve DNS spoofing functionality
- increase verbose output to user
  
