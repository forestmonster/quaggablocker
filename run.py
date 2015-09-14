from bhr_client.rest import login_from_env
from bhr_client.block_manager import BlockManager, DummyStdoutBlocker
import quaggablocker

def main():
    client = login_from_env()
    #blocker = DummyStdoutBlocker()
    blocker = quaggablocker.QuaggaBlocker()
    m = BlockManager(client, blocker)
    m.run()

if __name__ == "__main__":
    main()
