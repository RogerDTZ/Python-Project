import numpy as np


def read_matrix(file):
	mat = []
	for i in range(28):
		row = []
		lis = (file.readline()).split()
		for x in lis:
			if x[:1]=='1':
				row.append(1.0)
			else:
				row.append(float(int(x[2:]))/(10**(len(x)-2)))
		mat.append(row)
	file.readline()
	return mat


def transform(x):
	res = np.zeros((10, 1))
	res[x] = 1.0
	return res


def load_data(train_case_num, test_case_num):
	train_in_file = open("training.in", "r")
	train_out_file = open("training.out", "r")
	test_in_file = open("test.in", "r")
	train_data = []
	test_data = []
	for i in range(train_case_num):
		mat = read_matrix(train_in_file)
		ans = int(train_out_file.readline())
		train_in = np.reshape(mat, (28*28, 1))
		train_out = np.reshape(transform(ans), (10, 1))
		train_data.append((train_in, train_out))
		print('\r'*50, end='')
		print("Reading train data... {}/{}".format(i+1, train_case_num), end='')
	print("\nDone")
	for i in range(test_case_num):
		mat = read_matrix(test_in_file)
		test_in = np.reshape(mat, (28*28, 1))
		test_data.append(test_in)
		print('\r'*50, end='')
		print("Reading test data... {}/{}".format(i+1, test_case_num), end='')
	print("\nDone")
	return train_data, test_data
