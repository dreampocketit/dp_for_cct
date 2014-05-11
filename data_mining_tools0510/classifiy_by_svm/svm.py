import Orange
from Orange.classification import svm
from Orange.evaluation import testing, scoring
from Orange import data
from Orange import evaluation

from Orange.classification.svm import SVMLearner, kernels
from Orange.distance import Euclidean
from Orange.distance import Hamming


def acc(sta, sto):

	print str(sta)+"-"+str(sto)
	data = Orange.data.Table("../data/power"+str(sta)+"-"+str(sto)+".csv")

	highest = 0
	for i in range(1,101):
		j=float(i)/100
		learner = svm.SVMLearner(gamma=j, verbose=False)
		results = testing.cross_validation([learner], data, folds=10)

		if scoring.CA(results)[0]>highest:
			highest = scoring.CA(results)[0]
#		print "CA:  %.2f" % scoring.CA(results)[0]
#		print "AUC: %.2f" % scoring.AUC(results)[0]

	print "highest:"+str(highest)





for sta in range(2,7):
	for sto in range(sta+1,8):
		acc(sta,sto)