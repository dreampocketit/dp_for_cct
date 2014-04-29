import Orange

def acc(sta,sto):
	data = Orange.data.Table("power"+str(sta)+'-'+str(sto)+".csv")
	#ma = Orange.feature.scoring.score_all(data)

	ann = Orange.classification.neural.NeuralNetworkLearner(n_mid=10, reg_fact=1, max_iter=100, rand=None, normalize=True)
	res = Orange.evaluation.testing.cross_validation([ann], data, folds=10)
	print str(sta)+'-'+str(sto)+':'
	print "Accuracy: %.2f" % Orange.evaluation.scoring.CA(res)[0]
	print "AUC:      %.2f" % Orange.evaluation.scoring.AUC(res)[0]

for sta in range(2,6):
	for sto in range(sta+1,7):
		acc(sta,sto)