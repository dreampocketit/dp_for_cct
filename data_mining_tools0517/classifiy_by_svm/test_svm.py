import Orange
from Orange.classification import svm
from Orange.evaluation import testing, scoring
from Orange import data
from Orange import evaluation

from Orange.classification.svm import SVMLearner, kernels
from Orange.distance import Euclidean
from Orange.distance import Hamming
import orngStat
import time


def acc(sta, sto):

	print str(sta)+"-"+str(sto)
	data = Orange.data.Table("../data/power"+str(sta)+"-"+str(sto)+".csv")
	classes = data.domain.classVar.values
	print "analyze "+classes[1]+":"
	highest_precision = 0
	highest_precision_recall = 0
	highest_recall = 0
	highest_recall_precision = 0
	for i in range(1,101):
		j=float(i)/100

#		svm_l = Orange.classification.svm.SVMLearner(kernel_type=Orange.classification.svm.kernels.Linear)
#		rfe = Orange.classification.svm.RFE(learner=svm_l)
#		data_with_subset_of_features = rfe(data, 10)
#		print data_with_subset_of_features.domain
		
#		n = 10
#		ma = Orange.feature.scoring.score_all(data)
#		best = Orange.feature.selection.top_rated(ma, n)
#		print 'Best %d features:' % n
#		for s in best:
#			print s

		learner = svm.SVMLearner(gamma=j, verbose=False)
#		learner = Orange.feature.selection.FilteredLearner(learner, filter=Orange.feature.selection.FilterBestN(n=10), name='filtered')
		results = testing.cross_validation([learner], data, folds=10)
#		print scoring.CA(results)
#		print "analyze "+classes[0]+":"
		cm = scoring.confusion_matrices( results, class_index=1, ignore_weights=False, cutoff=0.5)[0]
#		print "TP: %i, FP: %i, FN: %s, TN: %i" % (cm.TP, cm.FP, cm.FN, cm.TN)
		
		if cm.TP+cm.FP!=0:
			if cm.TP/(cm.TP+cm.FP)>highest_precision:
				highest_precision = cm.TP/(cm.TP+cm.FP)
				highest_precision_recall = cm.TP/(cm.TP+cm.FN)

		if cm.TP+cm.FN!=0:
			if cm.TP/(cm.TP+cm.FN)>highest_recall:
				highest_recall = cm.TP/(cm.TP+cm.FN)
				highest_recall_precision = cm.TP/(cm.TP+cm.FP)

#		time.sleep(0.1)
		
	print "highest precision:"+str(highest_precision)+ "  recall:   "+str(highest_precision_recall)
	print "highest recall   :"+str(highest_recall)+ "  precision:"+str(highest_recall_precision)
	print 
	print 





for sta in range(2,7):
	for sto in range(sta+1,8):
		acc(sta,sto)