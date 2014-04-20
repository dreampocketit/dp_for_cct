import csv
import numpy as np


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
	f.write('delta_ave,theta_ave,lowalpha_ave,highalpha_ave,lowbeta_ave,highbeta_ave,lowgamma_ave,midgamma_ave,')		
	f.write('state\n')


	for row in csv.DictReader(open('output.csv','rU')):
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



		tmp = ''
		for i in range(sta, sto+1):
			tmp = tmp+str(delta[i])+','+str(theta[i])+','+str(lowalpha[i])+','+str(highalpha[i])+','+\
					str(lowbeta[i])+','+str(highbeta[i])+','+str(lowgamma[i])+','+str(midgamma[i])+','

		f.write(tmp)
		print delta
		print np.sum(np.array(delta)[1:6])
		print np.sum(np.array(theta)[1:6])
		f.write(str(cal_ave(sta,sto+1,delta))+',')
		f.write(str(cal_ave(sta,sto+1,theta))+',')
		f.write(str(cal_ave(sta,sto+1,lowalpha))+',')
		f.write(str(cal_ave(sta,sto+1,highalpha))+',')
		f.write(str(cal_ave(sta,sto+1,lowbeta))+',')
		f.write(str(cal_ave(sta,sto+1,highbeta))+',')
		f.write(str(cal_ave(sta,sto+1,lowgamma))+',')
		f.write(str(cal_ave(sta,sto+1,midgamma))+',')


#		f.write(str(cal_std(sta,sto+1,delta))+',')
#		f.write(str(cal_std(sta,sto+1,midgamma))+',')
#		f.write(str(cal_std(sta,sto+1,lowgamma))+',')
#		f.write(str(cal_std(sta,sto+1,theta))+',')
#		f.write(str(cal_std(sta,sto+1,highalpha))+',')
#		f.write(str(cal_std(sta,sto+1,lowalpha))+',')
#		f.write(str(cal_std(sta,sto+1,highbeta))+',')
#		f.write(str(cal_std(sta,sto+1,lowbeta))+',')
		f.write(str(row['state'])+'\n')


power(2,5)




	