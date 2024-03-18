from ppadb.client import Client as AdbClient
import subprocess


def open_app(device, package_name, activity_name):
    # Command to open the app
    command = f"am start -n {package_name}/{activity_name}"
    device.shell(command)

def connect():
    # Connect to ADB server
    client = AdbClient(host="127.0.0.1", port=5037)
    # Get list of devices
    devices = client.devices()
    if len(devices) == 0:
        print("No devices connected.")
        exit()
    
    device = devices[0]
    return device, client

def main():
    device, client = connect()

    # Package name of the app you want to open
    package_name = "com.playmini.miniworld"
    # Activity name of the app you want to open
    activity_name = "org.appplay.lib.AppPlayBaseActivity"
    
    open_app(device, package_name, activity_name)

if __name__ == "__main__":
    main()
