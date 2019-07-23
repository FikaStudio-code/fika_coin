import json

# Message Format(Default)
# {
#   "msg_type": STRING,
#   "payload": JSON(None),
# }

MSG_TEST = "TEST"
MSG_TX = "TX"
MSG_BLOCK = "BLOCK"
MSG_CHAIN = "CHAIN"

class MessageManager:
    def __init__(self):
        print("Hello, MM")

    def build(self, msg_type, payload):
        message = {
            "msg_type": msg_type,
            "payload": payload,
        }
        return json.dumps(message, sort_keys = True, indent = 4)

    def parse(self, conn):
        data_sum = ""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data_sum += data.decode()
        print(data_sum)
