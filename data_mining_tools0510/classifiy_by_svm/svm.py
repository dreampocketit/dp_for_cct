import Orange
from Orange.classification import svm
from Orange.evaluation import testing, scoring
from Orange import data
from Orange import evaluation

from Orange.classification.svm import SVMLearner, kernels
from Orange.distance import Euclidean
from Orange.distance import Hamming

data = Orange.data.Table("../data/power2-6.csv")

for i in range(1,11):
	j=float(i)/100
	print j
	learner = svm.SVMLearner(gamma=j, verbose=False)
	results = testing.cross_validation([learner], data, folds=10)

	print "CA:  %.2f" % scoring.CA(results)[0]
	print "AUC: %.2f" % scoring.AUC(results)[0]