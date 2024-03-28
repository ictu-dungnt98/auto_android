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
    
    # while True:
    #     try:
    #         # start adb-server
    #         cmd = f"adb start-server"
    #         subprocess.run(cmd, shell=True, timeout=5)
            
    #         # Connect to ADB server
    #         client = AdbClient(host="127.0.0.1", port=5037)
    #         # Get list of devices
    #         devices = client.devices()
    #         if len(devices) == 0:
    #             print("No devices connected.")
    #             exit()
    #         return devices
    #     except:
    #         pass

def state_machine(device, index):    
    step = CHON_UID
    package_name = "com.playmini.miniworld"
    activity_name = "org.appplay.lib.AppPlayBaseActivity"
    
    # connect adb
    time_start_wait = 0
    time_to_wait_sec = 10
    
    phone = Phone(device)

    # close app
    phone.close_app(package_name)
    time.sleep(1)
    phone.open_app(package_name, activity_name)
    time.sleep(2)
    
    while True:
        screenshot = phone.capture_screen()

        if step == CHON_UID:
            ret = 0
            imgs = ["show_list_uid", "show_list_uid2", "show_list_uid3",
                    "show_list_uid4", "show_list_uid5", "show_list_uid6",
                    "show_list_uid7"]
            for img in imgs:
                if (phone.wait_img(img, screenshot)):
                    if (phone.click_to_img(img, screenshot)):
                        ret = 1
                        break
            if ret:
                print("continue")
                continue
            
            ret = 0
            imgs = ["show_list_uid_success", "show_list_uid_success2", "show_list_uid_success3",
                    "show_list_uid_success4", "show_list_uid_success5", "show_list_uid_success6",
                    "show_list_uid_success7"]
            for img in imgs:
                if (phone.wait_img(img, screenshot)):
                    ret = 1
                    break
            if ret:
                step = SCROLL_ACCOUNT

        elif step == SCROLL_ACCOUNT:
            # scroll list uid
            ret = 0
            imgs = ["show_list_uid_success", "show_list_uid_success2", "show_list_uid_success3",
                    "show_list_uid_success4", "show_list_uid_success5", "show_list_uid_success6",
                    "show_list_uid_success7"]
            for img in imgs:
                if (phone.wait_img(img, screenshot)):
                    phone.swipe_list_uid(img, screenshot)
                    ret = 1
                    break
            if ret:
                step = CHOOSE_ACCOUNT
                
        elif step == CHOOSE_ACCOUNT:
            ret = 0
            imgs = ["add_uid", "add_uid2", "add_uid3",
                    "add_uid4", "add_uid5", "add_uid6",
                    "add_uid7"]
            for img in imgs:
                if (phone.wait_img(img, screenshot)):
                    phone.select_last_uid(img, screenshot)
                    step = JOIN_GAME
                    break
                
        elif step == JOIN_GAME:
            phone.click_to_join_game("show_list_uid", screenshot)
            step = LOGIN

        elif step == LOGIN:       
            if (phone.wait_img("close_unused_popup", screenshot)):
                if (phone.click_to_img("close_unused_popup", screenshot)):
                    continue
            if (phone.wait_img("close_tich_luy_dang_nhap", screenshot)):
                if (phone.click_to_img("close_tich_luy_dang_nhap", screenshot)):
                    continue
            if (phone.wait_img("plus_jump_to_qc", screenshot)):
                if (phone.click_left_of_img("plus_jump_to_qc", screenshot)):
                    continue
            if (phone.wait_img("qua_tang_qc", screenshot)):
                step = QUA_TANG_QC
        
        elif step == QUA_TANG_QC:
            if (phone.wait_img("qua_tang_qc", screenshot)):
                phone.click_to_img("qua_tang_qc", screenshot)
            if (phone.wait_img("xem_available", screenshot)):
                step = XEM_QC
                continue
            if (phone.wait_img("35_35", screenshot)):
                step = LOG_OUT
                continue
            if (phone.wait_img("OK_nhan_qua", screenshot)):
                phone.click_to_img("OK_nhan_qua", screenshot)

        if step == XEM_QC:
            if(phone.wait_img("35_35", screenshot)):
                step = LOG_OUT
                continue
            if(phone.wait_img("xem_available", screenshot)):
                if (phone.click_to_img("xem_available", screenshot)):
                    time_start_wait = time.time()
                    time_to_wait_sec = 30
            if(phone.wait_img("OK_nhan_qua", screenshot)):
                if (phone.click_to_img("OK_nhan_qua", screenshot)):
                    continue
            if(phone.wait_img("tiep_tuc_xem", screenshot)):
                if (phone.click_to_img("tiep_tuc_xem", screenshot)):
                    continue

            elapsed_time = time.time() - time_start_wait
            if (elapsed_time >= time_to_wait_sec):
                phone.go_to_home_screen()
                time.sleep(2)
                phone.open_app(package_name, activity_name)
                time.sleep(2)
                time_start_wait = time.time()
                time_to_wait_sec = 10
        
        elif step == LOG_OUT:
            if (phone.wait_img("close_xem_not_available", screenshot)):
                if (phone.click_to_img("close_xem_not_available", screenshot)):
                    continue
            if (phone.wait_img("setting_btn", screenshot)):
                phone.click_to_img("setting_btn", screenshot)
                step = DOI_UID
                continue
            if(phone.wait_img("OK_nhan_qua", screenshot)):
                phone.click_to_img("OK_nhan_qua", screenshot)

        elif step == DOI_UID:
            if(phone.wait_img("OK_nhan_qua", screenshot)):
                if (phone.click_to_img("OK_nhan_qua", screenshot)):
                    continue
            if (phone.wait_img("tai_khoan", screenshot)):
                if (phone.click_to_img("tai_khoan", screenshot)):
                    continue
            if (phone.wait_img("doi_uuid", screenshot)):
                if (phone.click_to_img("doi_uuid", screenshot)):
                    continue
            if (phone.wait_img("ok_doi_uid", screenshot)):
                if (phone.click_to_img("ok_doi_uid", screenshot)):
                    continue
            if (phone.wait_img("show_list_uid", screenshot) or
                phone.wait_img("show_list_uid2", screenshot) or
                phone.wait_img("show_list_uid3", screenshot)):
                step = CHON_UID
            if (phone.wait_img("show_list_uid2", screenshot)):
                step = CHON_UID

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
