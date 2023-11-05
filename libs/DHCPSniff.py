from scapy.all import *
import sys

from libs import log


def sniffer(packet):
    if packet.haslayer(BOOTP):
        if packet[BOOTP].op == 2:
            settingsQueue.put(packet[DHCP].options)

def sniffdhcp(settingsQueueL):
    globals()["settingsQueue"] = settingsQueueL
    try:
        sniff(prn=sniffer)
    except Exception as errno:
        log.msg("Note: script must be run as root!", "info")
        log.msg(str(errno), "error")
        sys.exit(0)