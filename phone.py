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
        adb_cmd = f"adb shell am force-stop {package_name}"
        subprocess.run(adb_cmd, shell=True)

    
    # def capture_screen(self):
    #     print("capture_screens " + self.device.serial)
    #     result = self.device.screencap()
    #     img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
        
    #     self.screen_img = "{}.png".format(self.device.serial)
    #     with open(self.screen_img, "wb") as fp:
    #         fp.write(result)
    #         print("save screen image")

    def capture_screen(self):
        # Run adb command to capture a screenshot
        adb_cmd = "adb exec-out screencap -p"
        adb_process = subprocess.Popen(adb_cmd, shell=True, stdout=subprocess.PIPE)
        # screenshot_bytes = adb_process.stdout.read()
        screenshot_bytes, _ = adb_process.communicate()
        # Convert the screenshot bytes to a numpy array
        screenshot_np = np.frombuffer(screenshot_bytes, dtype=np.uint8)
        # Decode the numpy array as an OpenCV image
        screenshot = cv2.imdecode(screenshot_np, cv2.IMREAD_COLOR)
        return screenshot

    
    # def find_image(self, template_path, screenshot):
    #     # Load the target image
    #     template = cv2.imread(template_path, cv2.IMREAD_COLOR)

    #     # Resize the template image to match the size of the screenshot
    #     template = cv2.resize(template, (screenshot.shape[1], screenshot.shape[0]))

    #     # Search for the target image within the screenshot
    #     result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    #     # Threshold for match confidence
    #     threshold = 0.8
    #     if max_val >= threshold:
    #         return max_loc
    #     else:
    #         return None
    
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

    def click_de_vao_game(self):
        screenshot = self.capture_screen()
        template = cv2.imread("login.png", cv2.IMREAD_COLOR)
        template_width, template_height = template.shape[1], template.shape[0]
        
        match_location = self.find_image("login.png", screenshot)
        if match_location:
            print("login.png image found at location:", match_location)
            # Get screen dimensions
            # Calculate center coordinates
            center_x = template_width / 4
            center_y = template_height / 4
            self.click_to_position(center_x, center_y)
            
            return True
        else:
            print("login.png image not found on the screen. Retrying in 1 second...")
            time.sleep(1)  # Wait for 1 second before retrying
            
            return False
    
    def wait_main_screen(self):
        screenshot = self.capture_screen()
        match_location = self.find_image("home.png", screenshot)
        
        if match_location:
            return True
        else:
            return False
    
    def click_to_person(self):
        screenshot = self.capture_screen()
        
        # Load input image (screenshot) and template image
        template = cv2.imread("nhan_vat.png", cv2.IMREAD_COLOR)
        # Convert images to the correct data type if necessary
        screenshot = cv2.convertScaleAbs(screenshot)
        template = cv2.convertScaleAbs(template)

        center_x, center_y = self.find_center_of_img("nhan_vat.png", screenshot)
    
        if center_x != 0 and center_y != 0:
            self.click_to_position(center_x, center_y)
            print("click_to_person success")
            return True
        else:
            time.sleep(1)  # Wait for 1 second before retrying
            return False
        
        
    def click_to_quang_cao(self):
        screenshot = self.capture_screen()
        
        # Load input image (screenshot) and template image
        template = cv2.imread("quang_cao.png", cv2.IMREAD_COLOR)
        # Convert images to the correct data type if necessary
        screenshot = cv2.convertScaleAbs(screenshot)
        template = cv2.convertScaleAbs(template)
        
        center_x, center_y = self.find_center_of_img("quang_cao.png", screenshot)
    
        if center_x != 0 and center_y != 0:
            self.click_to_position(center_x, center_y)
            print("click_to_quang_cao success")
            return True
        else:
            time.sleep(1)  # Wait for 1 second before retrying
            return False


    def click_to_position(self, x, y):
        command = f"input tap {x} {y}"
        self.device.shell(command)

