import Orange
from Orange.classification import svm
from Orange.evaluation import testing, scoring
from Orange import data
from Orange import evaluation

from Orange.classification.svm import SVMLearner, kernels
from Orange.distance import Euclidean
from Orange.distance import Hamming


def acc(name):


	data = Orange.data.Table("../data/"+str(name)+".csv")
	for row in data:
		print data

	highest = 0
	for i in range(1,101):
		j=float(i)/100
		learner = svm.SVMLearner(gamma=j, verbose=True)
		results = testing.cross_validation([learner], data, folds=10)

		if scoring.CA(results)[0]>highest:
			highest = scoring.CA(results)[0]
#		print "CA:  %.2f" % scoring.CA(results)[0]
#		print "AUC: %.2f" % scoring.AUC(results)[0]

	print "highest:"+str(highest)





acc('01-3-5-diff')