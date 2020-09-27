import numpy as np
import pandas as pd
import os

def remove_unwanted(files_list):
	""" Remove all the unwanted Files """
	to_delete = list()
	for file_ in files_list:
		if file_.find(".txt") != -1:
			if file_.find("_") != -1:
				pass
			else:
				to_delete.append(file_)
		else:
			to_delete.append(file_)

	for delete in to_delete:
		files_list.remove(delete)

	return files

def get_filelist(folder):
	""" Returns List of all the Files """
	folder_name = os.path.join(os.getcwd(),folder)
	print("The Folder Address is : " + str(folder_name))
	files_list = os.listdir(folder_name)
	files_list.sort()

	files = remove_unwanted(files_list)
	print("Count of Files important : " + str(len(files)))

	return files

def merge_time_data(files):
	""" Merging Time Series Data """
	ctrl_seqs = list()
	pd_seqs = list()
	count = 0
	for file_ in files:
		count += 1
		print(str(count) + " out of 306 Files done")
		if file_.find("Co") != -1:
			ctrl_seqs.append(file_)
		elif file_.find("Pt") != -1:
			pd_seqs.append(file_)
		else:
			print(file_)

	return ctrl_seqs,pd_seqs 

