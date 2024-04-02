from ppadb.client import Client as AdbClient
import subprocess
import time
import numpy as np
from phone import Phone
import threading

# list cac buoc
LOGIN = 1
QUA_TANG_QC = LOGIN + 1
XEM_QC = QUA_TANG_QC + 1
LOG_OUT = XEM_QC + 1
DOI_UID = LOG_OUT + 1
CHON_UID = DOI_UID + 1
SCROLL_ACCOUNT = CHON_UID + 1
CHOOSE_ACCOUNT = SCROLL_ACCOUNT + 1
JOIN_GAME = CHOOSE_ACCOUNT + 1
CLICK_NHAP_USER = JOIN_GAME + 1
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

def state_machine(device, index):    
    step = XEM_QC
    package_name = "com.playmini.miniworld"
    activity_name = "org.appplay.lib.AppPlayBaseActivity"
    
    # connect adb
    time_start_wait = 0
    time_to_wait_sec = 30
    
    phone = Phone(device)

    # # close app
    # phone.close_app(package_name)
    # time.sleep(2)
    # phone.open_app(package_name, activity_name)
    # time.sleep(2)
    
    while True:
        screenshot = phone.capture_screen()

        if step == XEM_QC:                    
            # OK_nhan_qua
            ret = 0
            imgs = ["OK_nhan_qua", "OK_nhan_qua2", "OK_nhan_qua3",
                    "OK_nhan_qua4", "OK_nhan_qua5", "OK_nhan_qua6",
                    "OK_nhan_qua7"]
            for img in imgs:
                if (phone.wait_img(img, screenshot)):
                    if (phone.click_to_img(img, screenshot)):
                        ret = 1
                        break
            if ret:        
                continue

            # xem_available
            ret = 0
            imgs = ["xem_available", "xem_available2", "xem_available3",
                    "xem_available4", "xem_available5", "xem_available6",
                    "xem_available7", "xem_available8", "xem_available9"]
            for img in imgs:
                if (phone.wait_img(img, screenshot)):
                    if (phone.click_to_img(img, screenshot)):
                        ret = 1
                        break
            if ret:
                time_start_wait = time.time()
                time_to_wait_sec = 30
                continue

            elapsed_time = time.time() - time_start_wait
            if (elapsed_time >= time_to_wait_sec):
                phone.go_to_home_screen()
                time.sleep(2)
                phone.open_app(package_name, activity_name)
                time.sleep(2)
                time_start_wait = time.time()
                time_to_wait_sec = 100

def process_devices(devices):
    threads = []

    # Create and start a thread for each device
    for index, device in enumerate(devices):
        thread = threading.Thread(target=state_machine, args=(device, index))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def main():
    devices = connect()
    print("phat hien {} thiet bi".format(len(devices)))
    process_devices(devices)
    # state_machine(devices[0], 0)
    
if __name__ == "__main__":
    main()
