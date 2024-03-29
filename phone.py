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
        self.phone_type = "j7_img"
        # self.phone_type = "samsung"
        self.img_35_35 = cv2.imread(f"{self.phone_type}/35_35.png", cv2.IMREAD_COLOR)
        self.img_35_35_2 = cv2.imread(f"{self.phone_type}/35_35_2.png", cv2.IMREAD_COLOR)
        self.img_35_35_3 = cv2.imread(f"{self.phone_type}/35_35_3.png", cv2.IMREAD_COLOR)
        self.img_35_35_4 = cv2.imread(f"{self.phone_type}/35_35_4.png", cv2.IMREAD_COLOR)
        self.img_35_35_5 = cv2.imread(f"{self.phone_type}/35_35_5.png", cv2.IMREAD_COLOR)
        
        self.img_add_uid = cv2.imread(f"{self.phone_type}/add_uid.png", cv2.IMREAD_COLOR)
        self.img_add_uid2 = cv2.imread(f"{self.phone_type}/add_uid2.png", cv2.IMREAD_COLOR)
        self.img_add_uid3 = cv2.imread(f"{self.phone_type}/add_uid3.png", cv2.IMREAD_COLOR)
        self.img_add_uid4 = cv2.imread(f"{self.phone_type}/add_uid4.png", cv2.IMREAD_COLOR)
        self.img_add_uid5 = cv2.imread(f"{self.phone_type}/add_uid5.png", cv2.IMREAD_COLOR)
        
        self.img_btn_dang_nhap = cv2.imread(f"{self.phone_type}/btn_dang_nhap.png", cv2.IMREAD_COLOR)
        self.img_close_quang_cao = cv2.imread(f"{self.phone_type}/close_quang_cao.png", cv2.IMREAD_COLOR)
        
        self.img_close_tich_luy_dang_nhap = cv2.imread(f"{self.phone_type}/close_tich_luy_dang_nhap.png", cv2.IMREAD_COLOR)
        self.img_close_tich_luy_dang_nhap2 = cv2.imread(f"{self.phone_type}/close_tich_luy_dang_nhap2.png", cv2.IMREAD_COLOR)
        self.img_close_tich_luy_dang_nhap3 = cv2.imread(f"{self.phone_type}/close_tich_luy_dang_nhap3.png", cv2.IMREAD_COLOR)
        self.img_close_tich_luy_dang_nhap4 = cv2.imread(f"{self.phone_type}/close_tich_luy_dang_nhap4.png", cv2.IMREAD_COLOR)
        self.img_close_tich_luy_dang_nhap5 = cv2.imread(f"{self.phone_type}/close_tich_luy_dang_nhap5.png", cv2.IMREAD_COLOR)
        
        self.img_close_unused_popup = cv2.imread(f"{self.phone_type}/close_unused_popup.png", cv2.IMREAD_COLOR)
        self.img_close_unused_popup2 = cv2.imread(f"{self.phone_type}/close_unused_popup2.png", cv2.IMREAD_COLOR)
        self.img_close_unused_popup3 = cv2.imread(f"{self.phone_type}/close_unused_popup3.png", cv2.IMREAD_COLOR)
        self.img_close_unused_popup4 = cv2.imread(f"{self.phone_type}/close_unused_popup4.png", cv2.IMREAD_COLOR)
        self.img_close_unused_popup5 = cv2.imread(f"{self.phone_type}/close_unused_popup5.png", cv2.IMREAD_COLOR)
        
        self.img_close_xem_not_available = cv2.imread(f"{self.phone_type}/close_xem_not_available.png", cv2.IMREAD_COLOR)
        self.img_dang_nhap_tai_khoan = cv2.imread(f"{self.phone_type}/dang_nhap_tai_khoan.png", cv2.IMREAD_COLOR)
        self.img_doi_uuid = cv2.imread(f"{self.phone_type}/doi_uuid.png", cv2.IMREAD_COLOR)
        self.img_insert_text = cv2.imread(f"{self.phone_type}/insert_text.png", cv2.IMREAD_COLOR)
        self.img_login = cv2.imread(f"{self.phone_type}/login.png", cv2.IMREAD_COLOR)
        self.img_ok_doi_uid = cv2.imread(f"{self.phone_type}/ok_doi_uid.png", cv2.IMREAD_COLOR)
        
        self.img_OK_nhan_qua = cv2.imread(f"{self.phone_type}/OK_nhan_qua.png", cv2.IMREAD_COLOR)
        self.img_OK_nhan_qua2 = cv2.imread(f"{self.phone_type}/OK_nhan_qua2.png", cv2.IMREAD_COLOR)
        self.img_OK_nhan_qua3 = cv2.imread(f"{self.phone_type}/OK_nhan_qua3.png", cv2.IMREAD_COLOR)
        self.img_OK_nhan_qua4 = cv2.imread(f"{self.phone_type}/OK_nhan_qua4.png", cv2.IMREAD_COLOR)
        self.img_OK_nhan_qua5 = cv2.imread(f"{self.phone_type}/OK_nhan_qua5.png", cv2.IMREAD_COLOR)
        self.img_OK_nhan_qua6 = cv2.imread(f"{self.phone_type}/OK_nhan_qua6.png", cv2.IMREAD_COLOR)
        self.img_OK_nhan_qua7 = cv2.imread(f"{self.phone_type}/OK_nhan_qua7.png", cv2.IMREAD_COLOR)
        
        self.img_ok_text_input = cv2.imread(f"{self.phone_type}/ok_text_input.png", cv2.IMREAD_COLOR)
        
        self.img_plus_jump_to_qc = cv2.imread(f"{self.phone_type}/plus_jump_to_qc.png", cv2.IMREAD_COLOR)
        self.img_plus_jump_to_qc2 = cv2.imread(f"{self.phone_type}/plus_jump_to_qc2.png", cv2.IMREAD_COLOR)
        self.img_plus_jump_to_qc3 = cv2.imread(f"{self.phone_type}/plus_jump_to_qc3.png", cv2.IMREAD_COLOR)
        self.img_plus_jump_to_qc4 = cv2.imread(f"{self.phone_type}/plus_jump_to_qc4.png", cv2.IMREAD_COLOR)
        self.img_plus_jump_to_qc5 = cv2.imread(f"{self.phone_type}/plus_jump_to_qc5.png", cv2.IMREAD_COLOR)
        self.img_plus_jump_to_qc6 = cv2.imread(f"{self.phone_type}/plus_jump_to_qc6.png", cv2.IMREAD_COLOR)
        
        self.img_qua_tang_qc = cv2.imread(f"{self.phone_type}/qua_tang_qc.png", cv2.IMREAD_COLOR)
        self.img_qua_tang_qc2 = cv2.imread(f"{self.phone_type}/qua_tang_qc2.png", cv2.IMREAD_COLOR)
        self.img_qua_tang_qc3 = cv2.imread(f"{self.phone_type}/qua_tang_qc3.png", cv2.IMREAD_COLOR)
        self.img_qua_tang_qc4 = cv2.imread(f"{self.phone_type}/qua_tang_qc4.png", cv2.IMREAD_COLOR)
        
        self.img_setting_btn = cv2.imread(f"{self.phone_type}/setting_btn.png", cv2.IMREAD_COLOR)
        
        self.img_show_list_uid = cv2.imread(f"{self.phone_type}/show_list_uid.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid2 = cv2.imread(f"{self.phone_type}/show_list_uid2.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid3 = cv2.imread(f"{self.phone_type}/show_list_uid3.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid4 = cv2.imread(f"{self.phone_type}/show_list_uid4.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid5 = cv2.imread(f"{self.phone_type}/show_list_uid5.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid6 = cv2.imread(f"{self.phone_type}/show_list_uid6.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid7 = cv2.imread(f"{self.phone_type}/show_list_uid7.png", cv2.IMREAD_COLOR)
        
        self.img_show_list_uid_success = cv2.imread(f"{self.phone_type}/show_list_uid_success.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid_success2 = cv2.imread(f"{self.phone_type}/show_list_uid_success2.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid_success3 = cv2.imread(f"{self.phone_type}/show_list_uid_success3.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid_success4 = cv2.imread(f"{self.phone_type}/show_list_uid_success4.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid_success5 = cv2.imread(f"{self.phone_type}/show_list_uid_success5.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid_success6 = cv2.imread(f"{self.phone_type}/show_list_uid_success6.png", cv2.IMREAD_COLOR)
        self.img_show_list_uid_success7 = cv2.imread(f"{self.phone_type}/show_list_uid_success7.png", cv2.IMREAD_COLOR)
        
        self.img_tai_khoan = cv2.imread(f"{self.phone_type}/tai_khoan.png", cv2.IMREAD_COLOR)
        self.img_text_input_username = cv2.imread(f"{self.phone_type}/text_input_username.png", cv2.IMREAD_COLOR)
        self.img_text_input_passwd = cv2.imread(f"{self.phone_type}/text_input_passwd.png", cv2.IMREAD_COLOR)
        
        self.img_tiep_tuc_dang_nhap = cv2.imread(f"{self.phone_type}/tiep_tuc_dang_nhap.png", cv2.IMREAD_COLOR)
        
        self.img_tiep_tuc_xem = cv2.imread(f"{self.phone_type}/tiep_tuc_xem.png", cv2.IMREAD_COLOR)
        self.img_tiep_tuc_xem2 = cv2.imread(f"{self.phone_type}/tiep_tuc_xem2.png", cv2.IMREAD_COLOR)
        self.img_tiep_tuc_xem3 = cv2.imread(f"{self.phone_type}/tiep_tuc_xem3.png", cv2.IMREAD_COLOR)
        
        self.img_x_quang_cao_2 = cv2.imread(f"{self.phone_type}/x_quang_cao_2.png", cv2.IMREAD_COLOR)
        
        self.img_xem_available = cv2.imread(f"{self.phone_type}/xem_available.png", cv2.IMREAD_COLOR)
        self.img_xem_available2 = cv2.imread(f"{self.phone_type}/xem_available2.png", cv2.IMREAD_COLOR)
        self.img_xem_available3 = cv2.imread(f"{self.phone_type}/xem_available3.png", cv2.IMREAD_COLOR)
        self.img_xem_available4 = cv2.imread(f"{self.phone_type}/xem_available4.png", cv2.IMREAD_COLOR)
        self.img_xem_available5 = cv2.imread(f"{self.phone_type}/xem_available5.png", cv2.IMREAD_COLOR)
        self.img_xem_available6 = cv2.imread(f"{self.phone_type}/xem_available6.png", cv2.IMREAD_COLOR)
        self.img_xem_available7 = cv2.imread(f"{self.phone_type}/xem_available7.png", cv2.IMREAD_COLOR)
        self.img_xem_available8 = cv2.imread(f"{self.phone_type}/xem_available8.png", cv2.IMREAD_COLOR)
        self.img_xem_available9 = cv2.imread(f"{self.phone_type}/xem_available9.png", cv2.IMREAD_COLOR)
        self.img_xem_available10 = cv2.imread(f"{self.phone_type}/xem_available10.png", cv2.IMREAD_COLOR)
        
        self.img_xem_not_available = cv2.imread(f"{self.phone_type}/xem_not_available.png", cv2.IMREAD_COLOR)

    def get_image_by_name(self, img_path):
        # print(f"get_image_by_name {img_path}")
        filename = os.path.basename(img_path)
        img_path = f"img_{filename}"
        img = getattr(self, img_path, None)
        if img is None:
            print(f"No image found for {img_path}")
        return img

    def open_app(self, package_name, activity_name):
        # Command to open the app
        command = f"am start -n {package_name}/{activity_name}"
        self.device.shell(command, timeout=5)
        time.sleep(2)

    def close_app(self,package_name):
        command = f"am force-stop {package_name}"
        self.device.shell(command, timeout=5)
        time.sleep(2)
    
    def go_to_home_screen(self):
        command = f"input keyevent KEYCODE_HOME"
        self.device.shell(command, timeout=5)

    def scroll_down(self, start_x, start_y, end_x, end_y):
        command = f"input swipe {start_x} {start_y} {end_x} {end_y}"
        self.device.shell(command, timeout=2)

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

    def find_center_of_img(self,template,screenshot):
        # # Load the template image
        # template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        # template = cv2.convertScaleAbs(image)
        # Convert images to the correct data type if necessary
        # screenshot = cv2.convertScaleAbs(screenshot)
        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Threshold for match confidence
        threshold = 0.8
        if max_val >= threshold:
            # Calculate the center coordinates
            top_left = max_loc
            template_width, template_height = template.shape[1], template.shape[0]
            center_x = top_left[0] + (template_width / 2)
            center_y = top_left[1] + (template_height / 2)
            return center_x, center_y
        return 0, 0

    def wait_img(self, img_path, screenshot):          
        image = self.get_image_by_name(img_path)
        match_location = self.find_image(image, screenshot)
        if match_location:
            # print("wait_img {} success".format(img_path))
            return True
        else:
            # print("wait_img {} fail".format(img_path))
            return False
    
    def click_to_img(self, img_path, screenshot):
        image = self.get_image_by_name(img_path)
        template = cv2.convertScaleAbs(image)
        screenshot = cv2.convertScaleAbs(screenshot)
        center_x, center_y = self.find_center_of_img(template, screenshot)
        
        if center_x != 0 and center_y != 0:
            self.click_to_position(center_x, center_y)
            print(f"{self.device.serial} click to {img_path} success at {center_x}:{center_y}")
            time.sleep(2)
            return True
        else:
            print(f"{self.device.serial} click to {img_path} fail")
            time.sleep(1)  # Wait for 1 second before retrying
            return False
    
    def click_left_of_img(self, img_path, screenshot):
        image = self.get_image_by_name(img_path)
        template = cv2.convertScaleAbs(image)
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
            print(f"{self.device.serial} click to {img_path} success at {center_x}:{center_y}")
            return True
        else:
            return None

    def click_to_position(self, x, y):
        command = f"input tap {x} {y}"
        self.device.shell(command, timeout=5)
        
    def swipe_list_uid(self, img_path, screenshot):
        image = self.get_image_by_name(img_path)
        template = cv2.convertScaleAbs(image)
        screenshot = cv2.convertScaleAbs(screenshot)
        center_x, center_y = self.find_center_of_img(template, screenshot)

        # from
        template_width, template_height = template.shape[1], template.shape[0]
        from_x = center_x - (template_width * 3)
        from_y = center_y - (template_height * 3)
        
        # to
        dst_x = from_x
        dst_y = from_y - (template_height * 6)
        print(f"{self.device.serial} swipe")
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        self.scroll_down(from_x, from_y, dst_x, dst_y)
        
    def select_last_uid(self, img_path, screenshot):
        image = self.get_image_by_name(img_path)
        template = cv2.convertScaleAbs(image)
        screenshot = cv2.convertScaleAbs(screenshot)
        center_x, center_y = self.find_center_of_img(template, screenshot)

        # from
        # default image size
        image = self.get_image_by_name("add_uid")
        template = cv2.convertScaleAbs(image)
        template_width, template_height = template.shape[1], template.shape[0]
        
        from_x = center_x
        from_y = center_y - (template_height * 1)
        self.click_to_position(from_x, from_y)
        print(f"{self.device.serial} click last uid success at {from_x}:{from_y}")
        
    def click_to_join_game(self, screenshot):
        image = self.get_image_by_name("show_list_uid")
        template = cv2.convertScaleAbs(image)
        screenshot = cv2.convertScaleAbs(screenshot)
        center_x, center_y = self.find_center_of_img(template, screenshot)

        # from
        template_width, template_height = template.shape[1], template.shape[0]
        from_x = center_x + (template_width * 3)
        from_y = center_y + (template_height * 3)
        self.click_to_position(from_x, from_y)
        print(f"{self.device.serial} click_to_join_game success at {from_x}:{from_y}")