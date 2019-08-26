import sys
import signal
import socket
import json
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from message_manager import MessageManager

MSG_TEST = "TEST"
MSG_TX = "TX"
MSG_BLOCK = "BLOCK"
MSG_CHAIN = "CHAIN"

class NodeCore:
    def __init__(self):
        self.name = sys.argv[-1]
        with open("node_json.txt", "r") as f:
            info = json.loads(f.read())
        self.info = info[self.name]
        self.ip = self.info["My_IP"]
        self.port = 11111
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

    def broadcast(self, message, sender):
        for ip in self.info.values():
            sleep(1)
            if (ip != self.ip and ip != sender):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, 11111))
                s.send(message.encode())
                s.close()
            else:
                continue

    def __handle_message(self, conn):
        result, sender, msg_type, payload = self.mm.parse(conn)
        if result == "OK":
            if msg_type == "TEST":
                message = self.mm.build(self.ip, MSG_TEST, payload)
                self.broadcast(message, sender)
        else:
            print("ERROR")

    def __KeyboardInterruptHandler(self, signal, frame):
        print("\nCtrl+C!!!")
        sys.exit(0)



if __name__ == "__main__":
    NodeCore()
