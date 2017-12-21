import urllib
import cv2
import numpy as np

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(0)
hc = cv2.CascadeClassifier("ball_20s.xml")
while True:
	_,img = cap.read()
	img = img[:,:img.shape[0]]
	print img.shape
	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)	

	
	footballs = hc.detectMultiScale(img_gray) 

	for (x,y,w,h) in footballs:
		cv2.rectangle(img, (x, y), (x+w,y+h), (255, 0, 0), 2)

	cv2.imshow('image',img)
	k = cv2.waitKey(1)
	if k == ord('q'):
		break


cv2.destroyAllWindows()