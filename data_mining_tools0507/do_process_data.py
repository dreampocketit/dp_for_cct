P_START_TIME=0
P_STOP_TIME=7
FILE_NAME = 'Jennifer.csv'



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
		
		PLUS = 0
		DIVIDE = 160000
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

		
		delta_ave1 = cal_ave(0,2,delta)
		theta_ave1 = cal_ave(0,2,theta)
		lowalpha_ave1 = cal_ave(0,2,lowalpha)
		highalpha_ave1 = cal_ave(0,2,highalpha)
		lowbeta_ave1 = cal_ave(0,2,lowbeta)
		highbeta_ave1 = cal_ave(0,2,highbeta)
		lowgamma_ave1 = cal_ave(0,2,lowgamma)
		midgamma_ave1 = cal_ave(0,2,midgamma)

		tmp1 = ''
		for i in range(sta, sto+1):
			tmp1 = tmp1+str(delta[i]-delta_ave1)+','+str(theta[i]-theta_ave1)+','+\
					str(lowalpha[i]-lowalpha_ave1)+','+str(highalpha[i]-highalpha_ave1)+','+\
					str(lowbeta[i]-lowbeta_ave1)+','+str(highbeta[i]-highbeta_ave1)+','+\
					str(lowgamma[i]-lowgamma_ave1)+','+str(midgamma[i]-midgamma_ave1)+','
		'''
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
