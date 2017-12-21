import cv2

cv2.namedWindow('video')
cap = cv2.VideoCapture(1)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('video/ball_bitec3.avi',fourcc,20.0,(640,480))
sw_state = 0

while True:

	ret,img = cap.read()

	if ret == True:

		cv2.imshow('video', img)
		if sw_state == 1:
			out.write(img)

		k = cv2.waitKey(20)
		if k == ord('q'):
			break
		elif k == ord('r'):
			if sw_state == 0:
				sw_state = 1
				print 'record'
			elif sw_state == 1:
				sw_state = 0
				print 'finish'



cap.release()
cv2.destroyAllWindows()
