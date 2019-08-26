import sys
import socket
from message_manager import MessageManager

def main():
    client_socket()

def client_socket():
    ip = sys.argv[-2]
    port = int(sys.argv[-1])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.3", 11111))
    message = make_tx()
    mm = MessageManager()
    test_message = mm.build(ip, "TEST", message)
    s.send(test_message.encode())
    s.close()

def make_tx():
    tx = {
        "sender": "Alice",
        "amount": 10,
        "fee": 1,
    }
    return tx

if __name__ == "__main__":
    main()
