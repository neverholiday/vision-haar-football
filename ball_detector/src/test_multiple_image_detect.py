# ###################################################
# See only function cameraAvailable

import cv2
import numpy as np
import argparse
from configobj import ConfigObj
import time


parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="directory image")
parser.add_argument("--mode",help = "capture hard negative")
args = parser.parse_args()

# Path to file XML, edit here
# path_xml = 'xml_file/data_haar_121217_13.xml'
path_xml = 'xml_file/data_rcap3.xml' 

calibrateA = 1.3
calibrateB = 10
print args.dir

def nothing(x):
    pass
     
def haarDetect(img):
    # hc = cv2.CascadeClassifier('xml_file/ball_new_9_10_2017.xml')
    
    hc = cv2.CascadeClassifier(path_xml)
    footballs = hc.detectMultiScale(img,calibrateA,calibrateB)
    
    return footballs

def gradientImg(img):
    img = np.float32(img) / 255.0
    
    # Calculate gradient 
    grad_x = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=1)
    grad_y = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=1)
    mag, angle = cv2.cartToPolar(grad_x, grad_y, angleInDegrees=True)

    return mag

def thresholdImg(img):
    
    ret,threshImage = cv2.threshold(img,10,50,cv2.THRESH_BINARY)
    return threshImage


def cameraAvailable(desicion):
    '''
    Parameter : Boolean 
    '''
    cv2.namedWindow("image",cv2.WINDOW_NORMAL)
    cv2.namedWindow("mask",cv2.WINDOW_NORMAL)
    cv2.namedWindow("detect",cv2.WINDOW_NORMAL)
    lower = np.array([28,108,100]) 
    higher = np.array([82,255,255])
    kernel = np.ones((5,5),np.uint8)

    if (desicion is True):
        # cap = cv2.VideoCapture("video/dowaina_chattarin_5.avi")
        cap = cv2.VideoCapture("video/ball_bitec.avi")
        # cap = cv2.VideoCapture(1)
        # scanlanmark = ScanLandmark(ConfigObj("colordef.ini"), is_do_horizontal = False)
        while True:
            _,img = cap.read()

            if(_ == True):
                # Convert to grayscale image  and use HAAR-feature to detect football on camera frame
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                footballs = haarDetect(img_gray)

                # save when frame detect false positive
                if(args.mode == "CAPTURE_HARD_NEGATIVE"):
                    if(len(footballs) > 1):
                        file_name = "image/hard_negative/" + str(int(time.time())) + ".jpg"
                        cv2.imwrite(file_name,img)

                # Convert to hsv color space 
                img_hsv = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2HSV)

                # Create field mask   
                mask = cv2.inRange(img_hsv, lower, higher)
                mask = cv2.dilate(mask,kernel,iterations = 1)

                # Find contours
                ret,contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                
                # Find max contour area and eliminate remain contours
                maxCnt = max(contours,key=lambda x:cv2.contourArea(x))
                convexCnt = cv2.convexHull(maxCnt)
                mask = np.zeros(mask.shape, mask.dtype)
                
                # Draw max contour area
                cv2.drawContours(mask,[convexCnt],-1,255,-1)

                # Check coordinate of football on the field 
                for (x,y,w,h) in footballs:
                    positionX = x+w/2
                    positionY = y+h/2
                    polygonTest = cv2.pointPolygonTest(convexCnt,(positionX,positionY),measureDist=False)

                    # Check all coordinates from "footballs" if coordinates are on the field, that will be a football
                    if(polygonTest == 1):
                        cv2.circle(img,(positionX,positionY),w/2,(255,255,255),3)
                        # Use coordinate after this (PositionX,PositionY)
                    elif (polygonTest == -1):
                        cv2.circle(img,(positionX,positionY),w/2,(0,0,255),3)

                res = cv2.bitwise_and(img, img,mask=mask)

                cv2.imshow("image",res)
                cv2.imshow("mask",mask)
                cv2.imshow("detect",img)
                k = cv2.waitKey(1)
                if k == ord('q'):
                    break
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        
        cv2.destroyAllWindows()

    elif (desicion is False):
        img = cv2.imread(args.dir,0)
        # img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = cv2.blur(img, (100, 100))

        img_32 = np.float32(img.copy()) / 255.0

        sobelX = cv2.Sobel(img_32,cv2.CV_32F,1,0,ksize=1)
        sobelY = cv2.Sobel(img_32,cv2.CV_32F,0,1,ksize=1)
        
        mag,angle = cv2.cartToPolar(sobelX,sobelY,angleInDegrees=True)
        
        mag = mag *127
        mag = np.uint8(mag)

        _,contours,hierchy = cv2.findContours(mag,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        # maxCnt = max(contours,key=lambda x:cv2.contourArea(x))
        # maxCnt
        # print maxCnt
        # print contours
        # cnt = contours.remove([maxCnt])
        # # print type(contours)
        cv2.drawContours(mag,contours,-1,(255,255,255),-1)
        
        # cv2.imwrite("gradient.jpg",mag)
            # draw the outer circle
        # mag = thresholdImg(mag)
        # footballs = haarDetect(img_gray)

        # for (x,y,w,h) in footballs:
        #     positionX = x+w/2
        #     positionY = y+h/2
        #     cv2.circle(img,(positionX,positionY),w/2,(255,255,255),3)
        # stack = np.hstack((img,mag))
        cv2.imshow("image",mag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    if(args.dir is None):
        cameraAvailable(True)
    else:
        cameraAvailable(False)

if __name__ == '__main__':
    main()
    