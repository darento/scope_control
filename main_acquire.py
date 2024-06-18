#!/usr/bin/env python3

"""Run the acquisition for a Scope. 
Usage: main.py YAMLCONF

Arguments:
    YAMLCONF  File with all parameters to take into account for the acquisition.

Options:
    -h --help     Show this screen.    
"""

import yaml
from docopt import docopt
from tqdm import tqdm

from src.lecroy import LeCroyScope
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
    MEASUREMENTS = config["measurement"]["num_meas"]
    CHANNELS = config["oscilloscope"]["channels"]
    TYPE = config["oscilloscope"]["type"]
    FILE_NAME = config["measurement"]["file_name"]

    print(f"Conectando al osciloscopio en: {OSCILLOSCOPE_IP}")
    oscilloscope = LeCroyScope(OSCILLOSCOPE_IP)
    oscilloscope.connect()

    measurement = Measurement(MEASUREMENTS)

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

    for _ in tqdm(range(measurement.num_meas), desc="Acquiring waveforms"):
        oscilloscope.set_trigger_mode("SINGLE")
        waveforms = oscilloscope.acquire_waveforms(CHANNELS)
        measurement.add_waveforms(waveforms)

    oscilloscope.disconnect()

    MeasurementIO.write(measurement, FILE_NAME)


if __name__ == "__main__":
    main()
