import urllib
import cv2
import numpy as np
import os


def store_raw_images():
	# http://image-net.org/api/text/imagenet.synset.geturls?wnid=n04254680 << football
	# http://image-net.org/api/text/imagenet.synset.geturls?wnid=n08659446 << neg
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n08659446'   
    neg_image_urls = urllib.urlopen(neg_images_link).read().decode()
    pic_num = 1
    
    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.urlretrieve(i, "negs/"+str(pic_num)+".jpg")
            img = cv2.imread("negs/"+str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (200, 200))
            cv2.imwrite("negs/"+str(pic_num)+".jpg",resized_image)
            pic_num += 1
            
        except Exception as e:
            print(str(e)) 

def find_uglies():
    match = False
    for file_type in ['negs']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('Get out!!!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))

def create_pos_n_neg():
    for file_type in ['negs']:
        
        for img in os.listdir(file_type):

            if file_type == 'pos':
                line = file_type+'/'+img+' 1 0 0 50 50\n'
                with open('info.dat','a') as f:
                    f.write(line)
            elif file_type == 'negs':
                line = file_type+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)

store_raw_images()
# find_uglies()
# create_pos_n_neg()


# img = cv2.imread("3.bmp")

# # resized_image = cv2.resize(img, (50, 50))
# # cv2.imwrite("origin.jpg",resized_image)	

# hc = cv2.CascadeClassifier("cascade.xml")
# footballs = hc.detectMultiScale(img)
 
# # for (x,y,w,h) in football:
# #         font = cv2.FONT_HERSHEY_SIMPLEX
# #         cv2.putText(img,'football',(x-w,y-h), font, 0.5, (11,255,255), 2, cv2.LINE_AA)

# print footballs
# for ball in footballs:
# 	cv2.rectangle(img, (ball[0], ball[1]), (ball[0] + ball[2], ball[0] + ball[3]), (255, 0, 0), 2)

# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow('image',img)
# cv2.waitKey(0)


# cv2.destroyAllWindows()