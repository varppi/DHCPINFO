from scapy.all import *
import sys

from libs import log 


def discover():
    ETHL   = Ether(dst='ff:ff:ff:ff:ff:ff', src="00:00:00:00:00:00", type=0x0800) 
    IPL    = IP(src='0.0.0.0', dst='255.255.255.255')
    UDPL   = UDP(dport=67,sport=68) 
    BOOTPL = BOOTP(op=1, chaddr="00:00:00:00:00:00")
    DHCPL  = DHCP(options=[('message-type','discover'), ('end')])
    packet = ETHL/IPL/UDPL/BOOTPL/DHCPL
    try:
        sendp(packet, verbose=False)
    except Exception as errno:
        log.msg(str(errno), "error")
        sys.exit(0)