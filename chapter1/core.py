import sys
import signal
import socket
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from message_manager import MessageManager

class NodeCore:
    def __init__(self):
        self.ip = sys.argv[-2]
        self.port = int(sys.argv[-1])
        self.mm = MessageManager()
        signal.signal(signal.SIGINT, self.__KeyboardInterruptHandler)
        self.__wait_access()

    def __wait_access(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(5)

        executor = ThreadPoolExecutor(max_workers = 5)

        while True:
            sleep(1)
            print("waiting connection...")
            conn, addr = s.accept()
            executor.submit(self.__handle_message, conn)

    def __handle_message(self, conn):
        self.mm.parse(conn)

    def __KeyboardInterruptHandler(self, signal, frame):
        print("\nCtrl+C!!!")
        sys.exit(0)



if __name__ == "__main__":
    NodeCore()
