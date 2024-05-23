import numpy as np


def process_waveform_data(raw_data):
    waveform = np.frombuffer(raw_data, dtype="int16")
    return waveform
