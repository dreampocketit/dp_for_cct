import Orange
import random
from Orange.evaluation import testing, scoring
from Orange import evaluation

def acc(sta,sto):
	data = Orange.data.Table("../data/power"+str(sta)+'-'+str(sto)+".csv")
	classes = data.domain.classVar.values
	#ma = Orange.feature.scoring.score_all(data)
	print str(sta)+'-'+str(sto)
	print "analyze "+classes[0]+":"
	highest = 0
	for mid_node in range(5,20):
		ann = Orange.classification.neural.NeuralNetworkLearner(n_mid=mid_node, reg_fact=1, max_iter=200, rand=random, normalize=True)
		results = Orange.evaluation.testing.cross_validation([ann], data, folds=3)

#		print "analyze "+classes[0]+":"
		cm = scoring.confusion_matrices( results, class_index=0, ignore_weights=False, cutoff=0.5)[0]
#		print "TP: %i, FP: %i, FN: %s, TN: %i" % (cm.TP, cm.FP, cm.FN, cm.TN)

		if cm.TP/(cm.TP+cm.FP)>highest:
			highest = cm.TP/(cm.TP+cm.FP)

	print "precision:"+str(highest)



for sta in range(2,7):
	for sto in range(sta+1,8):
		acc(sta,sto)
