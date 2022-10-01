from enum import Enum
import numpy as np

from wav_data import WavData

MAX_MSG_LEN = 4000

# Signal duration in microseconds
DURATION_BOUND = 480

# Ignore samples less than threshold
SAMPLE_THRESHOLD = 10000

from enum import Enum
class State(Enum):
    SILENCE = 1,
    LEAD_TONE = 2,
    DATA = 3,
    END_BLOCK = 4

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
            print(self.current_bits)
            control_bits_ok = \
                self.current_bits[0] == 0 and \
                self.current_bits[9] == 1 and \
                self.current_bits[10] == 1
            if not control_bits_ok:
                raise Exception('Control bits incorrect')
            byte = 0
            for bit in self.current_bits[1:9]:
                byte = (byte << 1) + bit
            self.bytes[self.bytes_count] = byte
            print(byte)
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

        if abs(sample_value) < SAMPLE_THRESHOLD:
            print('sample dropeed')
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

# Represents data stored in wav file along with its properties of interest
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

        print(f'Raw bytes decoded: {processor.bits.bytes_count}')

if __name__ == '__main__':
    decoder = PdxDecoder()
    data = WavData('wav/file_1.wav')
    decoder.decode(data)