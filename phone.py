try: 
    import os
    from ppadb.client import Client as AdbClient
    import numpy as np
    import cv2
except:
    os.system("pip install ppadb")
    os.system("pip install cv2")
    os.system("pip install numpy")
    os.system("pip install opencv-python")

from ppadb.client import Client as AdbClient
import numpy as np
import cv2
import subprocess
import time

class Phone:
    def __init__(self, device):
        self.device = device
        self.img_35_35 = cv2.imread("samsung/35_35.png", cv2.IMREAD_COLOR)
        self.img_add_uid = cv2.imread("samsung/add_uid.png", cv2.IMREAD_COLOR)
        self.img_btn_dang_nhap = cv2.imread("samsung/btn_dang_nhap.png", cv2.IMREAD_COLOR)
        self.img_close_quang_cao = cv2.imread("samsung/close_quang_cao.png", cv2.IMREAD_COLOR)
        self.img_close_tich_luy_dang_nhap = cv2.imread("samsung/close_tich_luy_dang_nhap.png", cv2.IMREAD_COLOR)
        self.img_close_unused_popup = cv2.imread("samsung/close_unused_popup.png", cv2.IMREAD_COLOR)
        self.img_close_xem_not_available = cv2.imread("samsung/close_xem_not_available.png", cv2.IMREAD_COLOR)
        self.img_dang_nhap_tai_khoan = cv2.imread("samsung/dang_nhap_tai_khoan.png", cv2.IMREAD_COLOR)
        self.img_doi_uuid = cv2.imread("samsung/doi_uuid.png", cv2.IMREAD_COLOR)
        self.img_insert_text = cv2.imread("samsung/insert_text.png", cv2.IMREAD_COLOR)
        self.img_login = cv2.imread("samsung/login.png", cv2.IMREAD_COLOR)
        self.img_ok_doi_uid = cv2.imread("samsung/ok_doi_uid.png", cv2.IMREAD_COLOR)
        self.img_OK_nhan_qua = cv2.imread("samsung/OK_nhan_qua.png", cv2.IMREAD_COLOR)
        self.img_ok_text_input = cv2.imread("samsung/ok_text_input.png", cv2.IMREAD_COLOR)
        self.img_plus_jump_to_qc = cv2.imread("samsung/plus_jump_to_qc.png", cv2.IMREAD_COLOR)
        self.img_qua_tang_qc = cv2.imread("samsung/qua_tang_qc.png", cv2.IMREAD_COLOR)
        self.img_setting_btn = cv2.imread("samsung/setting_btn.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid = cv2.imread("samsung/show_list_uid.png", cv2.IMREAD_COLOR)
        self.img_tai_khoan = cv2.imread("samsung/tai_khoan.png", cv2.IMREAD_COLOR)
        self.img_text_input_username = cv2.imread("samsung/text_input_username.png", cv2.IMREAD_COLOR)
        self.img_text_input_passwd = cv2.imread("samsung/text_input_passwd.png", cv2.IMREAD_COLOR)
        self.img_tiep_tuc_dang_nhap = cv2.imread("samsung/tiep_tuc_dang_nhap.png", cv2.IMREAD_COLOR)
        self.img_tiep_tuc_xem = cv2.imread("samsung/tiep_tuc_xem.png", cv2.IMREAD_COLOR)
        self.img_x_quang_cao_2 = cv2.imread("samsung/x_quang_cao_2.png", cv2.IMREAD_COLOR)
        self.img_xem_available = cv2.imread("samsung/xem_available.png", cv2.IMREAD_COLOR)
        self.img_xem_not_available = cv2.imread("samsung/xem_not_available.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid_success = cv2.imread("samsung/show_list_uid_success.png", cv2.IMREAD_COLOR)

    def get_image_by_name(self, img_path):
        print(f"get_image_by_name {img_path}")
        filename = os.path.basename(img_path)
        img_path = f"img_{filename}"
        img = getattr(self, img_path, None)
        if img is None:
            print(f"No image found for {img_path}")
        return img

    def open_app(self, package_name, activity_name):
        # Command to open the app
        command = f"am start -n {package_name}/{activity_name}"
        self.device.shell(command)

    def close_app(self,package_name):
        # adb_cmd = f"adb shell am force-stop {package_name}"
        # subprocess.run(adb_cmd, shell=True)
        command = f"am force-stop {package_name}"
        self.device.shell(command)
    
    def go_to_home_screen(self):
        # adb_cmd = "adb shell input keyevent KEYCODE_HOME"
        # subprocess.run(adb_cmd, shell=True)
        command = f"input keyevent KEYCODE_HOME"
        self.device.shell(command)

    def scroll_down(self, start_x, start_y, end_x, end_y):
        command = f"input swipe {start_x} {start_y} {end_x} {end_y}"
        self.device.shell(command)

    def capture_screen(self):
        # Run adb command to capture a screenshot
        screenshot_bytes = self.device.screencap()
        # Convert the screenshot bytes to a numpy array
        screenshot_np = np.frombuffer(screenshot_bytes, dtype=np.uint8)
        # Decode the numpy array as an OpenCV image
        screenshot = cv2.imdecode(screenshot_np, cv2.IMREAD_COLOR)
        return screenshot
  
    def find_image(self, image, screenshot):
        # Load the template image
        # template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        template = cv2.convertScaleAbs(image)

        # Convert images to the correct data type if necessary
        screenshot = cv2.convertScaleAbs(screenshot)

        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Threshold for match confidence
        threshold = 0.8
        # If a match is found with sufficient confidence
        if max_val >= threshold:
            # Extract the coordinates of the match
            match_location = max_loc
            return match_location
        else:
            return None


    def find_center_of_img(self,image,screenshot):
        # # Load the template image
        # template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        template = cv2.convertScaleAbs(image)
        # Convert images to the correct data type if necessary
        screenshot = cv2.convertScaleAbs(screenshot)
        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Threshold for match confidence
        threshold = 0.8
        if max_val >= threshold:
            # Calculate the center coordinates
            top_left = max_loc
            template_width, template_height = template.shape[1], template.shape[0]
            center_x = top_left[0] + template_width // 2
            center_y = top_left[1] + template_height // 2
            return center_x, center_y
        return 0, 0

    def wait_img(self, img_path, screenshot):          
        print("wait_img {}".format(img_path))
        image = self.get_image_by_name(img_path)
        match_location = self.find_image(image, screenshot)
        if match_location:
            return True
        else:
            return False
    
    def click_to_img(self, img_path, screenshot):
        image = self.get_image_by_name(img_path)
        screenshot = cv2.convertScaleAbs(screenshot)
        center_x, center_y = self.find_center_of_img(image, screenshot)
        
        if center_x != 0 and center_y != 0:
            self.click_to_position(center_x, center_y)
            print("click to {} success".format(img_path))
            return True
        else:
            print("click to {} fail".format(img_path))
            time.sleep(1)  # Wait for 1 second before retrying
            return False
    
    def click_left_of_img(self, img_path, screenshot):
        # Load the template image
        image = self.get_image_by_name(img_path)
        template = cv2.convertScaleAbs(image)
        # Convert images to the correct data type if necessary
        screenshot = cv2.convertScaleAbs(screenshot)

        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Threshold for match confidence
        threshold = 0.8
        if max_val >= threshold:
            # Calculate the center coordinates
            top_left = max_loc
            center_x = top_left[0]
            center_y = top_left[1]
            self.click_to_position(center_x, center_y)
            print("click to {} success".format(img_path))
            return True
        else:
            return None

    def click_to_position(self, x, y):
        command = f"input tap {x} {y}"
        self.device.shell(command)

