P_START_TIME=4
P_STOP_TIME=8
FILE_NAME = 'katrina.csv'



import csv
import numpy as np
import random
import itertools


delta_s = 'delta'
theta_s = 'theta'
low_alpha_s = 'lowalpha'
high_alpha_s = 'highalpha'
low_beta_s = 'lowbeta'
high_beta_s = 'highbeta'
low_gamma_s = 'lowgamma'
mid_gamma_s = 'midgamma'

delta = []
theta = []
lowalpha = []
highalpha = []
lowbeta = []
highbeta = []
lowgamma = []
midgamma = []

def cal_std(sta, sto, arr):
	return int(np.std(np.array(arr[sta:sto])))

def cal_ave(sta, sto, arr):
	return int(np.average(np.array(arr[sta:sto])))

def power(sta, sto):
	
	f = open('power'+str(sta)+'-'+str(sto)+'.csv','w')
	
	for i in range(sta, sto+1): 
		f.write(delta_s+'_'+str(i)+','+theta_s+'_'+str(i)+','+low_alpha_s+'_'+str(i)+','+high_alpha_s+'_'+str(i)+','+\
				low_beta_s+'_'+str(i)+','+high_beta_s+'_'+str(i)+','+low_gamma_s+'_'+str(i)+','+mid_gamma_s+'_'+str(i)+',')
	
	# this is for sum
	'''
	f.write('delta_ave,theta_ave,lowalpha_ave,highalpha_ave,lowbeta_ave,highbeta_ave,lowgamma_ave,midgamma_ave,')	
	'''
	'''
	for i in range(sta, sto+1): 
		f.write(delta_s+'_c'+str(i)+','+theta_s+'_c'+str(i)+','+low_alpha_s+'_c'+str(i)+','+high_alpha_s+'_c'+str(i)+','+\
				low_beta_s+'_c'+str(i)+','+high_beta_s+'_c'+str(i)+','+low_gamma_s+'_c'+str(i)+','+mid_gamma_s+'_c'+str(i)+',')
	'''
	f.write('state\n')


	for row in csv.DictReader(open(FILE_NAME,'rU')):
		
		delta = row['delta'].split('-')
		delta = [ int(x) for x in delta ]
		midgamma = row['midgamma'].split('-')
		midgamma = [ int(x) for x in midgamma ]
		lowgamma = row['lowgamma'].split('-')
		lowgamma = [ int(x) for x in lowgamma ]
		theta = row['theta'].split('-')
		theta = [ int(x) for x in theta ]
		highalpha = row['highalpha'].split('-')
		highalpha = [ int(x) for x in highalpha ]
		lowalpha = row['lowalpha'].split('-')
		lowalpha = [ int(x) for x in lowalpha ]
		highbeta = row['highbeta'].split('-')
		highbeta = [ int(x) for x in highbeta ]
		lowbeta = row['lowbeta'].split('-')
		lowbeta = [ int(x) for x in lowbeta ]

		
		######## start of normalizing ##########
		'''
		PLUS = 0
		DIVIDE = 1600000
		delta = row['delta'].split('-')
		delta = [ int((float(x)/DIVIDE))+PLUS for x in delta ]
		midgamma = row['midgamma'].split('-')
		midgamma = [ int((float(x)/DIVIDE))+PLUS for x in midgamma ]
		lowgamma = row['lowgamma'].split('-')
		lowgamma = [ int((float(x)/DIVIDE))+PLUS for x in lowgamma ]
		theta = row['theta'].split('-')
		theta = [ int((float(x)/DIVIDE))+PLUS for x in theta ]
		highalpha = row['highalpha'].split('-')
		highalpha = [ int((float(x)/DIVIDE))+PLUS for x in highalpha ]
		lowalpha = row['lowalpha'].split('-')
		lowalpha = [ int((float(x)/DIVIDE))+PLUS for x in lowalpha ]
		highbeta = row['highbeta'].split('-')
		highbeta = [ int((float(x)/DIVIDE))+PLUS for x in highbeta ]
		lowbeta = row['lowbeta'].split('-')
		lowbeta = [ int((float(x)/DIVIDE))+PLUS for x in lowbeta ]
		'''
		######## end of normalizing ##########
		
		tmp = ''
		for i in range(sta, sto+1):
			tmp = tmp+str(delta[i])+','+str(theta[i])+','+str(lowalpha[i])+','+str(highalpha[i])+','+\
					str(lowbeta[i])+','+str(highbeta[i])+','+str(lowgamma[i])+','+str(midgamma[i])+','
		
		f.write(tmp)
		

		######## start of calculating average of all ##########
		'''
		delta_ave = cal_ave(sta,sto+1,delta)
		theta_ave = cal_ave(sta,sto+1,theta)
		lowalpha_ave = cal_ave(sta,sto+1,lowalpha)
		highalpha_ave = cal_ave(sta,sto+1,highalpha)
		lowbeta_ave = cal_ave(sta,sto+1,lowbeta)
		highbeta_ave = cal_ave(sta,sto+1,highbeta)
		lowgamma_ave = cal_ave(sta,sto+1,lowgamma)
		midgamma_ave = cal_ave(sta,sto+1,midgamma)

		
		f.write(str(delta_ave)+',')
		f.write(str(theta_ave)+',')
		f.write(str(lowalpha_ave)+',')
		f.write(str(highalpha_ave)+',')
		f.write(str(lowbeta_ave)+',')
		f.write(str(highbeta_ave)+',')
		f.write(str(lowgamma_ave)+',')
		f.write(str(midgamma_ave)+',')
		'''
		######## end of calculating average of all##########


		######## start of calculating different from initials ##########

		'''
		delta_ave1 = cal_ave(0,1,delta)
		theta_ave1 = cal_ave(0,1,theta)
		lowalpha_ave1 = cal_ave(0,1,lowalpha)
		highalpha_ave1 = cal_ave(0,1,highalpha)
		lowbeta_ave1 = cal_ave(0,1,lowbeta)
		highbeta_ave1 = cal_ave(0,1,highbeta)
		lowgamma_ave1 = cal_ave(0,1,lowgamma)
		midgamma_ave1 = cal_ave(0,1,midgamma)

		tmp1 = ''
		for i in range(sta, sto+1):
			tmp1 = tmp1+str(delta[i]-delta_ave1)+','+str(theta[i]-theta_ave1)+','+\
					str(lowalpha[i]-lowalpha_ave1)+','+str(highalpha[i]-highalpha_ave1)+','+\
					str(lowbeta[i]-lowbeta_ave1)+','+str(highbeta[i]-highbeta_ave1)+','+\
					str(lowgamma[i]-lowgamma_ave1)+','+str(midgamma[i]-midgamma_ave1)+','

		f.write(tmp1)
		'''
		######## end of calculating different from initials ##########
		if str(row['state'])=='easy':
			f.write(str(0)+'\n')
		else:
			f.write(str(1)+'\n')

