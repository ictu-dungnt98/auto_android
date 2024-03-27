from ppadb.client import Client as AdbClient
import subprocess
import time
import numpy as np
from phone import Phone
import threading

# list cac buoc
LOGIN = 1
XEM_QC = LOGIN + 1
LOG_OUT = XEM_QC + 1
DOI_UID = LOG_OUT + 1
CHON_UID = DOI_UID + 1
SCROLL_ACCOUNT = CHON_UID + 1
SELECT_ACCOUNT = SCROLL_ACCOUNT + 1
CLICK_NHAP_USER = SELECT_ACCOUNT + 1
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
    step = CHON_UID
    package_name = "com.playmini.miniworld"
    activity_name = "org.appplay.lib.AppPlayBaseActivity"
    
    # connect adb
    time_start_wait = 0
    in_used = 0
    file_name = f"account{index}.txt"
    user_password_pairs = parse_user_password(file_name)
    
    phone = Phone(device)

    # close app
    phone.close_app(package_name)
    time.sleep(1)
    phone.open_app(package_name, activity_name)
    time.sleep(2)
    
    while True:
        screenshot = phone.capture_screen()

        if step == LOGIN:       
            if (phone.wait_img("close_unused_popup", screenshot)):
                phone.click_to_img("close_unused_popup", screenshot)
            if (phone.wait_img("close_tich_luy_dang_nhap", screenshot)):
                phone.click_to_img("close_tich_luy_dang_nhap", screenshot)
            if (phone.wait_img("plus_jump_to_qc", screenshot)):
                phone.click_left_of_img("plus_jump_to_qc", screenshot)
            if (phone.wait_img("qua_tang_qc", screenshot)):
                phone.click_to_img("qua_tang_qc", screenshot)
            if(phone.wait_img("xem_available", screenshot)):
                step = XEM_QC
            if(phone.wait_img("OK_nhan_qua", screenshot)):
                phone.click_to_img("OK_nhan_qua", screenshot)
            if(phone.wait_img("35_35", screenshot)):
                step = LOG_OUT

        if step == XEM_QC:
            if(phone.wait_img("35_35", screenshot)):
                step = LOG_OUT
            if(phone.wait_img("xem_available", screenshot)):
                if (phone.click_to_img("xem_available", screenshot)):
                    time_start_wait = time.time()
            if(phone.wait_img("OK_nhan_qua", screenshot)):
                if (phone.click_to_img("OK_nhan_qua", screenshot)):
                    continue
                
            elapsed_time = time.time() - time_start_wait
            if (elapsed_time >= 30):
                phone.go_to_home_screen()
                phone.open_app(package_name, activity_name)
                time.sleep(2)
                time_start_wait = time.time()
        
        elif step == LOG_OUT:
            if(phone.wait_img("OK_nhan_qua", screenshot)):
                phone.click_to_img("OK_nhan_qua", screenshot)
            if (phone.wait_img("close_xem_not_available", screenshot)):
                phone.click_to_img("close_xem_not_available", screenshot)
            if (phone.wait_img("setting_btn", screenshot)):
                phone.click_to_img("setting_btn", screenshot)
                step = DOI_UID

        elif step == DOI_UID:
            if(phone.wait_img("OK_nhan_qua", screenshot)):
                phone.click_to_img("OK_nhan_qua", screenshot)
            if (phone.wait_img("tai_khoan", screenshot)):
                phone.click_to_img("tai_khoan", screenshot)   
            if (phone.wait_img("doi_uuid", screenshot)):
                phone.click_to_img("doi_uuid", screenshot)
            if (phone.wait_img("ok_doi_uid", screenshot)):
                phone.click_to_img("ok_doi_uid", screenshot)
            if (phone.wait_img("show_list_uid", screenshot)):
                step = CHON_UID

        elif step == CHON_UID:
            if (phone.wait_img("show_list_uid", screenshot)):
                phone.click_to_img("show_list_uid", screenshot)
            if (phone.wait_img("show_list_uid_success", screenshot)):
                step = SCROLL_ACCOUNT
        elif step == SCROLL_ACCOUNT:
            # re-check
            if (phone.wait_img("show_list_uid", screenshot)):
                phone.click_to_img("show_list_uid", screenshot)
            # scroll list uid
            if (phone.wait_img("show_list_uid_success", screenshot)):
                phone.swipe_list_uid("show_list_uid_success", screenshot)
            # wait add uid button
            if (phone.wait_img("add_uid", screenshot)):
                step = SELECT_ACCOUNT
        elif step == SELECT_ACCOUNT:
            phone.select_last_uid("add_uid", screenshot)
            step = LOGIN

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
    # process_devices(devices)
    state_machine(devices[0], 0)
    
if __name__ == "__main__":
    main()
