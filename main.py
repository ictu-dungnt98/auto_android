from ppadb.client import Client as AdbClient
import subprocess
import time

# list cac buoc
LOGIN = 1
CLICK_NHAN_VAT = LOGIN + 1
CLICK_QUANG_CAO = CLICK_NHAN_VAT + 1

def get_screen_dimensions():
    # Run adb command to get the screen dimensions
    adb_cmd = "adb shell wm size"
    result = subprocess.run(adb_cmd, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    # Extract screen width and height from the output
    width, height = map(int, output.split()[-1].split('x'))
    return width, height

def click_center_of_screen():
    # Get screen dimensions
    width, height = get_screen_dimensions()
    # Calculate center coordinates
    center_x = width // 2
    center_y = height // 2
    # Run adb command to send a tap event at the center of the screen
    adb_cmd = f"adb shell input tap {center_x} {center_y}"
    print(adb_cmd)
    subprocess.run(adb_cmd, shell=True)

def open_app(device, package_name, activity_name):
    # Command to open the app
    command = f"am start -n {package_name}/{activity_name}"
    device.shell(command)

def close_app(package_name):
    adb_cmd = f"adb shell am force-stop {package_name}"
    subprocess.run(adb_cmd, shell=True)

def click_to_position(device, x, y):
    command = f"input tap {x} {y}"
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

    step = LOGIN
    package_name = "com.playmini.miniworld"
    activity_name = "org.appplay.lib.AppPlayBaseActivity"
    
    # close app
    close_app(package_name)
    time.sleep(1)

    while True:
        if step == LOGIN:
            open_app(device, package_name, activity_name)
            step = CLICK_NHAN_VAT
        if step == CLICK_NHAN_VAT:
            click_center_of_screen()
        if step == CLICK_QUANG_CAO:
            pass

if __name__ == "__main__":
    main()
