#!/usr/bin/env python3

"""Run the acquisition for a Scope. 
Usage: main.py YAMLCONF

Arguments:
    YAMLCONF  File with all parameters to take into account for the acquisition.

Options:
    -h --help     Show this screen.    
"""

import time

from matplotlib import pyplot as plt
import numpy as np
from src.lecroy import LeCroyScope
from src.measurement import process_waveform_data
import yaml
from docopt import docopt

from src.measurement import Measurement, MeasurementIO


def write_header(file, header_dict):
    """Write the header information into the file."""
    with open(file, "wb") as file:
        pass


def main():
    args = docopt(__doc__)
    config_file = args["YAMLCONF"]

    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    OSCILLOSCOPE_IP = config["oscilloscope"]["ip"]
    MEASUREMENTS = config["oscilloscope"]["measurements"]
    CHANNELS = config["oscilloscope"]["channels"]
    TYPE = config["oscilloscope"]["type"]

    print(f"Conectando al osciloscopio en: {OSCILLOSCOPE_IP}")
    oscilloscope = LeCroyScope(OSCILLOSCOPE_IP)
    oscilloscope.connect()

    measurement = Measurement(100)

    header_dict = {}

    for channel in CHANNELS:
        vertical_gain, vertical_offset, horizontal_interval = (
            oscilloscope.header_info_waveform(channel)
        )
        header_dict[channel] = {
            "vertical_gain": vertical_gain,
            "vertical_offset": vertical_offset,
            "horizontal_interval": horizontal_interval,
        }

    measurement.set_header(header_dict)

    for _ in range(measurement.num_meas):
        oscilloscope.scope.write("TRMD SINGLE")
        waveforms = oscilloscope.acquire_waveforms(CHANNELS)
        measurement.add_waveforms(waveforms)
        for channel, waveform in waveforms.items():
            # plot the waveform data using the header information
            vertical_gain = header_dict[channel]["vertical_gain"]
            vertical_offset = header_dict[channel]["vertical_offset"]

            horizontal_interval = header_dict[channel]["horizontal_interval"]
            time_axis = np.arange(
                0, horizontal_interval * len(waveform), horizontal_interval
            )

            plt.plot(time_axis, waveform + vertical_offset, label=f"Channel {channel}")
            plt.title(f"Channel {channel}")
            plt.xlabel("Time (s)")
            plt.ylabel("Voltage (V)")
            plt.legend()
            plt.grid()
        plt.show()

    oscilloscope.disconnect()

    MeasurementIO.write(measurement, "test.pickle")


if __name__ == "__main__":
    main()
