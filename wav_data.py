from scipy.io import wavfile
from enum import Enum

import logging

# Signal durations in microseconds
class BitDuration(Enum):
    ZERO = 640
    ONE = 320


# Represents data stored in wav file along with its properties of interest
class WavData:
    def __init__(self, file_name):
        logging.info(f'Loading {file_name}')

        self.file_name = file_name
        self.sample_rate, self.data = wavfile.read(file_name)
        
        self.num_channels = self.data.shape[1]
        self.samples_count = self.data.shape[0]

        # Sample duration in microseconds
        self.sample_micro_sec = 1 / self.sample_rate * 1000000;
        self.length_sec = self.samples_count / self.sample_rate

        logging.info(f'sample rate = {self.sample_rate}, sample duration = {self.sample_micro_sec} μs')
        logging.info(f'length = {self.length_sec} s')
