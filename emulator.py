
try: 
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
        print (self.device.serial)
        result = self.device.screencap()
        self.screen_img = "{}.png".format(self.device.serial.split(":")[1])
        with open(self.screen_img, "wb") as fp:
            fp.write(result)

    def find(self,template_pic_name=False,threshold=0.99):
        point = (0,0)
        if template_pic_name == False:
            return point
        
        img = cv2.imread(self.screen_img)
        img2 = cv2.imread("facebook.PNG")
        
        _, w1, h1 = img.shape[::-1]
        _, w2, h2 = img2.shape[::-1]

        print(w1, h1)
        print(w2, h2)

        res = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w2, top_left[1] + h2)

        # print(top_left)
        # print(bottom_right)
        # cv2.rectangle(img,top_left, bottom_right, (0, 255, 255), 0)
        # cv2.imshow('fb', img)
        # cv2.waitKey(0)
    
        point = (top_left[0] + w2/2, top_left[1] + h2/2)
        self.device.input_tap(point[0], point[1])
