import os
import sys
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import random

#Method to calculate Mean of data
def mean(data):
	if(len(data)==0):
		return 0
	return sum(data)/float(len(data))

#Method to calculate variance of data
def variance(data, mean):
	return sum([(x-mean)**2 for x in data])

#Method to calculate covariance
def covariance(x, u_x, y, u_y):
	covar = 0.0
	for i in xrange(len(x)):
		covar += (x[i] - u_x)*(y[i]-u_y)
	return covar

#Method to calculate coeff
def coeffecients(data):
	x = data[:,0]
	y = data[:,1]
	u_x = mean(x)
	u_y = mean(y)
	covar = covariance(x, u_x, y, u_y) / variance(x, u_x)
	b0 = u_y - covar * u_x
	return [b0, covar]

#Split dataset into train and test set
def split_data(data, split):
	train = list()
	train_size = split * len(data)
	data_copy = list(data)
	while len(train) < train_size:
		index = random.randrange(len(data_copy))
		train.append(data_copy.pop(index))
	return train, data_copy

#Method to apply linear regression model to the dataset
def linear_reg(train, test):
	pred = list()
	b0, b1 = coeffecients(train)
	for row in test:
		y_hat = b0 + b1*row[0]
		pred.append(y_hat)
	return pred

# Calculate root mean squared error
def rmse_metric(true_y, pred):
	sum_error = 0.0
	for i in range(len(true_y)):
		pred_error = pred[i] - true_y[i]
		sum_error += (pred_error ** 2)
	mean_error = sum_error / float(len(true_y))
	return sqrt(mean_error)
 
# Evaluate regression algorithm on training dataset
def eval_algo(data, algo, split, *args):
	train, test = split_data(data, split)
	test_set = list()
	for row in data:
		row_copy = list(row)
		row_copy[-1] = None
		test_set.append(row_copy)
	pred = algo(data, test_set, *args)
	true_y = [row[-1] for row in test]
	x = np.asarray(data)[:,0]
	y = np.asarray(data)[:,1]
	plt.plot(x,y, 'r^--', test_set,pred, 'b--s')
	plt.show()
	rmse = rmse_metric(true_y, pred)
	return rmse

if __name__=="__main__":
	df = pd.read_csv('data/data.csv', sep=',', header=None)
	data = df.values
	print coeffecients(data)
	split = 0.6
	rmse = eval_algo(data, linear_reg, split)
	print rmse


