from enum import Enum


class LogIntensity(Enum):
    """Log intensity levels for the AAS HTTP client. Higher levels produce more detailed logs (e.g. for item not found). Standard level only logs critical errors and warnings."""

    STANDARD = 1
    HIGH = 2
