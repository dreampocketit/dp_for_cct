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

subjects = ['01','02','03','04','05','06','07','08','09','10',
			'11','12','13','14','15','16','17','18','19','20',
			'21','22','23','24','25','26','27','28','29','30','31','32','33']
#subjects = ['33']
#subjects = ['']
def acc(sta, sto, subject):

#	print str(sta)+"-"+str(sto)
#	data = Orange.data.Table("../data/"+str(subject)+'-'+str(sta)+"-"+str(sto)+".csv")
	data = Orange.data.Table("../data/"+str(subject)+'-'+str(sta)+"-"+str(sto)+"_attr.csv")
	classes = data.domain.classVar.values
#	print "analyze "+classes[0]+":"
	highest_precision = 0
	highest_precision_recall = 0
	highest_recall = 0
	highest_recall_precision = 0
	for i in range(1,101):
#	for i in range(1,2):
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
#		learner = svm.SVMLearner(kernel_type=Orange.classification.svm.kernels.Linear ,verbose=False)
#		learner = Orange.feature.selection.FilteredLearner(learner, filter=Orange.feature.selection.FilterBestN(n=10), name='filtered')
		results = testing.cross_validation([learner], data, folds=10)
#		print scoring.CA(results)
#		print "analyze "+classes[0]+":"
		cm = scoring.confusion_matrices( results, class_index=0, ignore_weights=False, cutoff=0.52)[0]
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

	return 	format(highest_precision,'.3f'),format(highest_precision_recall,'.3f'), len(data)
#	return str(format(highest_precision,'.2f'))+ "\t"+str(format(highest_precision_recall,'.2f'))
#	print "highest recall   :"+str(highest_recall)+ "  precision:"+str(highest_recall_precision)
#	print 
#	print 
fwrite = open('svm_output.csv','w')
fwrite.write('subject_id,pre5,rec5,pre6,rec6,pre7,rec7\n')
print 'subject_id\tprec\treca\tprec\treca\tprec\treca'
print '------------------------------------------------------------------'
for s in subjects:
	pre5, rec5, length = acc(3,5,s)
	pre6, rec6, length = acc(3,6,s)
	pre7, rec7, length = acc(3,7,s)

	print 'subject:'+str(s),'\t',pre5,'\t',rec5,'\t',pre6,'\t',rec6,'\t',pre7,'\t',rec7,'\t',length
	fwrite.write('subject:'+str(s)+','+str(pre5)+','+str(rec5)+','+str(pre6)+','+str(rec6)+','+str(pre7)+','+str(rec7)+'\n')
#for sta in range(3,7):
#	for sto in range(sta+2,8):
#		acc(sta,sto)