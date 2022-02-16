
import logging

logging.basicConfig(level=logging.DEBUG)

logging.warn("Using virtual GPIO for testing")

BCM = "BCM"
OUT = "OUT"
IN = "IN"
HIGH = "HIGH"
LOW = "LOW"

_virtual_pin_fname = "virtual_pin.txt"

def setmode(mode):
    logging.info(f"setmode: {mode}")

def setup(pin, mode):
    logging.info(f"setup: pin={pin}, mode={mode}")

def input(pin):
    logging.info(f"input: pin={pin}")
    with open(_virtual_pin_fname, 'r') as f:
        return 1 if f.read().strip() == "ON" else 0

def output(pin, value):
    logging.info(f"output: pin={pin}, value={value}")
    with open(_virtual_pin_fname,'w') as f:
        f.write("ON" if value == HIGH else "OFF")