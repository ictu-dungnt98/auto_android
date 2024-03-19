from ppadb.client import Client as AdbClient
import subprocess
import time
import numpy as np
from phone import Phone

# list cac buoc
LOGIN = 1
CLICK_MAN_HINH_CHINH = LOGIN + 1
CLICK_NHAN_VAT = CLICK_MAN_HINH_CHINH + 1
CLICK_QUANG_CAO = CLICK_NHAN_VAT + 1
CLICK_QUA_TANG_QC = CLICK_QUANG_CAO + 1
NEXT = CLICK_QUA_TANG_QC + 1
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

    while True:
        if step == LOGIN:
            phone.open_app(package_name, activity_name)
            step = CLICK_MAN_HINH_CHINH
        elif step == CLICK_MAN_HINH_CHINH:
            phone.click_de_vao_game()
            if (phone.wait_main_screen()):
                step = CLICK_NHAN_VAT
        elif step == CLICK_NHAN_VAT:
            if (phone.click_to_img("nhan_vat.png")):
                step = CLICK_QUANG_CAO
        elif step == CLICK_QUANG_CAO:
            if(phone.click_to_img("quang_cao.png")):
                step = CLICK_QUA_TANG_QC
        elif step == CLICK_QUA_TANG_QC:
            if(phone.click_to_img("qua_tang_qc.png")):
                step = NEXT
        elif step == NEXT:
            pass

if __name__ == "__main__":
    main()
