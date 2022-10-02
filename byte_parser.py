import logging

LEADER_BYTES_COUNT = 652

ID_BYTE_1 = 0x42
ID_BYTE_2 = 0x03

MSG_COUNT = 64
MSG_LEN = 30
PAYLOAD_LEN = MSG_COUNT * MSG_LEN


class ByteParser:
    def __init__(self, bytes):
        self.input_bytes = bytes
        self.messages = list()
        self.current_message = list()
        self.block = list()
        self.text = str()

    def parseStream(self):
        pos = 0
        while self.input_bytes[pos] != ID_BYTE_1:
            pos = pos + 1

        if pos != LEADER_BYTES_COUNT:
            logging.error(f'Leader length incorrect: {pos}')

        pos = pos + 1
        if self.input_bytes[pos] != ID_BYTE_2:
            logging.error('Header error')
            return

        pos = pos + 1
        for i in range(0, MSG_COUNT):
            last_pos = pos + MSG_LEN
            message = self.input_bytes[pos: last_pos]
            checksum = self.input_bytes[last_pos]
            if not verifyMessage(message, checksum):
                return
            pos = last_pos + 1
            self.block.extend(list(message))

        if self.input_bytes[pos] == 0:
            logging.info('Terminator OK')

        payload_bytes = bytearray(self.block)
        self.text = payload_bytes.decode('ascii')

def verifyMessage(message, checksum):
    actual_checksum = sum(message) % 256
    return checksum == actual_checksum


