
from ppadb.client import Client as AdbClient
import cv2

class Emulator:
    def __init__(self, device):
        self.device = device
    
    def capture_screen(self):
        print (self.device.serial)
        result = self.device.screencap()
        file = "{}.png".format(self.device.serial.split(":")[1])
        print(file)
        with open(file, "wb") as fp:
            fp.write(result)
