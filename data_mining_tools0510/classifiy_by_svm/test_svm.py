import Orange
from Orange.classification import svm
from Orange.evaluation import testing, scoring
from Orange import data
from Orange import evaluation

from Orange.classification.svm import SVMLearner, kernels
from Orange.distance import Euclidean
from Orange.distance import Hamming
import orngStat


def acc(sta, sto):

	print str(sta)+"-"+str(sto)
	data = Orange.data.Table("../data/power"+str(sta)+"-"+str(sto)+".csv")
	classes = data.domain.classVar.values
	print "analyze "+classes[0]+":"
	highest = 0
	for i in range(1,101):
		j=float(i)/100
		learner = svm.SVMLearner(gamma=j, verbose=False)
		results = testing.cross_validation([learner], data, folds=10)
#		print scoring.CA(results)
#		print "analyze "+classes[0]+":"
		cm = scoring.confusion_matrices( results, class_index=0, ignore_weights=False, cutoff=0.5)[0]
#		print "TP: %i, FP: %i, FN: %s, TN: %i" % (cm.TP, cm.FP, cm.FN, cm.TN)
		

#		if cm.TP/(cm.TP+cm.FP)>highest:
#			highest = cm.TP/(cm.TP+cm.FP)

	print "precision:"+str(highest)




for sta in range(2,7):
	for sto in range(sta+1,8):
		acc(sta,sto)

#acc(2,6)