import pickle
from typing import Dict, Any


class Measurement:
    def __init__(self, num_meas: int) -> None:
        """
        Initialize Measurement with the number of measurements,
        a dictionary for measurement data, a header, and a file name.
        """
        self.num_meas = num_meas
        self.meas_data = {}
        self.header = {}

    def set_header(self, header: Dict[str, Any]) -> None:
        """
        Set the header information for the measurement.
        """
        self.header = header

    def add_waveforms(self, waveforms: Dict[str, Any]) -> None:
        """
        Add waveform data to the measurement data dictionary.
        """
        for channel, waveform in waveforms.items():
            if channel not in self.meas_data:
                self.meas_data[channel] = []
            self.meas_data[channel].append(waveform)


class MeasurementIO:
    @staticmethod
    def write(measurement: Measurement, file_name: str) -> None:
        """
        Write Measurement data to a file.
        """
        with open(file_name, "wb") as file:
            pickle.dump(
                {"header": measurement.header, "data": measurement.meas_data}, file
            )

    @staticmethod
    def read(file_name: str) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Read data from a file and return a Measurement object.
        """
        with open(file_name, "rb") as file:
            content = pickle.load(file)
            header_dict = content["header"]
            meas_data_dict = content["data"]
            return header_dict, meas_data_dict
