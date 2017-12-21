import sys
import cv2
import numpy as np

cv2.namedWindow('digitize',cv2.WINDOW_NORMAL)

if(len(sys.argv) == 2):
    # default
    directory_image = sys.argv[1]
else:
    directory_image = "image_test/1.jpg"

img = cv2.imread(directory_image,0)

model = cv2.HOGDescriptor()

model.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

(rects,weight) = model.detectMultiScale(img, winStride=(4, 4),
		padding=(8, 8), scale=1.05)

print rects
print weight

for (x, y, w, h) in rects:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow('digitize',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

