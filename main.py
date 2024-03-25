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
        print("j7_img/No devices connected.")
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
            if (phone.wait_img("j7_img/login.png", screenshot)):
                phone.click_to_img("j7_img/login.png", screenshot)
            if (phone.wait_img("j7_img/close_unused_popup.png", screenshot)):
                phone.click_to_img("j7_img/close_unused_popup.png", screenshot)
            if (phone.wait_img("j7_img/close_tich_luy_dang_nhap.png", screenshot)):
                phone.click_to_img("j7_img/close_tich_luy_dang_nhap.png", screenshot)
            if (phone.wait_img("j7_img/plus_jump_to_qc.png", screenshot)):
                phone.click_left_of_img("j7_img/plus_jump_to_qc.png", screenshot)
            if (phone.wait_img("j7_img/qua_tang_qc.png", screenshot)):
                phone.click_to_img("j7_img/qua_tang_qc.png", screenshot)
            if(phone.wait_img("j7_img/xem_available.png", screenshot)):
                step = XEM_QC
            if(phone.wait_img("j7_img/OK_nhan_qua.png", screenshot)):
                phone.click_to_img("j7_img/OK_nhan_qua.png", screenshot)
            # if(phone.wait_img("j7_img/35_35.png", screenshot)):
            #     step = LOG_OUT

        if step == XEM_QC:
            # if(phone.wait_img("j7_img/35_35.png", screenshot)):
            #     step = LOG_OUT
            if(phone.wait_img("j7_img/xem_available.png", screenshot)):
                if (phone.click_to_img("j7_img/xem_available.png", screenshot)):
                    time_start_wait = time.time()
            if(phone.wait_img("j7_img/OK_nhan_qua.png", screenshot)):
                if (phone.click_to_img("j7_img/OK_nhan_qua.png", screenshot)):
                    continue
                
            elapsed_time = time.time() - time_start_wait
            if (elapsed_time >= 30):
                phone.go_to_home_screen()
                phone.open_app(package_name, activity_name)
                time.sleep(2)
                time_start_wait = time.time()
        
        elif step == LOG_OUT:
            if (phone.wait_img("j7_img/close_xem_not_available.png", screenshot)):
                phone.click_to_img("j7_img/close_xem_not_available.png", screenshot)
            if (phone.wait_img("j7_img/setting_btn.png", screenshot)):
                phone.click_to_img("j7_img/setting_btn.png", screenshot)
                step = DOI_UID

        elif step == DOI_UID:
            if (phone.wait_img("j7_img/tai_khoan.png", screenshot)):
                phone.click_to_img("j7_img/tai_khoan.png", screenshot)   
            if (phone.wait_img("j7_img/doi_uuid.png", screenshot)):
                phone.click_to_img("j7_img/doi_uuid.png", screenshot)
            if (phone.wait_img("j7_img/ok_doi_uid.png", screenshot)):
                phone.click_to_img("j7_img/ok_doi_uid.png", screenshot)
            if (phone.wait_img("j7_img/login.png", screenshot)):
                step = CHON_UID

        elif step == CHON_UID:
            if (phone.wait_img("j7_img/show_list_uid.png", screenshot)):
                phone.click_to_img("j7_img/show_list_uid.png", screenshot)
            if (phone.wait_img("j7_img/add_uid.png", screenshot)):
                phone.click_to_img("j7_img/add_uid.png", screenshot)
            if (phone.wait_img("j7_img/dang_nhap_tai_khoan.png", screenshot)):
                phone.click_to_img("j7_img/dang_nhap_tai_khoan.png", screenshot)
            if (phone.wait_img("j7_img/text_input_username.png", screenshot)):
                step = CLICK_NHAP_USER
                
        elif step == CLICK_NHAP_USER:
            if (phone.wait_img("j7_img/text_input_username.png", screenshot)):
                phone.click_to_img("j7_img/text_input_username.png", screenshot)
            if (phone.wait_img("j7_img/insert_text.png", screenshot)):
                step = INSERT_USER
                
        elif step == INSERT_USER:
            if (phone.wait_img("j7_img/insert_text.png", screenshot)):
                user, passwd = user_password_pairs[in_used]
                device.shell(f"input text '{user}'")
                if (phone.wait_img("j7_img/ok_text_input.png", screenshot)):
                    phone.click_to_img("j7_img/ok_text_input.png", screenshot)
                    step = CLICK_NHAP_PASSWD
        
        elif step == CLICK_NHAP_PASSWD:
            if (phone.wait_img("j7_img/text_input_passwd.png", screenshot)):
                phone.click_to_img("j7_img/text_input_passwd.png", screenshot)
            if (phone.wait_img("j7_img/insert_text.png", screenshot)):
                step = INSERT_PASSWD

        elif step == INSERT_PASSWD:
            if (phone.wait_img("j7_img/insert_text.png", screenshot)):
                user, passwd = user_password_pairs[in_used]
                device.shell(f"input text '{passwd}'")
                if (phone.wait_img("j7_img/ok_text_input.png", screenshot)):
                    phone.click_to_img("j7_img/ok_text_input.png", screenshot)
                    step = CLICK_DANG_NHAP
                    in_used += 1
            else:
                step = CLICK_NHAP_PASSWD

        elif step == CLICK_DANG_NHAP:
            if (phone.wait_img("j7_img/btn_dang_nhap.png", screenshot)):
                if (phone.click_to_img("j7_img/btn_dang_nhap.png", screenshot)):
                    continue
            if (phone.wait_img("j7_img/tiep_tuc_dang_nhap.png", screenshot)):
                phone.click_to_img("j7_img/tiep_tuc_dang_nhap.png", screenshot)
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
    print("j7_img/phat hien {} thiet bi".format(len(devices)))
    # process_devices(devices)
    state_machine(devices[0], 0)
    
if __name__ == "__main__":
    main()
