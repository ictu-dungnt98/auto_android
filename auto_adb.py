from ppadb.client import Client as AdbClient
import cv2

apk_path = "example.apk"

# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

for device in devices:
    print (device.serial)
    result = device.screencap()
    file = "{}.png".format(device.serial.split(":")[0])
    print(file)
    with open(file, "wb") as fp:
        fp.write(result)