for i in range(P_START_TIME,P_STOP_TIME-1):
	for j in range(i+1,P_STOP_TIME):
		power(i,j)
		print 'produce files:'+str(i)+'-'+str(j)

print 
print 'now we are start to calculating:'
print 

############# start of calculating data ############

import neurolab as nl
import pylab as pl


def acc(sta,sto):

	input = []
	target = []
	f = open('power'+str(sta)+'-'+str(sto)+'.csv','rU')
	f.next()
	attr_len = 0
	for row in csv.reader(f):

		input.append(select_attr(row,[7],len(row)))
		attr_len = len(input[0])
		target.append([row[-1]])

	target  = np.array(target)

	target.reshape(len(target), 1)
	net = nl.net.newff([[0, 0.5]]*attr_len, [8,1])

	
	input = np.array(input)
	ten_cross(input, target, net)
#	net.trainf = nl.train.train_gd
#	error = net.train(input, target,show=10000,lr=0.1, epochs=1000, goal=0.1)
	
#	print 'significant error:'+str(min(error))


	'''
	pl.plot(error)
	pl.xlabel('Epoch number')
	pl.ylabel('Train error')
	pl.grid()
	pl.show()
	'''
#	for a in net.sim(input):
#		if a[0]>0.9999:
#			print str(1)
#		else:
#			print str(0)

#	f = open('eva'+str(sta)+'-'+str(sto)+'.csv','w')
#	for a in net.sim(input):
#		f.write(str(a[0])+'\n')
#	f.close()
#

def select_attr(arr, select, len_of_array):
	tmp_result = []
	for name in select:
		for shift in range(0,(len_of_array/8)):
			tmp_result.append(arr[name+shift*8])

	print tmp_result
	return tmp_result


def ten_cross(input, target, net):

	part_len = int(len(input)/10)
	pred_result = []

	net.trainf = nl.train.train_gd
	
	now = 0
	for progress in range(0,10):
#		print progress*part_len
#		print (progress+1)*part_len
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

#		print ":"+str(target[progress*part_len])
#		print ":"+str(target[now])

		error = net.train(train_set, train_tar ,show=10000,lr=0.1, epochs=100, goal=0.1)
		pred = net.sim(input[progress*part_len:(progress+1)*part_len])

		acc_num = 0
		
#		print pred

		for i in pred:
#			print now
			if i[0]>0.999:
				
				if int(target[now][0])==1:
					acc_num+=1
#					print 'right'

			else:
				if int(target[now][0])==0:
					acc_num+=1
#					print 'right'
					
			now+=1
						
		pred_result.append(float(acc_num)/len(pred))

	print np.average(np.array(pred_result))

#select_attr([0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7],[1,4,3],len([0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7]))

'''
for i in range(P_START_TIME,P_STOP_TIME-1):
	for j in range(i+1,P_STOP_TIME):
		print 'start time:'+str(i)+'  stop time:'+str(j)
		acc(i,j)
'''

acc(3,6)

