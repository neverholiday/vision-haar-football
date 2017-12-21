import cv2
import numpy as np


def nothing(x):
    pass


cv2.namedWindow("image")
cv2.createTrackbar('low', 'image', 20, 200, nothing)
cv2.createTrackbar('high', 'image', 500, 1000, nothing)
# print th1
while True:

    img = cv2.imread("gradient.jpg",0)
    # ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)

    low = cv2.getTrackbarPos("low","image")
    high = cv2.getTrackbarPos("high","image")
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1.5,20,
                            param1=10,param2=high,minRadius=20,maxRadius=0)
    # print circles
    if(circles is not None):
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
        # draw the outer circle
            cv2.circle(img,(i[0],i[1]),i[2],(255,255,255),2)
    
    cv2.imshow("image",img)
    k = cv2.waitKey(5)
    if(k == ord('q')):
        break

# print circles
cv2.destroyAllWindows()