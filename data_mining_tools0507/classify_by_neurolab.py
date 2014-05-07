P_START_TIME=3
P_STOP_TIME=8
FILE_NAME = 'katrina.csv'

acc_file = open('acc.txt','w')


import csv
import numpy as np
import random
import itertools
import neurolab as nl


def acc(sta,sto,attr):

	input = []
	target = []
	f = open('power'+str(sta)+'-'+str(sto)+'.csv','rU')
	f.next()
	attr_len = 0
	for row in csv.reader(f):

		input.append(select_attr(row,attr,len(row)))
		attr_len = len(input[0])
		target.append([row[-1]])

	target  = np.array(target)

	target.reshape(len(target), 1)

	for num_of_neuro in range(8,13):
		print 
		print '-------------------------------------'
		print '**number of mid neuro:'+str(num_of_neuro)
		print 
		net = nl.net.newff([[0, 0.5]]*attr_len, [num_of_neuro,1])

	
		input = np.array(input)
		tmp_acc = ten_cross(input, target, net)

		if int(tmp_acc)>0.5:
			print 'tmp_acc>0.5'
			acc_file.write('----------------------------\n')
			acc_file.write('attr:'+str(attr)+'\n')
			acc_file.write('num_of_neuro:'+str(num_of_neuro)+'\n')
			acc_file.write('sta:'+str(sta)+' sto:'+str(sto)+'\n')
			acc_file.write('accuracy rate:  '+str()+'\n')




def select_attr(arr, select, len_of_array):
	tmp_result = []
	for name in select:
		for shift in range(0,(len_of_array/8)):
			tmp_result.append(arr[name+shift*8])

#	print tmp_result
	return tmp_result


def ten_cross(input, target, net):

	part_len = int(len(input)/10)
	pred_result = []

	net.trainf = nl.train.train_gd
	
	now = 0
	for progress in range(0,10):
		print 'start at:'+str(progress*part_len)+' and end at:'+str((progress+1)*part_len)

		train_set = None
		train_tar = None
		if progress == 0:
			train_set = input[(progress+1)*part_len:-1]
			train_tar = target[(progress+1)*part_len:-1]
		elif progress == 9:
			train_set = input[0:progress*part_len]
			train_tar = target[0:(progress)*part_len]
		else:
			train_set = np.concatenate((input[0:progress*part_len],input[(progress+1)*part_len:-1]))
			train_tar = np.concatenate((target[0:progress*part_len],target[(progress+1)*part_len:-1]))

#		print 'train_set'
#		print train_set


		error = net.train(train_set, train_tar ,show=10000,lr=0.1, epochs=100, goal=0.1)
		pred = net.sim(input[progress*part_len:(progress+1)*part_len])

#		print input[progress*part_len:(progress+1)*part_len]

		acc_num = 0
		
#		print 'target,pred,original'
		for i in pred:
			
			if i[0]>0.999999:				
				if int(target[now][0])==1:
					acc_num+=1
#				print '  '+str(target[now][0])+'     '+str(1)+'  '+str(i[0])

			else:
				if int(target[now][0])==0:
					acc_num+=1
#				print '  '+str(target[now][0])+'     '+str(0)+'  '+str(i[0])

			now+=1
						
		pred_result.append(float(acc_num)/len(pred))
		print 'accuracy of this round:'+str(float(acc_num)/len(pred))
	print 
	print '**accuracy rate:'+str(np.average(np.array(pred_result)))
	print 

	return np.average(np.array(pred_result))


for attr in [[0,1],[2,3,4,5],[0,1,2,3,4,5],[6,7],[2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0],[1],[2],[3],[4],[5],[6],[7]]:
	for i in range(P_START_TIME,P_STOP_TIME-1):
		for j in range(i+1,P_STOP_TIME):
			print attr
			print 'start time:'+str(i)+'  stop time:'+str(j)
			acc(i,j,attr)


acc_file.close()
