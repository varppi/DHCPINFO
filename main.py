import argparse
import blessed
import os
import sys
import multiprocessing
from array import *
from multiprocessing import Process, Queue
import time

from libs import DHCPDiscover
from libs import DHCPSniff
from libs import log

def main():
    t = blessed.Terminal()
    print(f"""{t.red}
██████╗ ██╗  ██╗ ██████╗██████╗ ██╗███╗   ██╗███████╗ ██████╗ 
██╔══██╗██║  ██║██╔════╝██╔══██╗██║████╗  ██║██╔════╝██╔═══██╗
██║  ██║███████║██║     ██████╔╝██║██╔██╗ ██║█████╗  ██║   ██║
██║  ██║██╔══██║██║     ██╔═══╝ ██║██║╚██╗██║██╔══╝  ██║   ██║
██████╔╝██║  ██║╚██████╗██║     ██║██║ ╚████║██║     ╚██████╔╝
╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝   
                                              {t.purple}- @SpoofIMEI{t.normal}

""")

    try:
        if os.getuid() != 0:
            log.msg("Script must be run as root!", "error")
            sys.exit(0)
    except:
        pass

    settings = Queue()
    sniffer  = multiprocessing.Process(target=DHCPSniff.sniffdhcp, args=(settings,))
    sniffer.start()
    log.msg("Sniffer started", "info")

    time.sleep(0.5)
    
    DHCPDiscover.discover()
    log.msg("DHCP Discover sent", "info")

    log.msg("Waiting for reply...", "info")
    settings = settings.get()
    log.msg("DHCP Settings received:", "success")
    for setting in settings:
        settingL = [setting[0], setting[1]]
        if type(settingL[1]) == bytes:
            settingL[1] = settingL[1].decode()
    
        log.msg(f"-> {settingL[0]}: {settingL[1]}", "success")
    
    sniffer.kill()
    log.msg("Finished!", "info")
    

if __name__ == "__main__":
    main()