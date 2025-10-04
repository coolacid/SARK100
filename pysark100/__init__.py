#!/usr/bin/env python3
import serial
import math
from tqdm import tqdm
from pysark100.collector import Sark100Collector
from pysark100.bands import bands, generate_band_frequencies


class sark100:
    data_vaules = ['swr', 'r', 'x', 'z']

    def __init__(self, port='/dev/ttyUSB0'):
        self.device = serial.Serial(
                port=port,  # Replace with your port name (e.g., 'COM1' on Windows)
                baudrate=57600,
                bytesize=8,
                timeout=5,
                stopbits=serial.STOPBITS_ONE
        )
        self.data = Sark100Collector()

    def scan(self, start, end, step = 1000, progress=False):
        freq = start
        end += step
        total = math.ceil(((end - start) / step))
        print(f"Getting data between {start} and {end} with a step of {step} for a total of {total} data points.")
        self.device.write(f"scan {start} {end} {step}\r\n".encode())
        if progress:
            pbar = tqdm(total=total)
        while True:
            data = self.device.readline().decode('utf-8').strip()
            if data in ["Start", "", ">>"]:
                continue
            if data == "End":
                break
            if "Error" in data:
                print(data)
                break
            scan_result = dict(zip(self.data_vaules, data.split(",")))
            self.data.add_measurement(freq, data)
            freq += step
            if freq > end:
                break
            if progress:
                pbar.update(1)
                pbar.set_postfix({"Freqency": freq})
            yield {freq: scan_result}
        if progress:
            pbar.close()

    def scan_band(self, band, buffer_pct=0.15, step=1000, progress=False):
        freq_list = generate_band_frequencies(band, buffer_pct=buffer_pct, step_hz=step)
        return self.scan(freq_list[0], freq_list[-1], step, progress=progress)

    def plot(self):
        pass

    def __end__(self):
        self.device.close()
