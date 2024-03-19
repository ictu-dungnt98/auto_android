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
            phone.click_login_screen()
            if (phone.wait_main_screen()):
                step = CLICK_NHAN_VAT
        elif step == CLICK_NHAN_VAT:
            if (phone.click_to_person()):
                print("click person success")
                step = CLICK_QUANG_CAO
        elif step == CLICK_QUANG_CAO:
            pass

if __name__ == "__main__":
    main()


# import cv2
# import numpy as np

# def select_roi(image):
#     # Display the image and allow the user to select a region of interest (ROI)
#     clone = image.copy()
#     roi = cv2.selectROI("Select ROI", clone)
#     cv2.destroyAllWindows()

#     # Crop the image to the selected ROI
#     x, y, w, h = roi
#     roi_image = image[y:y+h, x:x+w]

#     return roi_image

# def save_template(template_image, filename):
#     # Save the template image to a file
#     cv2.imwrite(filename, template_image)

# if __name__ == "__main__":
#     # Load the screen capture image
#     screenshot = cv2.imread("home.png")

#     # Select a region of interest (ROI) from the screen capture
#     template = select_roi(screenshot)

#     # Save the selected region as the template image
#     save_template(template, "template.png")

#     print("Template image saved as 'template.png'")