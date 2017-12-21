import cv2
import os
import numpy as np


pathFalseNegative = "../image/hard_negative"
path_xml = '../xml_file/data_haar_121217_13.xml'

listImage = os.listdir(pathFalseNegative)
index_image = 0
cv2.namedWindow("image")

def haarDetect(img):
    
    hc = cv2.CascadeClassifier(path_xml)
    footballs = hc.detectMultiScale(img)
    
    return footballs


img = cv2.imread(pathFalseNegative+"/"+listImage[index_image],0)
while True:

    cv2.imshow("image",img)
    k = cv2.waitKey(5)
    if(k == ord('q')):
        break
    elif (k == ord('a')):
        print "swap"
        index_image += 1
        if(index_image < len(listImage)):
            img = cv2.imread(pathFalseNegative+"/"+listImage[index_image],0)
        else:
            break
    elif (k == ord('w')):
        footballs = haarDetect(img)
        for (x,y,w,h) in footballs:
            positionX = x+w/2
            positionY = y+h/2
            cv2.circle(img,(positionX,positionY),w/2,(255,255,255),3)        
cv2.destroyAllWindows()