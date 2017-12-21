import cv2

cv2.namedWindow('img')

# img = cv2.imread('dim.jpg')

# print img.shape
cap = cv2.VideoCapture(0)

while True:
	_,img = cap.read()

	x = (img.shape[1]/2) - 100
	y = (img.shape[0]/2) - 100
	# print x , y
	if _ == True:
		cv2.rectangle(img, (x,y), (x+200,y+200), (255,0,0),2)


		cv2.imshow('img',img)

		k = cv2.waitKey(1)
		if k == ord('q'):
			break

cap.release()			
cv2.destroyAllWindows()