import cv2
import numpy as np
import time

def nothing(x):
	pass
def find_q(x,y,size_img):
	if x > size_img[1]/2 and y < size_img[0]/2:
		print 'Q1'
		# return 1
	if x < size_img[1]/2 and y < size_img[0]/2:
		print 'Q2'
		# return 2
	if x < size_img[1]/2 and y > size_img[0]/2:
		print 'Q3'
		# return 3
	if x > size_img[1]/2 and y > size_img[0]/2:
		print 'Q4'
		# return 4

state_pause = 0
bool_record = 0


cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('bar')
cv2.createTrackbar('scale_factor', 'bar', 11,50 , nothing)
cv2.createTrackbar('min_neighbor', 'bar', 3, 50, nothing)

# cap = cv2.VideoCapture('video/sample_4.avi')
# cap = cv2.VideoCapture('video/ball_09_10_2017.avi')
cap = cv2.VideoCapture(1)
# hc = cv2.CascadeClassifier("ball_new_14s.xml")
# hc = cv2.CascadeClassifier("ball_new_22_08_2017.xml")
# hc = cv2.CascadeClassifier('xml_file/ball_new_9_10_2017.xml')
hc = cv2.CascadeClassifier('xml_file/ball_lbp2.xml')
font = cv2.FONT_HERSHEY_SIMPLEX

if bool_record:
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('video/' +  str(int(time.time())) + '.avi',fourcc, 20.0, (640,480))

divider = 10.0
while True:
	if state_pause == 0:
		_,img = cap.read()

		# if _ is True:
		# _ = cap.set(3,320)
		# _ = cap.set(4,240)
		img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)	
		scale_factor = cv2.getTrackbarPos('scale_factor', 'bar')
		min_neighbor = cv2.getTrackbarPos('min_neighbor', 'bar')

		scale_factor = scale_factor / float(divider) 
		time1 = cv2.getTickCount()

		if bool_record:
			footballs = hc.detectMultiScale(img_gray,1.7,7)
		else:
			footballs = hc.detectMultiScale(img_gray,scale_factor,min_neighbor)
		
		time2 = cv2.getTickCount()

		# print cv2.getTickFrequency()

		fps = (time2 - time1) / cv2.getTickFrequency()
		# fps = (time2 - time1) 
		cv2.putText(img,str(1/fps),(30,30),font,1,(0,0,0),2,cv2.LINE_AA)


		#  17s = 1.7,7  10s = 2,35 # 20s = 1.1,5 or 4 (small ball or big) 
	 
		for (x,y,w,h) in footballs:
			cv2.rectangle(img, (x, y), (x+w,y+h), (255, 0, 0), 2)

		cv2.imshow('image',img)
		if bool_record :
			out.write(img)


		# else:
		# 	break

	k = cv2.waitKey(30)
	if k == ord('q'):
		break
	elif k == ord('p'):
		if state_pause == 0:
			state_pause = 1
		else:
			state_pause = 0

cap.release()
cv2.destroyAllWindows()



# should have cursor for robot vision
# 
