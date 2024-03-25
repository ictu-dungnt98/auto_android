from ppadb.client import Client as AdbClient
import subprocess
import time
import numpy as np
from phone import Phone
import threading
import xml.etree.ElementTree as ET

import subprocess
import json
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import os


# list cac buoc
LOGIN = 1
XEM_QC = LOGIN + 1
LOG_OUT = XEM_QC + 1
DOI_UID = LOG_OUT + 1
CHON_UID = DOI_UID + 1
CLICK_NHAP_USER = CHON_UID + 1
INSERT_USER = CLICK_NHAP_USER + 1
CLICK_NHAP_PASSWD = INSERT_USER + 1
INSERT_PASSWD = CLICK_NHAP_PASSWD + 1
CLICK_DANG_NHAP = INSERT_PASSWD + 1

def parse_user_password(filename):
    user_password_pairs = []

    with open(filename, 'r') as file:
        for line in file:
            # Split the line into username and password based on the separator "|"
            parts = line.strip().split("|")
            if len(parts) == 2:
                username = parts[0].strip()
                password = parts[1].strip()
                user_password_pairs.append((username, password))

    return user_password_pairs

def connect():
    # start adb-server
    cmd = f"adb start-server"
    subprocess.run(cmd, shell=True)
    
    # Connect to ADB server
    client = AdbClient(host="127.0.0.1", port=5037)
    # Get list of devices
    devices = client.devices()
    if len(devices) == 0:
        print("No devices connected.")
        exit()

    return devices

# Function to get the screen size of the phone
def get_phone_screen_size():
    # Run adb shell command to get display metrics
    adb_cmd = "adb shell wm size"
    adb_process = subprocess.Popen(adb_cmd, shell=True, stdout=subprocess.PIPE)
    output = adb_process.stdout.read().decode("utf-8").strip()

    # Extract screen size from output
    screen_size = output.split("Physical size:")[1].split("\n")[0].strip()

    # Parse screen size as width and height
    width, height = map(int, screen_size.split("x"))

    return width, height

# Function to dump window layout using adb shell uiautomator dump
# def dump_window_layout(device):
#     # remove old file
#     # try:
#     #     os.remove("window_dump.xml")
#     # except:
#     #     pass
#     # Run adb shell uiautomator dump command
#     # Run adb shell uiautomator dump command
#     adb_cmd = "uiautomator dump /sdcard/window_dump.xml"
#     subprocess.run(adb_cmd, shell=True)
#     # Pull the XML file from the device
#     device.shell("pull /sdcard/window_dump.xml")
#     # Wait until the file exists
#     max_attempts = 10
#     interval = 0.5  # Check every 0.5 seconds
#     attempts = 0
    
#     while not os.path.exists("window_dump.xml"):
#         time.sleep(interval)
#         attempts += 1
#         if attempts >= max_attempts:
#             print("Timeout: File not found.")
#             return

#     print("File found: Window layout dump complete.")

def dump_window_layout(device):
    # remove old file
    try:
        os.remove("window_dump.xml")
    except:
        pass
    
    while True:
        # Run adb shell uiautomator dump command
        adb_cmd = "uiautomator dump /sdcard/window_dump.xml"
        device.shell(adb_cmd)
        time.sleep(2)

        # Pull the XML file from the device
        adb_cmd = "pull /sdcard/window_dump.xml"
        device.shell(adb_cmd)
        time.sleep(2)
        
        # Parse the XML file
        try:
            tree = ET.parse("window_dump.xml")
            root = tree.getroot()
            return root
        except:
            pass
    return None

# Function to parse the XML file containing window layout information
def parse_window_layout(device):
    try:
        tree = ET.parse("window_dump.xml")
        root = tree.getroot()
        # # Extract relevant information from the XML
        # # Example: find the package name and bounds of the first node
        # package_name = root.attrib.get("package")
        # bounds = root.find(".//node").attrib.get("bounds")
        return root
    except:
        pass

# Function to draw rectangles representing screen elements on a canvas image
def draw_screen_elements(root, image_size):
    img = Image.new("RGB", image_size, color="white")
    draw = ImageDraw.Draw(img)

    for node in root.findall(".//node"):
        bounds = node.attrib.get("bounds")
        left, top, right, bottom = map(int, bounds.strip("[]").replace("][", ",").split(","))
        draw.rectangle([left, top, right, bottom], outline="red")

    return img


def state_machine(device, index):
    # app package
    package_name = "com.playmini.miniworld"
    activity_name = "org.appplay.lib.AppPlayBaseActivity"
    
    # account
    in_used = 0
    step = CHON_UID
    file_name = f"account{index}.txt"
    user_password_pairs = parse_user_password(file_name)
    
    # connect adb
    phone = Phone(device)

    # close app
    phone.close_app(package_name)
    time.sleep(1)
    phone.open_app(package_name, activity_name)
    time.sleep(2)
    
    # Get the screen size of the phone
    screen_width, screen_height = get_phone_screen_size()
    print("Screen Width:", screen_width)
    print("Screen Height:", screen_height)
    
    while True:
        # Load XML file containing window layout information
        xml_file = "window_dump.xml"
        if (dump_window_layout(device) != None):
            # Parse and extract information from the dumped layout
            root = parse_window_layout(device)

            # Draw screen elements on an image
            image_size = (screen_width, screen_height)
            canvas_image = draw_screen_elements(root, image_size)

            # Display the canvas image
            canvas_image.show()
    
def main():
    devices = connect()
    print("phat hien {} thiet bi".format(len(devices)))
    state_machine(devices[0], 0)
    
if __name__ == "__main__":
    main()
