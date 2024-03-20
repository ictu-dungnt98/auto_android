from ppadb.client import Client as AdbClient
import subprocess
import time
import numpy as np
from phone import Phone

# list cac buoc
LOGIN = 1
XEM_QC = LOGIN + 1
LOG_OUT = XEM_QC + 1
DOI_UID = LOG_OUT + 1
CHON_UID = DOI_UID + 1
NEXT = CHON_UID + 1
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
    
    device = devices[0]
    return device, client

def main():
    step = LOGIN
    package_name = "com.playmini.miniworld"
    activity_name = "org.appplay.lib.AppPlayBaseActivity"
    
    # connect adb
    device, client = connect()
    phone = Phone(device)

    # close app
    phone.close_app(package_name)
    time.sleep(1)
    phone.open_app(package_name, activity_name)
    time.sleep(2)
    
    while True:
        screenshot = phone.capture_screen()

        if step == LOGIN:
            if (phone.wait_img("login.png", screenshot)):
                phone.click_de_vao_game(screenshot)
            if (phone.wait_img("home.png", screenshot)):
                phone.click_to_img("nhan_vat.png", screenshot)
            if (phone.wait_img("quang_cao.png", screenshot)):
                phone.click_to_img("quang_cao.png", screenshot)
            if (phone.wait_img("qua_tang_qc.png", screenshot)):
                phone.click_to_img("qua_tang_qc.png", screenshot)
            if(phone.wait_img("xem_available.png", screenshot)):
                step = XEM_QC

        if step == XEM_QC:
            if(phone.wait_img("xem_not_available.png", screenshot)):
                step = LOG_OUT
            if(phone.wait_img("xem_available.png", screenshot)):
                phone.click_to_img("xem_available.png", screenshot)
            if(phone.wait_img("close_quang_cao.png", screenshot)):
                phone.click_to_img("close_quang_cao.png", screenshot)
            if(phone.wait_img("x_quang_cao.png", screenshot)):
                phone.click_to_img("x_quang_cao.png", screenshot)
            if(phone.wait_img("x_quang_cao_2.png", screenshot)):
                phone.click_to_img("x_quang_cao_2.png", screenshot)
            if(phone.wait_img("OK_nhan_qua.png", screenshot)):
                phone.click_to_img("OK_nhan_qua.png", screenshot)
        
        elif step == LOG_OUT:
            if (phone.wait_img("tai_khoan.png", screenshot)):
                step = DOI_UID
                 
            if (phone.wait_img("close_xem_not_available.png", screenshot)):
                phone.click_to_img("close_xem_not_available.png", screenshot)
            if (phone.wait_img("setting_btn.png", screenshot)):
                phone.click_to_img("setting_btn.png", screenshot)
        
        elif step == DOI_UID:
            if (phone.wait_img("tai_khoan.png", screenshot)):
                phone.click_to_img("tai_khoan.png", screenshot)   
            if (phone.wait_img("doi_uuid.png", screenshot)):
                phone.click_to_img("doi_uuid.png", screenshot)
            if (phone.wait_img("ok_doi_uid.png", screenshot)):
                phone.click_to_img("ok_doi_uid.png", screenshot)
            if (phone.wait_img("login.png", screenshot)):
                step = CHON_UID
        elif step == CHON_UID:
            if (phone.wait_img("show_list_uid.png", screenshot)):
                phone.click_to_img("show_list_uid.png", screenshot)   
        
if __name__ == "__main__":
    main()
