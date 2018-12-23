import numpy as np
import random
import pickle

learn_rate = 0.005
ReLU_theta = 0.005
n = 28
train_in = []
train_out = []
layer = 0
layer_dim = []
para = {}
record = []


def ReLU(v):
	global ReLU_theta
	return (np.array(v>=0)*v)+(np.array(v<0)*v*ReLU_theta)
	#	return 1/(1+np.exp(-v))


def ReLU_d(v):
	global ReLU_theta
	return (np.array(v>=0)*np.ones(v.shape))+(np.array(v<0)*np.ones(v.shape)*ReLU_theta)
	#	s = ReLU(v)
	#	return s*(1-s)


def forward(w, a_prev, b):
	z = np.dot(w, a_prev)+b
	return w, b, z, ReLU(z)


def forwardPropagation(x):
	global layer
	global record
	record = [(0, 0, 0, 0, 0)]
	a_prev = x
	for i in range(1, layer):
		w, b, z, a = forward(para['w'+str(i)], a_prev, para['b'+str(i)])
		record.append((np.copy(w), np.copy(a_prev), np.copy(b), np.copy(z), np.copy(a)))
		a_prev = a


def cost(out, y):
	h, m = out.shape
	res = 0.0
	correct = 0
	for j in range(m):
		max_val = -1e400
		max_who = -1
		for i in range(h):
			res += (out[i][j]-y[i][j])*(out[i][j]-y[i][j])
			if out[i][j]>max_val:
				max_val = out[i][j]
				max_who = i
		if y[max_who][j]>=0.99:
			correct += 1
	res /= m
	return res, (correct, m)


def updatePara(l, delta, a_prev, m):
	height = delta.shape[0]
	dw = np.dot(delta, a_prev.T)*(1.0/m)
	db = np.zeros((height, 1))
	for i in range(height):
		row_sum = 0
		for j in range(m):
			row_sum += delta[i][j]
		db[i][0] = row_sum
	global learn_rate
	para['w'+str(l)] -= learn_rate*dw
	para['b'+str(l)] -= learn_rate*db


def backwardPropagation(y):
	global layer
	a = record[layer-1][4]
	m = a.shape[1]
	delta = np.zeros((layer_dim[layer-1], m))
	for i in range(delta.shape[0]):
		for j in range(delta.shape[1]):
			delta[i][j] = (1.0/m)*(a[i][j]-y[i][j])
	delta = delta*ReLU_d(record[layer-1][3])
	updatePara(layer-1, delta, record[layer-1][1], m)
	for l in reversed(range(1, layer-1)):
		delta = np.dot(record[l+1][0].T, delta)*ReLU_d(record[l][3])
		updatePara(l, delta, record[l][1], m)


def initPara(in_size, hidden, out_size, need):
	global layer
	global layer_dim
	global para
	layer_dim = [in_size]
	for i in range(hidden[0]):
		layer_dim.append(hidden[1])
	layer_dim.append(out_size)
	layer = len(layer_dim)

	if need:
		para = {}
		for i in range(1, layer):
			para['w'+str(i)] = np.zeros((layer_dim[i], layer_dim[i-1]))
			para['b'+str(i)] = np.zeros((layer_dim[i], 1))
			for x in range(0, layer_dim[i]):
				for y in range(0, layer_dim[i-1]):
					para['w'+str(i)][x][y] = random.random()*1-0.5
				para['b'+str(i)][x][0] = random.random()*1-0.5
	else:
		load_network()


def readTrainData(case_num):
	print("Reading train data...")
	fin = open("training.in", "r")
	fout = open("training.out", "r")
	for t in range(case_num):
		std_in = []
		for x in range(n):
			s = fin.readline()
			lis = s.split()
			for y in range(n):
				ns = lis[y]
				if ns[0]=='1':
					v = 1.0
				else:
					v = int(ns[2:len(ns)])/(10**(len(ns)-2))
				std_in.append(v)
		fin.readline()
		answer = int(fout.readline())
		std_out = []
		for i in range(10):
			if i==answer:
				std_out.append(1.0)
			else:
				std_out.append(0.0)
		train_in.append(std_in)
		train_out.append(std_out)
		for i in range(50):
			print('\r', end='')
		print("{}/{}".format(t+1, case_num), end='')
	print("\nDone")
	return train_in, train_out


def save_network():
	global para
	save_file = open("network", "wb")
	pickle.dump(para, save_file)
	save_file.close()


def load_network():
	global para
	load_file = open("network", "rb")
	para = pickle.load(load_file)


def initNetwork(hidden, tot_case_num):
	global layer_dim
	global para
	global train_in, train_out
	initPara(n*n, hidden, 10, False)
	train_in, train_out = readTrainData(tot_case_num)


def train(tot_case_num, rep):
	print("Start training......")
	for t in range(0, rep):
		m = tot_case_num
		x = np.zeros((n*n, m), dtype=float)
		y = np.zeros((10, m), dtype=float)
		for i in range(m):
			for j in range(n*n):
				x[j][i] = train_in[i][j]
			for j in range(10):
				y[j][i] = train_out[i][j]
		forwardPropagation(x)
		now, right = cost(record[len(layer_dim)-1][4], y)
		print("Time {}/{} error={} correct={}/{} rate={}%".format(t+1, rep, now, right[0], m, 100.0*right[0]/m))
		backwardPropagation(y)
	save_network()
	print("Train done!")


def answerTest(case_num):
	global record
	print("Answering test.in...")
	fin = open("test.in", "r")
	fout = open("test.out", "w")
	for t in range(case_num):
		std_in = []
		for x in range(n):
			s = fin.readline()
			lis = s.split()
			for y in range(n):
				ns = lis[y]
				if ns[0]=='1':
					v = 1.0
				else:
					v = int(ns[2:len(ns)])/(10**(len(ns)-2))
				std_in.append(v)
		fin.readline()
		x = np.zeros((n*n, 1))
		for i in range(n*n):
			x[i][0] = std_in[i]
		forwardPropagation(x)
		a = record[len(layer_dim)-1][4]
		max_val = -1.0
		max_who = -1
		for i in range(10):
			if a[i]>max_val:
				max_val = a[i]
				max_who = i
		fout.write(str(max_who)+'\n')
		for i in range(50):
			print('\r', end='')
		print("{}/{}".format(t+1, case_num), end='')
	print("\nDone")


initNetwork((2, 25), 500)
train(500, 1000)
