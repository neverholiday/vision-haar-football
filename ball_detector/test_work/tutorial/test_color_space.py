import cv2
import numpy as np

def nothing(x):
	pass

cv2.namedWindow('img')
cv2.namedWindow('mask')
cv2.namedWindow('res')
# cv2.namedWindow('contour')

cv2.namedWindow('bar')
cv2.createTrackbar('h_low', 'bar', 0, 179, nothing)
cv2.createTrackbar('h_high', 'bar', 0, 179, nothing)
cv2.createTrackbar('s_low', 'bar', 0, 255, nothing)
cv2.createTrackbar('s_high', 'bar', 0, 255, nothing)
cv2.createTrackbar('v_low', 'bar', 0, 255, nothing)
cv2.createTrackbar('v_high', 'bar', 0, 255, nothing)

# img = cv2.imread('3.jpg')
# cap = cv2.VideoCapture('raw.avi')
cap = cv2.VideoCapture(1)

# img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

blue = np.uint8([[[0,0,255]]])
green = np.uint8([[[0,255,0]]])
red = np.uint8([[[255,0,0]]])

color_list = [blue,green,red]

for i in color_list:
	hsv = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
	print hsv

while True:

	_,img = cap.read()

	if _ == True:
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		
		h_low = cv2.getTrackbarPos('h_low',  'bar')
		h_high = cv2.getTrackbarPos('h_high','bar')
		s_low = cv2.getTrackbarPos('s_low',  'bar')
		s_high = cv2.getTrackbarPos('s_high','bar')
		v_low = cv2.getTrackbarPos('v_low',  'bar')
		v_high = cv2.getTrackbarPos('v_high','bar')

		lower = np.array([h_low,s_low,v_low]) 
		higher = np.array([h_high,s_high,v_high]) 
		# lower = np.array([62,78,90]) #62 78 90
		# higher = np.array([137,178,210]) #137 178 210

		mask = cv2.inRange(img_hsv, lower, higher)

		res = cv2.bitwise_and(img, img,mask=mask)

		cv2.imshow('mask',mask)
		cv2.imshow('res', res)
		
		# im2 , contour , hier = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		# ___,contour , hier = cv2.findContours(mask,1,2)
		# moment = cv2.moments(contour[-1])
		# cx = int(moment['m10']/moment['m00'])
		# cy = int(moment['m01']/moment['m00'])
		# print cx,cy
		# cv2.drawContours(img, contour, -1, (0,0,255),3)

		cv2.imshow('img', img)

		# cv2.imshow('img',img)
		k = cv2.waitKey(1)
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
