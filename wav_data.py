from scipy.io import wavfile
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np

# Signal durations in microseconds
class BitDuration(Enum):
    ZERO = 640
    ONE = 320


# Represents data stored in wav file along with its properties of interest
class WavData:
    def __init__(self, file_name):
        self.file_name = file_name
        self.samplerate, self.data = wavfile.read(file_name)
        
        self.num_channels = self.data.shape[1]
        self.samples_count = self.data.shape[0]

        # Sample duration in microseconds
        self.sample_micro_sec = 1 / self.samplerate * 1000000;
        self.length_sec = self.samples_count / self.samplerate

        print(f"sample rate = {self.samplerate}, sample duration = {self.sample_micro_sec} μs")
        print(f"length = {self.length_sec} s")

    def draw(self):
        zoom = 200
        samples_in_zoom = int(self.samples_count / zoom)
        start_time = 2.5 * 1000 * 1000
        time = np.linspace(start_time, self.length_sec / zoom, samples_in_zoom)
        plt.plot(time, self.data[:samples_in_zoom, 0], label="Left channel")
        plt.plot(time, self.data[:samples_in_zoom, 1], label="Right channel")
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()


if __name__ == '__main__':
    wav = WavData('wav/file_1.wav')
    wav.draw()