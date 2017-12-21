from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('image/shape_predict.dat')

cap = cv2.VideoCapture(0)

# fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# out = cv2.VideoWriter('output.avi',fourcc, 20.0, (500,375))

while True :

	ret,img = cap.read()


	# img = cv2.imread('test.jpg')
	img = imutils.resize(img,width=500)

	gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	detects = detector(gray_img,1)

	for (i,detect) in enumerate(detects):

		shape = predictor(gray_img,detect)
		shape = face_utils.shape_to_np(shape)

		(x,y,w,h) = face_utils.rect_to_bb(detect)
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

		for (x,y) in shape:
			cv2.circle(img,(x,y),1,(0,0,255),-1)

	# out.write(img)
	cv2.imshow('image',img)
	# print img.shape[0] , img.shape[1]

	k = cv2.waitKey(5)
	if k == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()