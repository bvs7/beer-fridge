
import logging

logging.basicConfig(level=logging.DEBUG)

logging.warn("Using virtual MCP9808 for testing")

_virtual_tempF_fname = 'virtual_tempF.txt'

class MCP9808():

    def begin(self):
        logging.info("Begin virtual MCP9808")

    def readTempC(self):
        with open(_virtual_tempF_fname,'r') as f:
            return (float(f.read().strip()) - 32.0) * 5.0 /9.0