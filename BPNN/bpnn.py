import random
import pickle
import numpy as np


class BPNN(object):
	def __init__(self, layer_dim, load=False):
		self.layer_num = len(layer_dim)
		self.layer_dim = layer_dim
		if not load:
			"""
			self.w = [np.random.randn(y, x) for x, y in zip(layer_dim[:-1], layer_dim[1:])]
			self.b = [np.random.randn(y, 1) for y in layer_dim[1:]]
			"""
			self.w = []
			self.b = []
			for x, y in zip(layer_dim[:-1], layer_dim[1:]):
				self.w.append(np.zeros((y, x)))
				for i in range(self.w[-1].shape[0]):
					for j in range(self.w[-1].shape[1]):
						self.w[-1][i][j] = random.random()-0.5
			for y in layer_dim[1:]:
				self.b.append(np.zeros((y, 1)))
				for i in range(self.b[-1].shape[0]):
					for j in range(self.b[-1].shape[1]):
						self.b[-1][i][j]= random.random()-0.5
		else:
			self.load_network()

	#	self.w = [np.zeros((y, x)) for x, y in zip(layer_dim[:-1], layer_dim[1:])]
	#	self.b = [np.zeros((y, 1)) for y in layer_dim[1:]]

	def train(self, train_data, iter_time, mini_size, learn_rate, test_data=None):
		print("Start training...")
		n = len(train_data)
		if test_data:
			n_test = len(test_data)
		else:
			n_test = 0
		for it in range(iter_time):
			print("Iterating time: {}/{} ".format(it+1, iter_time), end='')
			random.shuffle(train_data)
			mini_batches = [train_data[i:i+mini_size] for i in range(0, n, mini_size)]
			for mini_batch in mini_batches:
				self.trainNetwork(mini_batch, learn_rate)
			if test_data:
				error_sum, error_avg, correct = self.test(test_data)
				print("error:sum={}, avg={}, correct={}/{}({}%)".format(error_sum, error_avg, correct, n_test, 100.0*correct/n_test))
			self.save_network()

	def trainNetwork(self, data, learn_rate):
		change_w = [np.zeros(w.shape) for w in self.w]
		change_b = [np.zeros(b.shape) for b in self.b]
		for x, y in data:
			tw, tb = self.backwardPropagation(x, y)
			change_w = [w+nw for w, nw in zip(change_w, tw)]
			change_b = [b+nb for b, nb in zip(change_b, tb)]
		alpha = (1.0/len(data))*learn_rate
		self.w = [w-alpha*nw for w, nw in zip(self.w, change_w)]
		self.b = [b-alpha*nb for b, nb in zip(self.b, change_b)]

	def forwardPropagation(self, a):
		for w, b in zip(self.w, self.b):
			a = f(np.dot(w, a)+b)
		return a

	def backwardPropagation(self, x, y):
		delta_w = [np.zeros(w.shape) for w in self.w]
		delta_b = [np.zeros(b.shape) for b in self.b]
		a = x
		a_list = [a]
		z_list = [[]]
		for w, b in zip(self.w, self.b):
			z = np.dot(w, a)+b
			z_list.append(z)
			a = f(z)
			a_list.append(a)
		delta = (a_list[-1]-y)*f_d(z_list[-1])
		delta_w[-1] = np.dot(delta, a_list[-2].T)
		delta_b[-1] = delta
		for l in reversed(range(1, self.layer_num-1)):
			z = z_list[l]
			delta = np.dot(self.w[l].T, delta)*f_d(z)
			delta_w[l-1] = np.dot(delta, a_list[l-1].T)
			delta_b[l-1] = delta
		return delta_w, delta_b

	def test(self, test_data):
		error = 0
		m = len(test_data)
		for x, y in test_data:
			a = self.forwardPropagation(x)
			error += sum((u-v)*(u-v) for u, v in zip(a, y))
		result = [(np.argmax(self.forwardPropagation(x)), np.argmax(y)) for x, y in test_data]
		right = 0
		for x, y in result:
			right += int(x==y)
		return error, error/m, right

	def save_network(self):
		file = open("network.save", "wb")
		pickle.dump(self.w, file)
		pickle.dump(self.b, file)
		file.close()

	def load_network(self):
		file = open("network.save", "rb")
		self.w = pickle.load(file)
		self.b = pickle.load(file)
		file.close()

	def answerTest(self, test_data, test_out_dir):
		file = open(test_out_dir, "w")
		m = len(test_data)
		now = 0
		for x in test_data:
			a = self.forwardPropagation(x)
			predict = int(np.argmax(a))
			file.write(str(predict)+'\n')
			now += 1
			print('\r'*50, end='')
			print("Answering test... {}/{}".format(now, m), end='')
		print("\nDone")


ReLU_theta = 0.0005


def f(v):
	return (np.array(v>=0)*v)+(np.array(v<0)*v*ReLU_theta)
	#	return 1.0/(1.0+np.exp(-v))


def f_d(v):
	return (np.array(v>=0)*np.ones(v.shape))+(np.array(v<0)*np.ones(v.shape)*ReLU_theta)
	#	return f(v)*(1-f(v))
