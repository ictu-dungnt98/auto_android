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

class Emulator:
    def __init__(self, device):
        self.device = device
        self.screen_img = ""
    
    def capture_screen(self):
        print("capture_screens " + self.device.serial)
        result = self.device.screencap()
        img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
        
        self.screen_img = "{}.png".format(self.device.serial)
        cv2.imwrite(self.screen_img, img)
        # with open(self.screen_img, "wb") as fp:
        #     fp.write(result)
        #     print("save screen image")

    def open_app(self, x, y):
        print("open_app {} {}".format(x, y))
        self.device.input_tap(x, y)

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
