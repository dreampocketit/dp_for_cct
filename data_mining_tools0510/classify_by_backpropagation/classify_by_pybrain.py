from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.tools.validation	 import CrossValidator,ModuleValidator
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
from random import shuffle
import numpy as np
all_data = []
import csv
f = open('power2-6.csv','rU')
f.next()

f_out = open('output_pybrain1.txt','w')


for row in csv.reader(f):
	all_data.append(row)

shuffle(all_data)
print 'shuffled'

attr_len = len(all_data[0])-1

print attr_len

def split_data(seq, num):
	avg = len(seq) / float(num)
	out = []
	last = 0.0

	while last < len(seq):
		out.append(seq[int(last):int(last + avg)])
		last += avg

	return out

def get_test_data(array,num):
	tst = []
	trn = []
	for i in xrange(len(array)):
		if i!=num:
			for tmp in array[i]:
				trn.append(tmp)
		else:
			for tmp in array[i]:
				tst.append(tmp)

	return tst,trn


all_acc = []

# determined number of mid nodes
for mid_node in range(5,15):

	oneR_acc = []
	for seq in range(0,10):
		pretst,pretrn = get_test_data(split_data(all_data,10),seq)
		trndata = ClassificationDataSet(attr_len, 1, nb_classes=2)
		tstdata = ClassificationDataSet(attr_len, 1, nb_classes=2)

		for d in pretst:
			tstdata.addSample(d[:-1],d[-1])

		for d in pretrn:
			trndata.addSample(d[:-1],d[-1])


		trndata._convertToOneOfMany( )
		tstdata._convertToOneOfMany( )


		#start to make a network
		fnn = buildNetwork( trndata.indim, 10, trndata.outdim, recurrent=False )
		trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.01, verbose=True, weightdecay=0.01 )

		#start to train
		trainer.trainEpochs(200)


		#start to classify data
		progress=0
		num_of_acc=0
		for out in trainer.testOnClassData(dataset=tstdata):
			print out
			if out==int(trndata['class'][progress]):
				print out,int(trndata['class'][progress])
				num_of_acc+=1
			progress+=1
			print 'progress:'+str(progress)
		oneR_acc.append(float(num_of_acc)/progress)

	f_out.write('\n')
	f_out.write('node number:'+str(mid_node)+'\n')
	f_out.write('accuracy:'+str(np.average(np.array(oneR_acc)))+'\n')
	f_out.write('-------------------------\n')
	all_acc.append(np.average(np.array(oneR_acc)))	

print all_acc



