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

    
    def capture_screen(self):
        print("capture_screens " + self.device.serial)
        result = self.device.screencap()
        img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
        
        self.screen_img = "{}.png".format(self.device.serial)
        with open(self.screen_img, "wb") as fp:
            fp.write(result)
            print("save screen image")

    def find(self,template_img_file="img.png",threshold=0.99):
        print("find image " + template_img_file)
        point = (0,0)
        img = cv2.imread(self.screen_img)
        img2 = cv2.imread(template_img_file)
        _, w2, h2 = img2.shape[::-1]

        res = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        top_left = max_loc
        bottom_right = (top_left[0] + w2, top_left[1] + h2)

        # draw rectangle
        print(top_left)
        print(bottom_right)
        cv2.rectangle(img,top_left, bottom_right, (0, 255, 255), 0)
        cv2.imshow('img', img)
        cv2.imshow('img2', img2)
        cv2.waitKey(0)
    
        point = (top_left[0] + w2/2, top_left[1] + h2/2)
        return point

    def get_screen_dimensions(self):
        # Run adb command to get the screen dimensions
        adb_cmd = "adb shell wm size"
        result = subprocess.run(adb_cmd, shell=True, capture_output=True, text=True)
        output = result.stdout.strip()
        # Extract screen width and height from the output
        width, height = map(int, output.split()[-1].split('x'))
        return width, height

    def click_center_of_screen(self):
        # Get screen dimensions
        width, height = self.get_screen_dimensions()
        # Calculate center coordinates
        center_x = width // 2
        center_y = height // 2
        # Run adb command to send a tap event at the center of the screen
        adb_cmd = f"adb shell input tap {center_x} {center_y}"
        print(adb_cmd)
        subprocess.run(adb_cmd, shell=True)

    def click_to_position(self, x, y):
        command = f"input tap {x} {y}"
        self.device.shell(command)

