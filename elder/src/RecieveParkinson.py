import serial
import time
from matplotlib import pyplot as plt
from drawnow import *

class Parkinson(object):
	"""docstring for RecieveParkinson"""
	def __init__(self, port = 'COM3' ,brate = 19200):
		self.serial = serial.Serial(port,brate,timeout = 3)
		self.serial.flush()
		self.activatePackage = [255,255,60,255,255,0,0,0,0,0,0,0,0,0,0,0]

	def activateParkinson(self,data = []):
		self.SEND(data)

	def SEND(self,package = []):
		self.serial.write(package)

	def recieveRawPackage(self):
		DATA = []
		flagNotRecieve = 0
		if flagNotRecieve == 0:
			self.activateParkinson(self.activatePackage)
		while self.serial.inWaiting() :
			if flagNotRecieve == 0:
				flagNotRecieve = 1
			DATA.append(ord(self.serial.read()))
			# print self.serial.inWaiting()
		if flagNotRecieve:
			flagNotRecieve = 0
			return DATA

	def closePort(self):
		self.serial.close()

	def convertToRealValue(self,Data = []):
		RealData = []
		# print Data[3]
		ax = float("{0:.2f}".format((float(Data[3] | (Data[4] << 8))/100)-10))
		ay = float("{0:.2f}".format((float(Data[5] | (Data[6] << 8))/100)-10))
		az = float("{0:.2f}".format((float(Data[7] | (Data[8] << 8))/100)-10))

		gx = (Data[9] | (Data[10] << 8)) - 255
		gy = (Data[11] | (Data[12] << 8)) - 255
		gz = (Data[13] | (Data[14] << 8)) - 255
		
		RealData.append(ax)
		RealData.append(ay)
		RealData.append(az)
		RealData.append(gx)
		RealData.append(gy)
		RealData.append(gz)

		return RealData

if __name__ == '__main__':

	# p_ax = []
	# p_ay = []
	SampleData = []
	values0 = []
	values1 = []
	values2 = []
	values3 = []
	values4 = []
	values5 = []

	for i in range(100):
		values0.append(0)
		values1.append(0)
		values2.append(0)
		values3.append(0)
		values4.append(0)
		values5.append(0)

	def plotValues():
	    plt.title('Parkinson Checking')
	    plt.grid(True)
	    plt.ylabel('Values')
	    
	    plt.subplot(2,1,1)
	    plt.ylim(-2,2)
	    plt.plot(values0, 'rx-', label='Ax')
	    plt.legend(loc='upper right')
	    plt.plot(values1, 'gx-', label='Ay')
	    plt.legend(loc='upper right')
	    plt.plot(values2, 'bx-', label='Az')
	    plt.legend(loc='upper right')

	    plt.subplot(2,1,2)
	    plt.ylim(-300,300)
	    plt.plot(values3, 'rx-', label='Gx')
	    plt.legend(loc='upper right')
	    plt.plot(values4, 'gx-', label='Gy')
	    plt.legend(loc='upper right')
	    plt.plot(values5, 'bx-', label='Gz')
	    plt.legend(loc='upper right')

	    
	reciver = Parkinson(port = 'COM10')
	time.sleep(2)
	print reciver.activatePackage
	for i in range(100):
		while True:
			Data = reciver.recieveRawPackage()
			if Data is not None:
				# print Data
				SampleData = reciver.convertToRealValue(Data)
				
				values0.append(SampleData[0])
				values0.pop(0)
				values1.append(SampleData[1])
				values1.pop(0)
				values2.append(SampleData[2])
				values2.pop(0)
				
				values3.append(SampleData[3])
				values3.pop(0)
				values4.append(SampleData[4])
				values4.pop(0)
				values5.append(SampleData[5])
				values5.pop(0)

				drawnow(plotValues)
				# plt.scatter(i,SampleData[0])
				# plt.pause(0.05)
				print SampleData
				break
				
			time.sleep(0.5)
	plt.show()
	reciver.closePort()


# import numpy as np
# import matplotlib.pyplot as plt

# plt.axis([0, 10, 0, 1])
# plt.ion()

# for i in range(10):
#     y = np.random.random()
#     plt.scatter(i, y)
#     plt.pause(0.05)

# # while True:
# #     plt.pause(0.05)