import signal
import time
import pprint
import random

WATCHDOG_TIMEOUT = 60 #seconds
UNBLOCK_INTERVAL = 30 #seconds

class DummyStdoutBlocker:
    def __init__(self):
        pass

    def block_many(self, records):
        for r in records:
            print time.ctime(), "block", r['cidr']
            pprint.pprint(r)

    def unblock_many(self, records):
        for r in records:
            print time.ctime(), "unblock", r['block']['cidr']

class BlockManager:
    def __init__(self, client, blocker):
        self.client = client
        self.blocker = blocker

    def do_block(self):
        records = self.client.get_block_queue(timeout=UNBLOCK_INTERVAL+2)
        if records:
            self.blocker.block_many(records)
            self.client.set_blocked(records)
        return bool(records)

    def do_unblock(self):
        records = self.client.get_unblock_queue()
        if records:
            self.blocker.unblock_many(records)
            self.client.set_unblocked(records)
        return bool(records)

    def run_once(self):
        did = self.do_unblock()
        did = did or self.do_block()
        return did

    def run(self):
        """Run the blocker, blocking and unblocking as needed"""
        since_unblock = 0
        while True:
            blocked = unblocked = False
            signal.alarm(WATCHDOG_TIMEOUT)
            if time.time() - since_unblock > UNBLOCK_INTERVAL:
                unblocked = self.do_unblock()
                since_unblock = time.time()
            blocked = self.do_block()
            if not (blocked or unblocked):
                time.sleep(0.1)

# Is ./block_manager.py able to contact 192.168.56.101:8000?
# It's not trying.
# If so, why is it not implementing blocks?
