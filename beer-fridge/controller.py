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

DEFAULT_UPPER_LIMIT = 54.0
DEFAULT_LOWER_LIMIT = 50.0
DEFAULT_RELAY_PIN = 4
DEFAULT_DELAY_S = 60.0 # S

LIMIT_LOWER_LIMIT = -20
LIMIT_UPPER_LIMIT = 100

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

        self.fridge_on = bool(GPIO.input(self.relay_pin))

    def run(self):
        logging.info("Controller Running")
        while not self.quit:
            self.updateTemp()

            n = 0
            while True:
                if self.quit or n >= self.delay:
                    break
                n += 1
                time.sleep(1)

    def updateTemp(self): # TODO: thread safety
        self.tempC = self.temp_sensor.readTempC()
        self.tempF = CtoF(self.tempC)

        logging.debug(str(datetime.datetime.now()))
        logging.info("Temp: {}, Fridge On?: {}".format(self.tempF, self.fridge_on))

        if not self.fridge_on:
            if self.tempF > self.upper_limit:
                if __name__ == "__main__":
                    logging.info("FRIDGE ON")
                self.fridge_on = True
                GPIO.output(self.relay_pin, GPIO.HIGH)
        else:
            if self.tempF < self.lower_limit:
                if __name__ == "__main__":
                    logging.info("FRIDGE OFF")
                self.fridge_on = False
                GPIO.output(self.relay_pin, GPIO.LOW)

    def setUpperLimit(self, limit):
        try:
            limit = float(limit)
        except ValueError:
            return False
        
        if limit < LIMIT_LOWER_LIMIT or limit > LIMIT_UPPER_LIMIT:
            return False

        self.upper_limit = limit
        return True
    
    def setLowerLimit(self, limit):
        try:
            limit = float(limit)
        except ValueError:
            return False
        
        if limit < LIMIT_LOWER_LIMIT or limit > LIMIT_UPPER_LIMIT:
            return False

        self.lower_limit = limit
        return True

    def setDelay(self, delay):
        try:
            delay = float(delay)
        except ValueError:
            return False
        if delay < 1.0 or delay > 60*60*4: #longer than 1 min, shorter than 4 hours
            return False

        self.delay = delay
        return True