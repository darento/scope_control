import numpy as np
import pyvisa
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

logger.addHandler(handler)


class LeCroyScope:
    def __init__(self, ip_address: str) -> None:
        """Initialize the LeCroyScope with the given IP address."""
        self.ip_address = ip_address
        self.rm = pyvisa.ResourceManager()
        self.scope = None

    def _acquire_waveform(self, channel: str) -> np.ndarray:
        """Acquire a waveform from the given channel."""
        # Set the channel and query the waveform
        self.scope.write(f"{channel}:INSPECT? 'SIMPLE'")
        raw_data = self.scope.read()

        # Convertir la cadena en una lista de valores
        data_list = raw_data.split()
        # Convertir la lista de cadenas en una lista de flotantes
        data_list = [float(value) for value in data_list[2:-1]]

        # Convertir la lista en un array de NumPy
        data_array = np.array(data_list)

        return data_array

    def connect(self) -> None:
        """Connect to the oscilloscope."""
        if self.scope is None:
            self.scope = self.rm.open_resource(
                f"TCPIP0::{self.ip_address}::inst0::INSTR"
            )
            logger.info(f"Connected to: {self.scope.query('*IDN?')}")

    def acquire_waveforms(self, channels: list[str]) -> dict[str, np.ndarray]:
        """Acquire waveforms from the given channels."""
        if self.scope is None:
            logger.error("Oscilloscope is not connected.")
            return None

        self.scope.write("TRMD SINGLE")
        waveforms = {}
        for channel in channels:
            waveforms[channel] = self._acquire_waveform(channel)

        return waveforms

    # TODO: The method does not work as expected. Fix it.
    def acquire_measurement(self, channel: str, measurement_type: str) -> str:
        """Acquire a measurement of the given type from the given channel."""
        if self.scope is None:
            logger.error("Oscilloscope is not connected.")
            return None

        self.scope.write(f"{channel}:PAVA? {measurement_type}")
        measurement = self.scope.read()
        return measurement

    def header_info_waveform(self, channel: str) -> tuple[float, float, float]:
        """Retrieve the header information from the oscilloscope."""

        self.scope.write(f"{channel}:INSPECT? 'VERTICAL_GAIN'")
        vertical_gain = self.scope.read()
        vertical_gain = float(vertical_gain.split()[-2])
        self.scope.write(f"{channel}:INSPECT? 'VERTICAL_OFFSET'")
        vertical_offset = self.scope.read()
        vertical_offset = float(vertical_offset.split()[-2])

        self.scope.write(f"{channel}:INSPECT? 'HORIZ_INTERVAL'")
        horizontal_interval = self.scope.read()
        horizontal_interval = float(horizontal_interval.split()[-2])

        return vertical_gain, vertical_offset, horizontal_interval

    def disconnect(self) -> None:
        """Disconnect from the oscilloscope."""
        if self.scope is not None:
            self.scope.close()
            self.scope = None
            logger.info("Disconnected from oscilloscope")
