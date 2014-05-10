import Orange, cPickle
from Orange.classification import svm

data = Orange.data.Table("../power3-6.csv")
classifier = svm.LinearSVMLearner(data)

test_data = Orange.data.Table("../power2-6-test.csv")

i = 0
for row in test_data:
	if row[-1] == classifier(row):
		i+=1
	print row[-1], classifier(row)
print i
