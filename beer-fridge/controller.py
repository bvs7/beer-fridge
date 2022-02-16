import time
import logging
import datetime

logging.basicConfig(level=logging.DEBUG)


try:
    import Adafruit_MCP9808.MCP9808 as MCP9808 # type: ignore comment
except ModuleNotFoundError:
    logging.error("No Temp sensor library, using virtual")
    import virtual_MCP9808 as MCP9808
    
try:
    import RPi.GPIO as GPIO                    # type: ignore comment
except ModuleNotFoundError:
    logging.error("No RPi.GPIO library, using virtual")
    import virtual_GPIO as GPIO


__all__ = ['FridgeController']

DEFAULT_UPPER_LIMIT = 54
DEFAULT_LOWER_LIMIT = 50
DEFAULT_RELAY_PIN = 4
DEFAULT_DELAY_S = 5.0 # S

def CtoF(tempC):
    return tempC * 9.0/5.0 + 32.0

class FridgeController:

    def __init__(self,
        relay_pin=DEFAULT_RELAY_PIN, upper_limit=DEFAULT_UPPER_LIMIT,
        lower_limit=DEFAULT_LOWER_LIMIT, delay=DEFAULT_DELAY_S):

        self.quit = False

        self.delay = delay

        self.upper_limit = upper_limit # F
        self.lower_limit = lower_limit # F

        self.temp_sensor = MCP9808.MCP9808()
        self.temp_sensor.begin()

        self.relay_pin = relay_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay_pin,GPIO.OUT)

        self.fridge_on = GPIO.input(self.relay_pin)

    def run(self):
        while not self.quit:
            tempC = self.temp_sensor.readTempC()
            tempF = CtoF(tempC)
            logging.debug(str(datetime.datetime.now()))
            logging.info("Temp: {}, Fridge On?: {}".format(tempF, self.fridge_on))

            if not self.fridge_on:
                if tempF > self.upper_limit:
                    if __name__ == "__main__":
                        logging.info("FRIDGE ON")
                    self.fridge_on = True
                    GPIO.output(self.relay_pin, GPIO.HIGH)
            else:
                if tempF < self.lower_limit:
                    if __name__ == "__main__":
                        logging.info("FRIDGE OFF")
                    self.fridge_on = False
                    GPIO.output(self.relay_pin, GPIO.LOW)

            time.sleep(self.delay)