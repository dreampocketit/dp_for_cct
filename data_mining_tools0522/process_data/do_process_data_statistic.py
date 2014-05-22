P_START_TIME=2
P_STOP_TIME=8
FILE_NAME = '../subjects/katrina.csv'



import csv
import numpy as np
import random
import itertools
import math


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

def cal_max(sta, sto, arr):
	return int(np.max(np.array(arr[sta:sto])))

def cal_min(sta, sto, arr):
	return int(np.min(np.array(arr[sta:sto])))

def power(sta, sto):
	
	f = open('../data/statistic'+str(sta)+'-'+str(sto)+'.csv','w')
	
	#f.write('delta_ave,theta_ave,lowalpha_ave,highalpha_ave,lowbeta_ave,highbeta_ave,lowgamma_ave,midgamma_ave,')
	f.write('delta_max,theta_max,lowalpha_max,highalpha_max,lowbeta_max,highbeta_max,lowgamma_max,midgamma_max,')
	f.write('delta_min,theta_min,lowalpha_min,highalpha_min,lowbeta_min,highbeta_min,lowgamma_min,midgamma_min,')	
	
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
		delta = row['delta'].split('-')
		delta = [ math.log1p(float(x)) for x in delta ]
		midgamma = row['midgamma'].split('-')
		midgamma = [ math.log1p(float(x)) for x in midgamma ]
		lowgamma = row['lowgamma'].split('-')
		lowgamma = [ math.log1p(float(x)) for x in lowgamma ]
		theta = row['theta'].split('-')
		theta = [ math.log1p(float(x)) for x in theta ]
		highalpha = row['highalpha'].split('-')
		highalpha = [ math.log1p(float(x)) for x in highalpha ]
		lowalpha = row['lowalpha'].split('-')
		lowalpha = [ math.log1p(float(x)) for x in lowalpha ]
		highbeta = row['highbeta'].split('-')
		highbeta = [ math.log1p(float(x)) for x in highbeta ]
		lowbeta = row['lowbeta'].split('-')
		lowbeta = [ math.log1p(float(x)) for x in lowbeta ]
		'''
		######## end of normalizing ##########
		

		######## start of calculating average of all ##########
		
		delta_ave = cal_ave(sta,sto+1,delta)
		theta_ave = cal_ave(sta,sto+1,theta)
		lowalpha_ave = cal_ave(sta,sto+1,lowalpha)
		highalpha_ave = cal_ave(sta,sto+1,highalpha)
		lowbeta_ave = cal_ave(sta,sto+1,lowbeta)
		highbeta_ave = cal_ave(sta,sto+1,highbeta)
		lowgamma_ave = cal_ave(sta,sto+1,lowgamma)
		midgamma_ave = cal_ave(sta,sto+1,midgamma)

		
	#	f.write(str(delta_ave)+',')
	#	f.write(str(theta_ave)+',')
	#	f.write(str(lowalpha_ave)+',')
	#	f.write(str(highalpha_ave)+',')
	#	f.write(str(lowbeta_ave)+',')
	#	f.write(str(highbeta_ave)+',')
	#	f.write(str(lowgamma_ave)+',')
	#	f.write(str(midgamma_ave)+',')
		
		######## end of calculating average of all##########

		######## start of calculating max of all ##########
		delta_max = cal_max(sta,sto+1,delta)
		theta_max = cal_max(sta,sto+1,theta)
		lowalpha_max = cal_max(sta,sto+1,lowalpha)
		highalpha_max = cal_max(sta,sto+1,highalpha)
		lowbeta_max = cal_max(sta,sto+1,lowbeta)
		highbeta_max = cal_max(sta,sto+1,highbeta)
		lowgamma_max = cal_max(sta,sto+1,lowgamma)
		midgamma_max = cal_max(sta,sto+1,midgamma)

		
		f.write(str(delta_max)+',')
		f.write(str(theta_max)+',')
		f.write(str(lowalpha_max)+',')
		f.write(str(highalpha_max)+',')
		f.write(str(lowbeta_max)+',')
		f.write(str(highbeta_max)+',')
		f.write(str(lowgamma_max)+',')
		f.write(str(midgamma_max)+',')


		######## end of calculating max of all##########

		######## start of calculating min of all ##########

		delta_min = cal_min(sta,sto+1,delta)
		theta_min = cal_min(sta,sto+1,theta)
		lowalpha_min = cal_min(sta,sto+1,lowalpha)
		highalpha_min = cal_min(sta,sto+1,highalpha)
		lowbeta_min = cal_min(sta,sto+1,lowbeta)
		highbeta_min = cal_min(sta,sto+1,highbeta)
		lowgamma_min = cal_min(sta,sto+1,lowgamma)
		midgamma_min = cal_min(sta,sto+1,midgamma)

		
		f.write(str(delta_min)+',')
		f.write(str(theta_min)+',')
		f.write(str(lowalpha_min)+',')
		f.write(str(highalpha_min)+',')
		f.write(str(lowbeta_min)+',')
		f.write(str(highbeta_min)+',')
		f.write(str(lowgamma_min)+',')
		f.write(str(midgamma_min)+',')

		######## end of calculating min of all##########
		
		if str(row['state'])=='easy':
			f.write('easy\n')
		else:
			f.write('difficult\n')

for i in range(P_START_TIME,P_STOP_TIME-1):
	for j in range(i+1,P_STOP_TIME):
		power(i,j)
		print 'produce files:'+str(i)+'-'+str(j)