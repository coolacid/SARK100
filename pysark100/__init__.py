#!/usr/bin/env python3
import serial
import math
from tqdm import tqdm
from pysark100.collector import Sark100Collector
from pysark100.bands import bands, generate_band_frequencies

class sark100Scan:
    data_values = ['swr', 'r', 'x', 'z']

    def __init__(self, parent, start, end, step=1000, progress=True):
        self.device = parent.device
        self.data = Sark100Collector()
        self.step = step
        self.start = start
        self.cur_freq = start
        self.end = end + step
        self.progress = progress
        if self.progress:
            total = math.ceil(((end - start) / step))
            self.pbar = tqdm(total=total)

        self.device.write(f"scan {start} {end} {step}\r\n".encode())

    def _ensure_full(self):
        while self.cur_freq < self.end:
            try:
                self.__next__()
            except StopIteration:
                break

    def get_dataframe(self):
        self._ensure_full()
        return self.data.df

    def plot(self, *args, **kwargs):
        self._ensure_full()
        self.data.plot(*args, **kwargs)

    def plot_interactive(self, *args, **kwargs):
        self._ensure_full()
        self.data.plot_interactive(*args, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            data = self.device.readline().decode('utf-8').strip()

            # If we're run over just stop the Iteration
            if self.cur_freq > self.end:
                raise StopIteration

            # We skip responses we don't care about
            if data in ["Start", "", ">>"]:
                continue

            # The SARK100 has said it's ended it's data
            if data == "End":
                self.cur_freq += self.step
                if self.progress:
                    self.pbar.close()
                raise StopIteration

            # The SARK100 has said there's been an error, so raise an error
            if "Error" in data:
                print(data)
                raise StopIteration

            # We've got data, break out of our loop
            break

        if self.progress:
            self.pbar.update(1)
            self.pbar.set_postfix({"Freqency": self.cur_freq})

        self.data.add_measurement(self.cur_freq, data)
        self.cur_freq += self.step
        return dict(zip(self.data_values, data.split(",")))

class sark100:
    def __init__(self, port='/dev/ttyUSB0'):
        self.device = serial.Serial(
                port=port,  # Replace with your port name (e.g., 'COM1' on Windows)
                baudrate=57600,
                bytesize=8,
                timeout=5,
                stopbits=serial.STOPBITS_ONE
        )

    def scan(self, start, end, step = 1000, progress=False):
        total = math.ceil(((end - start) / step))
        print(f"Getting data between {start} and {end} with a step of {step} for a total of {total} data points.")
        return sark100Scan(self, start, end, step)

    def scan_band(self, band, buffer_pct=0.15, step=1000, progress=False):
        freq_list = generate_band_frequencies(band, buffer_pct=buffer_pct, step_hz=step)
        return self.scan(freq_list[0], freq_list[-1], step, progress=progress)

    def __end__(self):
        self.device.close()
