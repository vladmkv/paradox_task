from enum import Enum
import logging
from wav_data import WavData
from byte_parser import ByteParser

MAX_MSG_LEN = 4000

# Signal duration in microseconds
DURATION_BOUND = 480

# Ignore samples less than threshold
SAMPLE_THRESHOLD = 1000

from enum import Enum
class State(Enum):
    SILENCE = 1,
    LEAD_TONE = 2

class BitAccumulator:
    def __init__(self):
        self.current_bits = list()
        self.bytes = bytearray([0] * MAX_MSG_LEN)
        self.bytes_count = 0
        self.state = State.SILENCE

    def addBit(self, bit):
        if self.state == State.SILENCE:
            if bit == 1:
                self.state = State.LEAD_TONE
                # Missed start bit
                self.current_bits.append(0)
        if self.state == State.LEAD_TONE:
            self.decodeBit(bit)

    def decodeBit(self, bit):
        self.current_bits.append(bit)
        if len(self.current_bits) == 11:
            # Check control bits
            control_bits_ok = \
                self.current_bits[0] == 0 and \
                self.current_bits[9] == 1 and \
                self.current_bits[10] == 1
            if not control_bits_ok:
                raise Exception('Control bits incorrect')
            byte = 0
            for bit in self.current_bits[8:0:-1]:
                byte = (byte << 1) + bit
            self.bytes[self.bytes_count] = byte
            self.bytes_count = self.bytes_count + 1
            self.current_bits.clear()

class SampleProcessor:
    def __init__(self):
        # Current bit
        self.bit = 0
        self.bit_start = 0
        self.sign = 0
        self.bits = BitAccumulator()
        pass

    def addSample(self, sample, time):
        sample_value = int(sample)

        amp = abs(sample_value)
        if amp < SAMPLE_THRESHOLD:
            logging.info(f'Sample dropped: {amp}')
            return

        new_sign = 1 if sample_value > 0 else -1

        # Always process first sample and initialize sign
        if self.sign == 0:
            self.bit_start = time
            self.sign = new_sign
        elif new_sign != self.sign:
            # Signal flipped. Determine & store previous bit
            bit_duration = time - self.bit_start
            bit = 1 if bit_duration < DURATION_BOUND else 0

            if bit == 0:
                pass

            self.bits.addBit(bit)
            # Start next bit
            self.bit_start = time
            self.sign = new_sign

class PdxDecoder:
    def __init__(self):
        pass

    def decode(self, wav_data):
        print(f'Decoding {wav_data.file_name}')

        # Work with one channel of stereo sound
        channel = wav_data.data[:, 0]

        processor = SampleProcessor()

        for sample_index in range(0, wav_data.samples_count):
            time = sample_index * 1000 * 1000 / wav_data.sample_rate
            sample = channel[sample_index]
            processor.addSample(sample, time)

        logging.info(f'Raw bytes decoded: {processor.bits.bytes_count}')

        parser = ByteParser(processor.bits.bytes)
        parser.parseStream()

        print(f'{parser.text} ({len(parser.text)} payload bytes)\n\n')

if __name__ == '__main__':
    logging.basicConfig(filename='decoder.log', filemode='w', encoding='utf-8', level=logging.DEBUG)
    decoder = PdxDecoder()

    for i in range(1, 4):
        decoder.decode(WavData(f'wav/file_{i}.wav'))
