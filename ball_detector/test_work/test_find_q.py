import cv2

cv2.namedWindow('img',cv2.WINDOW_NORMAL)
cv2.namedWindow('img_plot',cv2.WINDOW_NORMAL)
img = cv2.imread('1.jpg')
img_plot = img
print img.shape

# horizontal
cv2.line(img, (0,img.shape[0]/2),(img.shape[1],img.shape[0]/2), (255,255,255),5)
cv2.line(img_plot, (0,img.shape[0]/2),(img.shape[1],img.shape[0]/2), (255,255,255),5)

# vertical

cv2.line(img, (img.shape[1]/2,0),(img.shape[1]/2,img.shape[0]), (255,255,255),5)
cv2.line(img_plot,(img.shape[1]/2,0),(img.shape[1]/2,img.shape[0]), (255,255,255),5)


# while True:

x = int(raw_input('x : '))
y = int(raw_input('y : '))

# Q1
if x > 320 and y < 240:
	print 'Q1'
# Q2
if x < 320 and y < 240:
	print 'Q2'
if x < 320 and y > 240:
	print 'Q3'
if x > 320 and y > 240:
	print 'Q4'

img_plot = cv2.circle(img, (x,y), 5, (255,255,255),-1)
cv2.imshow('img_plot', img_plot)
cv2.imshow('img', img)
cv2.waitKey(0)
	# if q == ord('q'):
	# 	break

cv2.destroyAllWindows()