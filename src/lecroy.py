import pyvisa
import logging

logger = logging.getLogger(__name__)


class LeCroyScope:
    def __init__(self, ip_address):
        """Initialize the LeCroyScope with the given IP address."""
        self.ip_address = ip_address
        self.rm = pyvisa.ResourceManager()
        self.scope = None

    def connect(self):
        """Connect to the oscilloscope."""
        if self.scope is None:
            self.scope = self.rm.open_resource(
                f"TCPIP0::{self.ip_address}::inst0::INSTR"
            )
            logger.info(f"Connected to: {self.scope.query('*IDN?')}")

    def acquire_waveform(self, channel):
        """Acquire a waveform from the given channel."""
        if self.scope is None:
            logger.error("Oscilloscope is not connected.")
            return None

        self.scope.write(f"{channel}:WF? DAT1")
        data = self.scope.read_raw()
        return data

    def acquire_measurement(self, channel, measurement_type):
        """Acquire a measurement of the given type from the given channel."""
        if self.scope is None:
            logger.error("Oscilloscope is not connected.")
            return None

        measurement = self.scope.query(f"{channel}:PAVA? :{measurement_type}?")
        return measurement

    def acquire_measurement2(self, channel, measurement_type):
        """Acquire a measurement of the given type from the given channel."""
        if self.scope is None:
            logger.error("Oscilloscope is not connected.")
            return None

        measurement = self.scope.query(f"{channel}:parameter:{measurement_type}?")
        return measurement

    def disconnect(self):
        """Disconnect from the oscilloscope."""
        if self.scope is not None:
            self.scope.close()
            self.scope = None
            logger.info("Disconnected from oscilloscope")
