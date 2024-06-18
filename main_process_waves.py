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

    file_name = config["measurement"]["file_name"]
    num_meas = config["measurement"]["num_meas"]

    header_dict, waveforms = MeasurementIO.read(file_name)

    for num in range(num_meas):
        for channel in waveforms.keys():
            waveform = waveforms[channel][num]
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


if __name__ == "__main__":
    main()
