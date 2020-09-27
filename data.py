import numpy as np
import pandas as pd
import os

class Data:

	def __init__(self, deep, gait_cycle, step = 50, features = np.arange(1,19),pk_level = True):

		'''
		:param deep:  data in the format for deep learning algorithms
		:param gait_cycle: number of gait cycle per signal
		:param step: overlap between gait signals
		:param features: signals to be loaded ( coming from sensors)
		:param pk_level: if true , y is the parkinson level according
		'''

		################################################
		self.deep = deep
		self.nb_gait_cycle = gait_cycle
		self.step = step

		self.features_to_load = features # There are 18 Features since arange starts from 1
		self.nb_features = self.features_to_load.shape[0] # 18 in our case
		################################################

		self.X_data = np.array()
		self.Y_data = np.array()
		self.nb_data_per_person = np.array([0])
		self.pk_list = pk_list
		self.ctrl_list = ctrl_list

		self.load(norm = None)

	def generate_datas(self, datas, y,data_list):
		'''
		:param datas: Data Loaded for 1 Patient Report
		:param y: Label of the Patient
		:param data_list: List Containing number of segments  per patients
		'''

		count = 0
		X_data = np.array()
		Y_data = np.array()
		nb_datas = int(datas.shape[0] - self.nb_gait_cycle) # 12119 - 100

		for start in range(0,nb_datas,self.step):
			end = start + self.nb_gait_cycle # 0 + 100
			data = datas[start:end,:]

			if X_data.size == 0:
				X_data = data
				Y_data = y
			else:
				X_data = np.dstack((X_data,data))
				Y_data = np.vstack((Y_data,y))

			count += 1

		data_list = np.append(data_list, count + data_list[-1])
		return X_data,Y_data,data_list

	def load_data(self,liste,y):
		""" Loads Data for One type """
		'''
		:param liste: List of Patients FilePaths
		:param y: Control => 0 and Parkinson => 1
		'''

		for i in range(liste):
			datas = np.loadtxt(liste[i])
			datas = datas[:,self.features_to_load] # First Coloumn Deleted

			print("Shape of Data for " + str(i) +" : " + str(datas.shape[0]))

			# Deep is 1 for now always so no IF condition #### Important (DL Model Specific)

			X_data,Y_data,self.nb_data_per_person = self.generate_datas(datas,y,self.nb_data_per_person)

			if self.X_data.size == 0:
				self.X_data = X_data
				self.Y_data = Y_data
			else:
				self.X_data = np.dstack((self.X_data,X_data))
				self.Y_data = np.vstack((self.Y_data,Y_data))

			print(X_data.shape,self.X_data.shape)

			

	def load(self, norm = 'std'):
		""" Loading the Data """
		print("Loading Training Control")
		self.load_data(self.ctrl_list,0)

		# Deep = 1
		self.last_ctrl = self.X_data.shape[2]
		self.last_ctrl_patient = len(self.nb_data_per_person)

		print("Loading Training Parkinson")

		self.X_data = self.X_data.transpose(2,0,1)

		flag = input("Enter Whether you want Normalization or Not [Y/N]")
		if flag == "Y":
			self.X_data = self.normalize_l2(self.X_data)
		else if flag == "N":
			print("No Normalization will be done")
		else:
			print("Not a Valid Input, Normalization wont be done")

		self.X_ctrl = self.X_data[:self.last_ctrl]
		self.y_ctrl =  self.y_data[:self.last_ctrl]
		self.X_park = self.X_data[self.last_ctrl:]
		self.y_park = self.y_data[self.last_ctrl:]

		print("Save Training")

		np.save("X_data", self.X_data)
		np.save("Y_data", self.y_data)
		np.save('data_person',self.nb_data_per_person)
		np.save('ctrl_list', self.ctrl_list)
		np.save('pk_list', self.pk_list)

	def normalize_l2(self,data):
		""" L2 Normalization """

		data = keras.backend.l2_normalize(data,axis = (1,2))
		data = tf.keras.backend.get_value(data)
		return data

