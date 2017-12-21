import cv2
import numpy as np
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-m","--mode",help = "calibrate or use default",required = True)
args = vars(ap.parse_args())


def nothing(x):
	pass


_ = True
cv2.namedWindow('img')

# cv2.namedWindow('contour')
if args["mode"] == "Manual":
	cv2.createTrackbar('h_low', 'img', 0, 179, nothing)
	cv2.createTrackbar('h_high', 'img', 0, 179, nothing)
	cv2.createTrackbar('s_low', 'img', 0, 255, nothing)
	cv2.createTrackbar('s_high', 'img', 0, 255, nothing)
	cv2.createTrackbar('v_low', 'img', 0, 255, nothing)
	cv2.createTrackbar('v_high', 'img', 0, 255, nothing)

# img = cv2.imread('3.jpg')
# cap = cv2.VideoCapture('raw.avi')
cap = cv2.VideoCapture(1)
# cap = cv2.VideoCapture("video/ball_bitec3.avi")

# img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

blue = np.uint8([[[0,0,255]]])
green = np.uint8([[[0,255,0]]])
red = np.uint8([[[255,0,0]]])
kernel = np.ones((10,10),np.uint8)
color_list = [blue,green,red]

for i in color_list:
	hsv = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
	print hsv

while True:

	_,img = cap.read()
	# img = cv2.imread("../tutorial/3.jpg")

	if _ == True:
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		if args["mode"] == "Manual":	
			h_low = cv2.getTrackbarPos('h_low',  'img')
			h_high = cv2.getTrackbarPos('h_high','img')
			s_low = cv2.getTrackbarPos('s_low',  'img')
			s_high = cv2.getTrackbarPos('s_high','img')
			v_low = cv2.getTrackbarPos('v_low',  'img')
			v_high = cv2.getTrackbarPos('v_high','img')

			lower = np.array([h_low,s_low,v_low]) 
			higher = np.array([h_high,s_high,v_high])

		
		
		elif args["mode"] == "Auto":
			lower = np.array([54,110,55]) 
			higher = np.array([85,255,255])
			lower_ball = np.array([127,67,37]) 
			higher_ball = np.array([255,255,255])

		mask = cv2.inRange(img_hsv, lower, higher)
		mask2 = cv2.inRange(img,lower_ball,higher_ball)
		
		mask_all = cv2.bitwise_and(mask,mask2)

		res1 = cv2.bitwise_and(img, img,mask=mask_all)
		# res2 = cv2.bitwise_and(img,img,mask=mask2)
		# cv2.imshow('mask1',mask)
		# cv2.imshow('res1', res1)
		
		im2 , contour , hier = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		# moment = cv2.moments(contour[-1])
		# cx = int(moment['m10']/moment['m00'])
		# cy = int(moment['m01']/moment['m00'])
		# print cx,cy
		cv2.drawContours(img, contour, -1, (0,0,0),3)

		stack = np.hstack((res1,img))
		cv2.imshow('img', stack)

		# cv2.imshow('img',img)
		k = cv2.waitKey(20)
		if k == ord('q'):
			break
		elif k == ord('p'):
			ret,th2 = cv2.threshold(mask.copy(),127,255,cv2.THRESH_BINARY_INV)
			cv2.imshow("mask",th2)
			cv2.waitKey(0)
	else:
		cap.set(cv2.CAP_PROP_POS_MSEC,0)
		# pass

cap.release()
cv2.destroyAllWindows()	
