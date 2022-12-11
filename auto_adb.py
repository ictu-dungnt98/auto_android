from ppadb.client import Client as AdbClient
import cv2
import emulator

class Auto:
    def __init__(self):
        # Default is "127.0.0.1" and 5037
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.devices = self.client.devices()

    def list_devices(self):
        for device in self.devices:
            print(device.serial)

    def capture_screens(self):
        for device in self.devices:
            e = emulator.Emulator(device)
            screen = e.capture_screen()

auto = Auto()
# auto.list_devices()
auto.capture_screens()