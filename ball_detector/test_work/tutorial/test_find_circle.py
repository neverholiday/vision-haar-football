import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",help = "Add image ngai kwai")
ap.add_argument("-v","--video",help = "directory or self video")
ap.add_argument("-m","--mode",help = "mode Auto or Manual",required = True)
args = vars(ap.parse_args())

ret = True
pauseToggle = 0
wait = 10

def nothing(x):
    pass

cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.namedWindow("mask",cv2.WINDOW_NORMAL)
cv2.namedWindow("edge",cv2.WINDOW_NORMAL)
if(args["mode"] == "Manual"):
    cv2.createTrackbar('h_low', 'image', 0, 179, nothing)
    cv2.createTrackbar('h_high', 'image', 0, 179, nothing)
    cv2.createTrackbar('s_low', 'image', 0, 255, nothing)
    cv2.createTrackbar('s_high', 'image', 0, 255, nothing)
    cv2.createTrackbar('v_low', 'image', 0, 255, nothing)
    cv2.createTrackbar('v_high', 'image', 0, 255, nothing)

    cv2.createTrackbar('h_low_ball', 'image', 0, 179, nothing)
    cv2.createTrackbar('h_high_ball', 'image', 0, 179, nothing)
    cv2.createTrackbar('s_low_ball', 'image', 0, 255, nothing)
    cv2.createTrackbar('s_high_ball', 'image', 0, 255, nothing)
    cv2.createTrackbar('v_low_ball', 'image', 0, 255, nothing)
    cv2.createTrackbar('v_high_ball', 'image', 0, 255, nothing)

elif(args["mode"] == "CIRCLE"):
    cv2.createTrackbar('min', 'mask', 1, 200, nothing)
    cv2.createTrackbar('max', 'mask', 1, 200, nothing)




if(args["video"] is not None):
    if(args["video"] == "WEBCAM"):
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(args["video"])

while True:
    if(args["image"] is not None):
        image_directory = args["image"]
        img = cv2.imread(image_directory)
    if(args["video"] is not None):
        ret,img = cap.read()
    
    
    if(ret is True):
    # print ret

        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        if(args["mode"] == "Manual"):
            h_low = cv2.getTrackbarPos('h_low',  'image')
            h_high = cv2.getTrackbarPos('h_high','image')
            s_low = cv2.getTrackbarPos('s_low',  'image')
            s_high = cv2.getTrackbarPos('s_high','image')
            v_low = cv2.getTrackbarPos('v_low',  'image')
            v_high = cv2.getTrackbarPos('v_high','image')

            h_low_ball = cv2.getTrackbarPos('h_low_ball',  'image')
            h_high_ball = cv2.getTrackbarPos('h_high_ball','image')
            s_low_ball = cv2.getTrackbarPos('s_low_ball',  'image')
            s_high_ball = cv2.getTrackbarPos('s_high_ball','image')
            v_low_ball = cv2.getTrackbarPos('v_low_ball',  'image')
            v_high_ball = cv2.getTrackbarPos('v_high_ball','image')

            lower_bound = np.array([h_low,s_low,v_low])
            upper_bound = np.array([h_high,s_high,v_high])

            lower_bound_ball = np.array([h_low_ball,s_low_ball,v_low_ball])
            upper_bound_ball = np.array([h_high_ball,s_high_ball,v_high_ball])

        elif(args["mode"] == "CIRCLE" or args["mode"] == "Auto" ):
            
            # Green
            # lower_bound = np.array([35,63,0])
            # upper_bound = np.array([49,255,255])
            
            # Football
            # lower_bound = np.array([0,0,0])
            # upper_bound = np.array([179,25,255])
            
            # Green
            lower_bound = np.array([44,40,0]) 
            upper_bound = np.array([85,255,255])

            lower_bound_ball = np.array([0,0,0])
            upper_bound_ball = np.array([119,48,255])
            maxValue = cv2.getTrackbarPos("max","mask")
            minValue = cv2.getTrackbarPos("min","mask")

        mask = cv2.inRange(img_hsv,np.array(lower_bound),np.array(upper_bound))
        # mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel = np.ones((3,3),dtype=np.uint8))
        mask = cv2.dilate(mask,kernel = np.ones((5,5),dtype=np.uint8),iterations=1)

        mask_ball = cv2.inRange(img_hsv,np.array(lower_bound_ball),np.array(upper_bound_ball))
        mask_ball = cv2.dilate(mask_ball,kernel = np.ones((5,5),dtype=np.uint8),iterations=1)
        # mask_ball = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel = np.ones((3,3),dtype=np.uint8))

        # ret,th1 = cv2.threshold(mask,127,255,cv2.THRESH_BINARY_INV)
        edges = cv2.Canny(mask,100,200)

        mask_final = cv2.bitwise_and(mask,mask_ball)

        if(args["mode"] == "CIRCLE" or args["mode"] == "Auto" ):
            # _,contours,_ = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            
            # # for cnt in contours:
            # for cnt in contours:
            #     hull = cv2.convexHull(cnt)
            #     cv2.drawContours(mask,[hull],-1,(255,0,0),5)
            
            if(args["mode"] == "CIRCLE"):
                circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,param1 = minValue,param2 = 18,minRadius=0,maxRadius=0)
                # print circles
                if(circles is not None):
                    circles = np.uint16(np.around(circles))
                    for i in circles[0,:]:
                    # draw the outer circle
                        cv2.circle(img,(i[0],i[1]),i[2],(0,0,0),2)
        

        res = cv2.bitwise_and(img,img,mask=mask_final)
        
        maskShow = np.hstack((mask,mask_ball,mask_final))
        
        cv2.imshow("mask",maskShow)
        cv2.imshow("image",res)
        cv2.imshow("edge",edges)

        k = cv2.waitKey(wait)
        if(k == ord('q')):
            break
        elif(k == ord('p')):
            pauseToggle += 1
            if(pauseToggle > 1):
                pauseToggle = 0
            
            if(pauseToggle == 0):
                wait = 10
            elif(pauseToggle == 1):
                wait = 0

            
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

# print hull
cv2.destroyAllWindows()