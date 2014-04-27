import Orange

data = Orange.data.Table("power.csv")
#ma = Orange.feature.scoring.score_all(data)

bayes = Orange.classification.neural.NeuralNetworkLearner(n_mid=10, reg_fact=1, max_iter=300, rand=None)
res = Orange.evaluation.testing.cross_validation([bayes], data, folds=10)
print "Accuracy: %.2f" % Orange.evaluation.scoring.CA(res)[0]
print "AUC:      %.2f" % Orange.evaluation.scoring.AUC(res)[0]