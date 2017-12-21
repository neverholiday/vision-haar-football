import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('test.jpg')

hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

lower_green = np.array([50,100,100])
upper_green = np.array([70,255,255])

mask_blue = cv2.inRange(hsv,lower_blue,upper_blue)
mask_green = cv2.inRange(hsv,lower_green,upper_green)

cv2.namedWindow('origin', cv2.WINDOW_NORMAL)
cv2.imshow('origin',img)

cv2.namedWindow('blue', cv2.WINDOW_NORMAL)
cv2.imshow('blue',mask_blue)
cv2.namedWindow('green', cv2.WINDOW_NORMAL)
cv2.imshow('green',mask_green)

cv2.waitKey(0)
cv2.destroyAllWindows()

# plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
# plt.show()