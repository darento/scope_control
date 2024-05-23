#!/usr/bin/env python3

"""Run the acquisition for a Scope. 
Usage: main.py YAMLCONF

Arguments:
    YAMLCONF  File with all parameters to take into account for the acquisition.

Options:
    -h --help     Show this screen.    
"""

from src.lecroy import LeCroyScope
from src.measurement import process_waveform_data
import yaml
from docopt import docopt


def main():
    args = docopt(__doc__)
    config_file = args["YAMLCONF"]

    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    OSCILLOSCOPE_IP = config["oscilloscope"]["ip"]

    print(f"Connecting to oscilloscope at: {OSCILLOSCOPE_IP}")
    oscilloscope = LeCroyScope(OSCILLOSCOPE_IP)
    oscilloscope.connect()

    try:
        measurement = oscilloscope.acquire_measurement("C1", "PK2Pk")
        print(f"Peak-to-Peak Voltage: {measurement} V")

        raw_waveform = oscilloscope.acquire_waveform("C1")
        waveform = process_waveform_data(raw_waveform)
        print(f"Waveform data: {waveform}")
    finally:
        oscilloscope.disconnect()


if __name__ == "__main__":
    main()
