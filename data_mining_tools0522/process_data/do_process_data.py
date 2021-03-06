P_START_TIME=3
P_STOP_TIME=8
#FILE_NAME = ['01-rev','02-rev','03-rev','04-rev','05-rev','06-rev',
#			'07-rev','08-rev','09-rev','10-rev','11-rev','12-rev','13-rev',
#			'14-rev','15-rev','16-rev','17-rev','18-rev','19-rev','20-rev',
#			'21-rev','22-rev','23-rev','24-rev','25-rev','26-rev','27-rev',
#			'28-rev','29-rev','30-rev','31-rev','32-rev','33-rev']
FILE_NAME = ['32-rev']


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
	return int(round(np.std(np.array(arr[sta:sto]))))

def cal_ave(sta, sto, arr):
	return int(round(np.average(np.array(arr[sta:sto]))))

def power(sta, sto, f_n):
	print f_n
	f = open('../data/'+str(f_n[12:-8])+'-'+str(sta)+'-'+str(sto)+'.csv','w')
	'''
	for i in range(sta, sto+1): 
		f.write(delta_s+'_'+str(i)+','+theta_s+'_'+str(i)+','+low_alpha_s+'_'+str(i)+','+high_alpha_s+'_'+str(i)+','+\
				low_beta_s+'_'+str(i)+','+high_beta_s+'_'+str(i)+','+low_gamma_s+'_'+str(i)+','+mid_gamma_s+'_'+str(i)+',')
	'''
	# this is for sum
	
	f.write('delta_ave,theta_ave,lowalpha_ave,highalpha_ave,lowbeta_ave,highbeta_ave,lowgamma_ave,midgamma_ave,')	
	
	
	for i in range(sta, sto+1): 
		f.write(delta_s+'_c'+str(i)+','+theta_s+'_c'+str(i)+','+low_alpha_s+'_c'+str(i)+','+high_alpha_s+'_c'+str(i)+','+\
				low_beta_s+'_c'+str(i)+','+high_beta_s+'_c'+str(i)+','+low_gamma_s+'_c'+str(i)+','+mid_gamma_s+'_c'+str(i)+',')
	
	f.write('state\n')
	

	for row in csv.DictReader(open(f_n,'rU')):
		
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

		
		######## start of normalizing by dividing ##########
		
		PLUS = 0
		DIVIDE = 1
		delta = row['delta'].split('-')
		delta = [ int(round((float(x)/DIVIDE)))+PLUS for x in delta ]
		midgamma = row['midgamma'].split('-')
		midgamma = [ int(round((float(x)/DIVIDE)))+PLUS for x in midgamma ]
		lowgamma = row['lowgamma'].split('-')
		lowgamma = [ int(round((float(x)/DIVIDE)))+PLUS for x in lowgamma ]
		theta = row['theta'].split('-')
		theta = [ int(round((float(x)/DIVIDE)))+PLUS for x in theta ]
		highalpha = row['highalpha'].split('-')
		highalpha = [ int(round((float(x)/DIVIDE)))+PLUS for x in highalpha ]
		lowalpha = row['lowalpha'].split('-')
		lowalpha = [ int(round((float(x)/DIVIDE)))+PLUS for x in lowalpha ]
		highbeta = row['highbeta'].split('-')
		highbeta = [ int(round((float(x)/DIVIDE)))+PLUS for x in highbeta ]
		lowbeta = row['lowbeta'].split('-')
		lowbeta = [ int(round((float(x)/DIVIDE)))+PLUS for x in lowbeta ]
		
		######## end of normalizing ##########

		######## start of normalizing by log ##########
		'''
		delta = row['delta'].split('-')
		delta = [ np.log(float(x)) for x in delta ]
		midgamma = row['midgamma'].split('-')
		midgamma = [ np.log(float(x)) for x in midgamma ]
		lowgamma = row['lowgamma'].split('-')
		lowgamma = [ np.log(float(x)) for x in lowgamma ]
		theta = row['theta'].split('-')
		theta = [ np.log(float(x)) for x in theta ]
		highalpha = row['highalpha'].split('-')
		highalpha = [ np.log(float(x)) for x in highalpha ]
		lowalpha = row['lowalpha'].split('-')
		lowalpha = [ np.log(float(x)) for x in lowalpha ]
		highbeta = row['highbeta'].split('-')
		highbeta = [ np.log(float(x)) for x in highbeta ]
		lowbeta = row['lowbeta'].split('-')
		lowbeta = [ np.log(float(x)) for x in lowbeta ]
		'''
		######## end of normalizing ##########
		
		tmp = ''
		for i in range(sta, sto+1):
			tmp = tmp+str(delta[i])+','+str(theta[i])+','+str(lowalpha[i])+','+str(highalpha[i])+','+\
					str(lowbeta[i])+','+str(highbeta[i])+','+str(lowgamma[i])+','+str(midgamma[i])+','

		'''
		f.write(tmp)
		'''

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
		
		base_sta = 0
		base_sto = 3
		

		delta_ave1 = cal_ave(base_sta,base_sto,delta)
		theta_ave1 = cal_ave(base_sta,base_sto,theta)
		lowalpha_ave1 = cal_ave(base_sta,base_sto,lowalpha)
		highalpha_ave1 = cal_ave(base_sta,base_sto,highalpha)
		lowbeta_ave1 = cal_ave(base_sta,base_sto,lowbeta)
		highbeta_ave1 = cal_ave(base_sta,base_sto,highbeta)
		lowgamma_ave1 = cal_ave(base_sta,base_sto,lowgamma)
		midgamma_ave1 = cal_ave(base_sta,base_sto,midgamma)


		tmp1 = ''
		tmp1 += str(delta_ave1)+','+str(theta_ave1)+','+str(lowalpha_ave1)+','+str(highalpha_ave1)+','+\
				str(lowbeta_ave1)+','+str(highbeta_ave1)+','+str(lowgamma_ave1)+','+str(midgamma_ave1)+','

		for i in range(sta, sto+1):
			tmp1 = tmp1+str(delta[i]-delta_ave1)+','+str(theta[i]-theta_ave1)+','+\
					str(lowalpha[i]-lowalpha_ave1)+','+str(highalpha[i]-highalpha_ave1)+','+\
					str(lowbeta[i]-lowbeta_ave1)+','+str(highbeta[i]-highbeta_ave1)+','+\
					str(lowgamma[i]-lowgamma_ave1)+','+str(midgamma[i]-midgamma_ave1)+','
			print delta_ave1
		
		f.write(tmp1)
		
		######## end of calculating different from initials ##########
		if str(row['state'])=='easy':
			f.write('easy\n')
		else:
			f.write('difficult\n')

#		if str(row['state'])=='easy':
#			f.write('0\n')
#		else:
#			f.write('1\n')
for f_name in FILE_NAME:
	for i in range(P_START_TIME,P_STOP_TIME-1):
		for j in range(i+1,P_STOP_TIME):
			power(i,j,'../subjects/'+str(f_name)+'.csv')
			print 'produce files:'+str(i)+'-'+str(j)
