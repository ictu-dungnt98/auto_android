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
        self.screen_img = ""
    
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

    def capture_screen(self):
        # Run adb command to capture a screenshot
        screenshot_bytes = self.device.screencap()
        # Convert the screenshot bytes to a numpy array
        screenshot_np = np.frombuffer(screenshot_bytes, dtype=np.uint8)
        # Decode the numpy array as an OpenCV image
        screenshot = cv2.imdecode(screenshot_np, cv2.IMREAD_COLOR)
        return screenshot
  
    def find_image(self, template_path, screenshot):
        # Load the template image
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)

        # Convert images to the correct data type if necessary
        screenshot = cv2.convertScaleAbs(screenshot)
        template = cv2.convertScaleAbs(template)

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


    def find_center_of_img(self,template_path,screenshot):
        # # Load the template image
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        # Convert images to the correct data type if necessary
        screenshot = cv2.convertScaleAbs(screenshot)
        template = cv2.convertScaleAbs(template)
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
        match_location = self.find_image(img_path, screenshot)
        if match_location:
            return True
        else:
            return False
    
    def click_to_img(self, img_path, screenshot):
        
        # Load input image (screenshot) and template image
        template = cv2.imread(img_path, cv2.IMREAD_COLOR)
        # Convert images to the correct data type if necessary
        screenshot = cv2.convertScaleAbs(screenshot)
        template = cv2.convertScaleAbs(template)

        center_x, center_y = self.find_center_of_img(img_path, screenshot)
    
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
        template = cv2.imread(img_path, cv2.IMREAD_COLOR)
        # Convert images to the correct data type if necessary
        screenshot = cv2.convertScaleAbs(screenshot)
        template = cv2.convertScaleAbs(template)

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

