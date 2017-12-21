import cv2
import serial
import time
# import numpy as np

# center 512

class Control_camera(object):
	"""docstring for Control_camera"""
	def __init__(self,port = 'COM3',brate = 1000000):
		self.serial = serial.Serial(port,brate) 
		# Only neck

	def low_high(self,number):
		low = 255 & number
		high = 65280 & number
		high = high >> 8
		return [low,high]

	def send(self,packet = []):
		chk = sum(packet)
		chk = chk  - 255 - 255
		chksum = (~chk) & 255
		packet.append(chksum)
		self.serial.write(packet)

	# degree <= 1023 
	def control_motor(self,id_motor,degree):
		degree_LH = self.low_high(degree)
		pact = [255,255,id_motor,7,3,30,degree_LH[0],degree_LH[1],255,1]
		self.send(pact)
		# print 'Send!'
	
	def close_port(self):
		self.serial.close()

##################################################################################

	def find_q(self,x,y,size_img):
		if x > size_img[1]/2 and y < size_img[0]/2:
			# print 'Q1'
			return 1
		elif x < size_img[1]/2 and y < size_img[0]/2:
			# print 'Q2'
			return 2
		elif x < size_img[1]/2 and y > size_img[0]/2:
			# print 'Q3'
			return 3
		elif x > size_img[1]/2 and y > size_img[0]/2:
			# print 'Q4'
			return 4

###################################################################################

# def main():
# 	ID = [3,4]
# 	control = Control_camera()
# 	control.control_motor(ID[0],390)
# 	control.control_motor(ID[1],390)
# 	time.sleep(1)
# 	control.control_motor(ID[0],610)
# 	control.control_motor(ID[1],610)
# 	time.sleep(1)
# 	control.control_motor(ID[0],511)
# 	control.control_motor(ID[1],511)
# 	control.close_port()

if __name__ == '__main__':
	# main()
	control = Control_camera()
	cv2.namedWindow('image', cv2.WINDOW_NORMAL)

	# cap = cv2.VideoCapture('video1.mp4')
	cap = cv2.VideoCapture(1)
	hc = cv2.CascadeClassifier("ball_new_14s.xml")

	# fourcc = cv2.VideoWriter_fourcc(*'XVID')
	# out = cv2.VideoWriter('video/test_with_robot.avi',fourcc, 20.0, (640,480))

	motor_val1 = 512
	motor_val2 = 512

	state_motor = 0

	while True:
		_,img = cap.read()

		if _ is True:
		
			img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)	

			footballs = hc.detectMultiScale(img_gray,1.1,6) 
			#  17s = 1.7,7  10s = 2,35 # 20s = 1.1,5 or 4 (small ball or big) 
 			
			for (x,y,w,h) in footballs:
				cv2.rectangle(img, (x, y), (x+w,y+h), (255, 0, 0), 2)
				# cv2.line(img, (0,img.shape[0]/2),(img.shape[1],img.shape[0]/2), (255,255,255),5)
				# cv2.line(img, (img.shape[1]/2,0),(img.shape[1]/2,img.shape[0]), (255,255,255),5)
				cenX = (x+(x+w))/2
				cenY = (y+(y+h))/2

				# print img.shape[1],img.shape[0],'||',cenX,cenY

				cv2.circle(img, (cenX,cenY), 3, (255,0,0))
				quard = control.find_q(cenX, cenY, img.shape[0:2])
				# if((cenX<(img.shape[1]/2)+5) and (cenX>(img.shape[1]/2)-5) or (cenY<(img.shape[0]/2)+5) and (cenY>(img.shape[0]/2)-5)):
				if(quard == 1):
					# ID 3 (-) ID 4 (-)
					# print 'Q1'
					motor_val1 -= 5
					motor_val2 -= 5
					control.control_motor(3, motor_val1)
					control.control_motor(4, motor_val2)
				elif(quard == 2):
					# ID 3 (-) ID 4 (+)
					motor_val1 -= 5
					motor_val2 += 5
					control.control_motor(3, motor_val1)
					control.control_motor(4, motor_val2)
					# print 'Q2'
				elif(quard == 3):
					# ID 3 (+) ID 4 (+)
					motor_val1 += 5
					motor_val2 += 5
					control.control_motor(3, motor_val1)
					control.control_motor(4, motor_val2)
					# print 'Q3'
				elif(quard == 4):
					# ID 3 (+) ID 4 (-)
					motor_val1 += 5
					motor_val2 -= 5
					control.control_motor(3, motor_val1)
					control.control_motor(4, motor_val2)
					# print 'Q4'
					

				# cv2.circle(img, (160,120), 5, (0,0,255))
				# print x,y,'||',x+w,y+h
				# print cenX,cenY
			out.write(img)

			cv2.imshow('image',img)
			k = cv2.waitKey(10)
			if k == ord('q'):
				break
		else:
			break

	cap.release()
	cv2.destroyAllWindows()
	control.close_port()



# should have cursor for robot vision
# 
