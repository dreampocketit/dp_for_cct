from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.tools.validation	 import CrossValidator,ModuleValidator
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal

alldata = None
import csv
f = open('statistic3-6.csv','rU')
f.next()
FIRST = True
for row in csv.reader(f):
	if FIRST= True:
		attr_len = len(row)-1
		ClassificationDataSet(attr_len, 1, nb_classes=2)
		FIRST = False
	alldata.addSample(row[:-1],row[-1])


tstdata, trndata = alldata.splitWithProportion( 0.2 )
alldata._convertToOneOfMany( )
trndata._convertToOneOfMany( )
tstdata._convertToOneOfMany( )
 
#We can also examine the dataset
print "Number of training patterns: ", len(trndata)
print "Input and output dimensions: ", trndata.indim, trndata.outdim
print "First sample (input, target, class):"
print trndata['input'][0], trndata['target'][0], trndata['class'][0]

fnn     = buildNetwork( trndata.indim, 5, trndata.outdim, recurrent=False )
trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01 )
trainer.trainEpochs(1000)


g=0
j=0
for out in trainer.testOnClassData(dataset=tstdata):
	if out==int(trndata['class'][g]):
		j+=1
	g+=1
print j
print float(j)/24



