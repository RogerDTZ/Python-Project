import data_loader
import bpnn

train_data, test_data = data_loader.load_data(40000, 0)
net = bpnn.BPNN([784, 25, 25, 10], load=True)
net.train(train_data[:30000], 10000, 20, 1, train_data[30000:])
#	net.answerTest(test_data, "test.out")
