#!/usr/local/bin/python
"""Implements RTBH blocking methods for Quagga's Zebra daemon.
"""
import re, os, telnetlib
os.environ["PATH"] += os.pathsep + '/usr/local/lib/python2.7/site-packages/bhr_client'
from bhr_client.rest import login_from_env
from bhr_client.block_manager import BlockManager, DummyStdoutBlocker

QUAGGA_SERVER = '192.168.56.102'
PORT = '2601'
PASSWORD = 'quagga'
ENABLE_PASSWORD = 'quagga2'
WATCHDOG_TIMEOUT = 60 #seconds
UNBLOCK_INTERVAL = 30 #seconds

class QuaggaBlocker:
    """Adds to, and removes blocks from, Quagga's listening Zebra daemon."""

    def __init__(self):
        print "New instance of QuaggaBlocker class."

    def block_many(self, records):
        """Add an arbitrary number of blocks to Quagga.
        """
        #for record in records:
        #    print time.ctime(), "block", record["cidr"]
        print "Asked to block_many."

        try:
            tco = telnetlib.Telnet(QUAGGA_SERVER, PORT)
            tco.read_until("Password: ")
        except Exception, exception:
            print "Error connecting to Quagga at " + QUAGGA_SERVER + ":" + PORT
            raise exception
        else:
            print "Connected to Quagga at " + QUAGGA_SERVER + ":" + PORT
            tco.write(PASSWORD + "\n")
            tco.read_until("> ")
            tco.write("enable\n")
            print "enable"
            tco.read_until("Password: ")
            tco.write(ENABLE_PASSWORD + "\n")
            print "enable pass"
            tco.read_until("# ")
            tco.write("configure terminal\n")
            print "conf term"
            # Never want to see this:
            # freebsd-base# configure terminal
            # VTY configuration is locked by other VTY
            # freebsd-base#
            tco.read_until("(config)# ")
            for record in records:
                tco.write("ip route " + str(record['cidr']) + " Null0\n")
                tco.read_until("(config)# ")
                print "ip route " + str(record['cidr']) + " Null0"
            #tco.read_until("(config)# ")
            tco.write("write memory\n")
            print "write mem"
            tco.read_until("(config)# ")
            tco.write("exit\n")
            print "exit"
            tco.read_until("# ")
            tco.write("exit\n")
            print "exit"
            # We need to be sure.
            tco.close()
            print "tco.close()"
            print "------------------------------"
            # TODO: Send a syslog entry with the addresses blocked to the SIEM
            # of what we did. 15 addresses blocked.

    def unblock_many(self, records):
        """Remove an arbitrary number of blocks from Quagga.
        """
        # for record in records:
        #     print time.ctime(), "unblock", record["cidr"]
        print "Asked to unblock_many."
        try:
            tco = telnetlib.Telnet(QUAGGA_SERVER, PORT)
            tco.read_until("Password: ")
        except Exception, exception:
            print "Error connecting to Quagga at " + QUAGGA_SERVER + ":" + PORT
            raise exception
        else:
            print "Connected to Quagga at " + QUAGGA_SERVER + ":" + PORT
            tco.write(PASSWORD + "\n")
            tco.read_until("> ")
            tco.write("enable\n")
            print "enable"
            tco.read_until("Password: ")
            tco.write(ENABLE_PASSWORD + "\n")
            print "enable password"
            tco.read_until("# ")
            tco.write("configure terminal\n")
            print "conf term"
            tco.read_until("(config)# ")
            for record in records:
                tco.write("no ip route " + str(record['block']['cidr']) + " Null0\n")
                tco.read_until("(config)# ")
                print "no ip route " + str(record['block']['cidr']) + " Null0"
            #tco.read_until("(config)# ")
            tco.write("write memory\n")
            print "write mem"
            tco.read_until("(config)# ")
            tco.write("exit\n")
            print "exit"
            tco.read_until("# ")
            tco.write("exit\n")
            print "exit"
            # We need to be sure.
            tco.close()
            print "tco.close()"
            print "------------------------------"

def getblocks():
    """Retrieves blocked addresses from a Quagga server running Zebra.

    :returns: list (IPv4 addresses)

    """
    # Issue Quagga commands using Telnet.
    tco = telnetlib.Telnet(QUAGGA_SERVER, PORT)
    tco.read_until("Password: ")
    tco.write(PASSWORD + "\n")
    tco.read_until("> ")
    tco.write("enable\n")
    tco.read_until("Password: ")
    tco.write(ENABLE_PASSWORD + "\n")
    tco.read_until("# ")
    tco.write("show running-config" + "\n")
    fullconfig = tco.read_until("end")
    tco.write("exit" + "\n")
    # (?<=...) positive lookbehind assertion
    # (?=...) positive lookahead assertion
    blocked = re.findall(
            r'(?<=ip route )(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?=\/32 Null0)',
            fullconfig, re.MULTILINE)
    tco.close()
    return blocked

def main():
    client = login_from_env()
    #blocker = DummyStdoutBlocker()
    blocker = QuaggaBlocker()
    m = BlockManager(client, blocker)
    m.run()

if __name__ == "__main__":
    main()
