import cv2
import numpy as np

def nothing(x):
	pass

cv2.namedWindow("img")
cv2.namedWindow("mask")
cv2.createTrackbar('y_low', 'img', 0, 179, nothing)
cv2.createTrackbar('y_high', 'img', 0, 179, nothing)
cv2.createTrackbar('u_low', 'img', 0, 255, nothing)
cv2.createTrackbar('u_high', 'img', 0, 255, nothing)
cv2.createTrackbar('v_low', 'img', 0, 255, nothing)
cv2.createTrackbar('v_high', 'img', 0, 255, nothing)

while( True ):
	img = cv2.imread("test_find_ball2.jpg")
	
	y_low = cv2.getTrackbarPos('y_low',"img")
	y_high = cv2.getTrackbarPos('y_high',"img")
	u_low = cv2.getTrackbarPos('u_low',"img")
	u_high = cv2.getTrackbarPos('u_high',"img")
	v_low = cv2.getTrackbarPos('v_low',"img")
	v_high = cv2.getTrackbarPos('v_high',"img")

	lower_bound = np.array((y_low,u_low,v_low),dtype=np.uint8)
	upper_bound = np.array((y_high,u_high,v_high),dtype=np.uint8)
	

	img_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
	mask = cv2.inRange(img_yuv,lower_bound,upper_bound)

	stack = np.hstack((img,img_yuv))
	cv2.imshow("img",stack)
	cv2.imshow("mask",mask)
	k = cv2.waitKey(5)
	if( k == ord('q')):
		break
cv2.destroyAllWindows()