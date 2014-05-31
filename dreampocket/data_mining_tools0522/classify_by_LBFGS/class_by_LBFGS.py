import Orange
import random
from Orange.evaluation import testing, scoring
from Orange import evaluation

subjects = ['01','02','03','04','05','06','07','08','09','10',
			'11','12','13','14','15','16','17','18','19','20',
			'21','22','23','24','25','26','27','28','29','30','31','32']

def acc(sta,sto,subject):
	data = Orange.data.Table("../data/"+str(subject)+'-'+str(sta)+"-"+str(sto)+".csv")
	classes = data.domain.classVar.values
	#ma = Orange.feature.scoring.score_all(data)
	highest_precision = 0
	highest_precision_recall = 0
	highest_recall = 0
	highest_recall_precision = 0
	for mid_node in range(5,20):
		ann = Orange.classification.neural.NeuralNetworkLearner(n_mid=mid_node, reg_fact=1, max_iter=200, rand=random, normalize=True)
		results = Orange.evaluation.testing.cross_validation([ann], data, folds=10)

#		print "analyze "+classes[0]+":"
		cm = scoring.confusion_matrices( results, class_index=0, ignore_weights=False, cutoff=0.5)[0]
#		print "TP: %i, FP: %i, FN: %s, TN: %i" % (cm.TP, cm.FP, cm.FN, cm.TN)

		if cm.TP+cm.FP!=0:
			if cm.TP/(cm.TP+cm.FP)>highest_precision:
				highest_precision = cm.TP/(cm.TP+cm.FP)
				highest_precision_recall = cm.TP/(cm.TP+cm.FN)

		if cm.TP+cm.FN!=0:
			if cm.TP/(cm.TP+cm.FN)>highest_recall:
				highest_recall = cm.TP/(cm.TP+cm.FN)
				highest_recall_precision = cm.TP/(cm.TP+cm.FP)

	return 	format(highest_precision,'.3f'),format(highest_precision_recall,'.3f')



fwrite = open('neural_output.csv','w')
fwrite.write('subject_id,pre5,rec5,pre6,rec6,pre7,rec7\n')
print 'subject_id\tprec\treca\tprec\treca\tprec\treca'
print '------------------------------------------------------------------'
for s in subjects:
	pre5, rec5 = acc(3,5,s)
	pre6, rec6 = acc(3,6,s)
	pre7, rec7 = acc(3,7,s)
	print 'subject:'+str(s),'\t',pre5,'\t',rec5,'\t',pre6,'\t',rec6,'\t',pre7,'\t',rec7
	fwrite.write('subject:'+str(s)+','+str(pre5)+','+str(rec5)+','+str(pre6)+','+str(rec6)+','+str(pre7)+','+str(rec7)+'\n')
