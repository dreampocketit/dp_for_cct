import csv
import numpy as np
import neurolab as nl
def acc(sta=2,sto=3):

	input = []
	target = []
	f = open('power'+str(sta)+'-'+str(sto)+'.csv','rU')
	f.next()
	attr_len = 0
	for row in csv.reader(f):
		input.append(row[:-1])
		attr_len = len(row[:-1])
		target.append([row[-1]])

	input = np.array(input)
	target  = np.array(target)

	target.reshape(len(target), 1)
	net = nl.net.newff([[0, 0.5]]*attr_len, [5,1])
	net.trainf = nl.train.train_gd
	error = net.train(input, target,show=10000,lr=0.1, epochs=1000, goal=0.1)
	
	print 'significant error:'+str(min(error))

	print '-------------------------------'

	'''
	pl.plot(error)
	pl.xlabel('Epoch number')
	pl.ylabel('Train error')
	pl.grid()
	pl.show()
	'''
	print net.sim(input)
acc(2,3)