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

#subjects = ['01','02','03','04','05','06','07','08','09','10',
#			'11','12','13','14','15','16','17','18','19','20',
#			'21','22','23','24','25','26','27','28','29','30','31','32','33','34','35']
subjects = ['01']
#subjects = ['']
def acc(sta, sto, subject):

#	print str(sta)+"-"+str(sto)
#	data = Orange.data.Table("../data/"+str(subject)+'-'+str(sta)+"-"+str(sto)+".csv")
	data1 = Orange.data.Table("../data/"+str(subject)+'-1'+'-'+str(sta)+"-"+str(sto)+"_attr.csv")
	data2 = Orange.data.Table("../data/"+str(subject)+'-2'+'-'+str(sta)+"-"+str(sto)+"_attr.csv")
	data3 = Orange.data.Table("../data/"+str(subject)+'-3'+'-'+str(sta)+"-"+str(sto)+"_attr.csv")

	cv_indices1 = Orange.data.sample.SubsetIndicesCV(data1, 4)
	cv_indices2 = Orange.data.sample.SubsetIndicesCV(data2, 4)
	cv_indices3 = Orange.data.sample.SubsetIndicesCV(data3, 4)



	classes = data1.domain.classVar.values
#	print "analyze "+classes[0]+":"
	highest_precision = 0
	highest_precision_recall = 0
	highest_recall = 0
	highest_recall_precision = 0

	for fold in range(4):
		train = data1.select(cv_indices1, fold, negate = 1)
		test  = data1.select(cv_indices1, fold)
	'''    	
	for i in range(1,101):
		j=float(i)/100


		learner = svm.SVMLearner(gamma=j, verbose=False)
		results = testing.cross_validation([learner], data, folds=10)

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
	'''
	return 	format(highest_precision,'.3f'),format(highest_precision_recall,'.3f'), len(data1)
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