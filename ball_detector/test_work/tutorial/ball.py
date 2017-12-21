import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def haar_one(integral):
	black = integral[20][10] - integral[1][10] - integral[20][1] + integral[1][1]
	white = integral[20][20] - integral[1][20] - integral[20][11] + integral[11][11]
	# print white,black
	feat = white - black
	return feat

def haar_two(integral):
	black = integral[20][20] - integral[11][20] - integral[20][1] + integral[11][1]
	white = integral[10][20] - integral[1][20] - integral[10][1] + integral[1][1]
	feat = white - black
	return feat

def crop(_dir):
	listDir = os.listdir(_dir)
	if 'info.lst' in listDir or 'test.py' in listDir:
		listDir.remove('info.lst')
		listDir.remove('test.py')
	for name in listDir:
		Dir = _dir+'/'+name
		print Dir
		# time.sleep(1)
		img = cv2.imread(Dir)
		crop = img[140:340,220:420]
		resize_crop = cv2.resize(crop, (20,20))
		cv2.imwrite(Dir, resize_crop)

list_img = os.listdir('ball')
print 'haar1 | haar2 | dir'
for name in list_img:
	dir_img = 'ball/' + name
	img = cv2.imread(dir_img,0)
	cv2.imshow('img', img)
	cv2.waitKey(0)
	integral = cv2.integral(img)
	dis1 = haar_one(integral)
	dis2 = haar_two(integral)
	print dis1,dis2,dir_img

# for i in range(101):
# # 	img_dir = 'ball/'+str(i)+'.jpg'
# # 	img = cv2.imread(img_dir)
# 	if img.size != 400:
# 		crop(img_dir)
# 	integral = cv2.integral(img)
# 	num = haar_one(integral)
# 	print num 
# crop('ball')

# img = cv2.imread('ball.jpg',0)
# print img.shape
# print integral.shape

# num = haar_one(integral)
# print num

# cv2.waitKey(0)


