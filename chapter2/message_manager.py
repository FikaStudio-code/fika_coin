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
cmd_list = [MSG_TX, MSG_BLOCK, MSG_CHAIN, MSG_TEST]

class MessageManager:
    def __init__(self):
        print("Hello, MM")

    def build(self, sender, msg_type, payload):
        message = {
            "from": sender,
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
        dict_data = json.loads(data_sum)
        if dict_data["msg_type"] in cmd_list:
            return ("OK", dict_data["from"], dict_data["msg_type"], dict_data["payload"])
        else:
            return ("NO", "", "", "")
