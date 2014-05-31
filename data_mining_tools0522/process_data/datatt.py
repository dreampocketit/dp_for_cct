import csv
import numpy as np
import random
import itertools

P_START_TIME=3
P_STOP_TIME=8
base_sta = 0
base_sto = 3
DIVIDE = 1

#subjects = ['01','02','03','04','05','06','07','08','09','10',
#			'11','12','13','14','15','16','17','18','19','20',
#			'21','22','23','24','25','26','27','28','29','30','31','32','33','34']
subjects=['35']
seconds=['3-5','3-6','3-7']
filter_array = ['gamma']




FILE_NAME = []
for s in subjects:
	FILE_NAME.append(s+'-rev')


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
	global base_sto
	global base_sta
	global DIVIDE
#	print f_n
	f = open('../data/'+str(f_n[12:-8])+'-'+str(sta)+'-'+str(sto)+'.csv','w')
	'''
	for i in range(sta, sto+1): 
		f.write(delta_s+'_'+str(i)+','+theta_s+'_'+str(i)+','+low_alpha_s+'_'+str(i)+','+high_alpha_s+'_'+str(i)+','+\
				low_beta_s+'_'+str(i)+','+high_beta_s+'_'+str(i)+','+low_gamma_s+'_'+str(i)+','+mid_gamma_s+'_'+str(i)+',')
	'''
	# this is for sum
	#f.write('delta_ave,theta_ave,lowalpha_ave,highalpha_ave,lowbeta_ave,highbeta_ave,lowgamma_ave,midgamma_ave,')
	f.write('delta_base_ave,theta_base_ave,lowalpha_base_ave,highalpha_base_ave,lowbeta_base_ave,highbeta_base_ave,lowgamma_base_ave,midgamma_base_ave,')	
	
	
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
		
		delta = row['delta'].split('-')
		delta = [ int(round((float(x)/DIVIDE))) for x in delta ]
		midgamma = row['midgamma'].split('-')
		midgamma = [ int(round((float(x)/DIVIDE))) for x in midgamma ]
		lowgamma = row['lowgamma'].split('-')
		lowgamma = [ int(round((float(x)/DIVIDE))) for x in lowgamma ]
		theta = row['theta'].split('-')
		theta = [ int(round((float(x)/DIVIDE))) for x in theta ]
		highalpha = row['highalpha'].split('-')
		highalpha = [ int(round((float(x)/DIVIDE))) for x in highalpha ]
		lowalpha = row['lowalpha'].split('-')
		lowalpha = [ int(round((float(x)/DIVIDE))) for x in lowalpha ]
		highbeta = row['highbeta'].split('-')
		highbeta = [ int(round((float(x)/DIVIDE))) for x in highbeta ]
		lowbeta = row['lowbeta'].split('-')
		lowbeta = [ int(round((float(x)/DIVIDE))) for x in lowbeta ]
		
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
		
		

		delta_base_ave = cal_ave(base_sta,base_sto,delta)
		theta_base_ave = cal_ave(base_sta,base_sto,theta)
		lowalpha_base_ave = cal_ave(base_sta,base_sto,lowalpha)
		highalpha_base_ave = cal_ave(base_sta,base_sto,highalpha)
		lowbeta_base_ave = cal_ave(base_sta,base_sto,lowbeta)
		highbeta_base_ave = cal_ave(base_sta,base_sto,highbeta)
		lowgamma_base_ave = cal_ave(base_sta,base_sto,lowgamma)
		midgamma_base_ave = cal_ave(base_sta,base_sto,midgamma)


		tmp1 = ''
		tmp1 += str(delta_base_ave)+','+str(theta_base_ave)+','+str(lowalpha_base_ave)+','+str(highalpha_base_ave)+','+\
				str(lowbeta_base_ave)+','+str(highbeta_base_ave)+','+str(lowgamma_base_ave)+','+str(midgamma_base_ave)+','

		for i in range(sta, sto+1):

			tmp1 = tmp1+str(delta[i]-delta_base_ave)+','+str(theta[i]-theta_base_ave)+','+\
					str(lowalpha[i]-lowalpha_base_ave)+','+str(highalpha[i]-highalpha_base_ave)+','+\
					str(lowbeta[i]-lowbeta_base_ave)+','+str(highbeta[i]-highbeta_base_ave)+','+\
					str(lowgamma[i]-lowgamma_base_ave)+','+str(midgamma[i]-midgamma_base_ave)+','
		
		f.write(tmp1)
		
		######## end of calculating different from initials ##########
		if str(row['state'])=='easy':
			f.write('easy\n')
		else:
			f.write('difficult\n')


for f_name in FILE_NAME:
	for i in range(P_START_TIME,P_STOP_TIME-1):
		for j in range(i+1,P_STOP_TIME):
			power(i,j,'../subjects/'+str(f_name)+'.csv')
#			print 'produce files:'+str(i)+'-'+str(j)

###############################################
'''
def differential(FILE_NAME):
	tar_array=['delta_c','theta_c','lowalpha_c','highalpha_c','lowbeta_c','highbeta_c','lowgamma_c','midgamma_c']
	in_f = open("../data/"+FILE_NAME+".csv",'r')
	attrs = in_f.readline().split(',')


	matching = []
	matching_name = []
	for tar in tar_array:
		tmp_array = []
		for s in attrs:
			if tar in s:
				matching_name.append(s)
				tmp_array.append(attrs.index(s))
		matching.append(tmp_array)
	time_len = (len(matching_name)/8)-1

	final_output = []
	attr_name_array = []

	for original_attr in attrs[:-1]:
		attr_name_array.append(original_attr)


	for attr_name in tar_array:
		for i in range(time_len):
			attr_name_array.append(attr_name+'c'+str(i))
	attr_name_array.append('state')
	final_output.append(attr_name_array)

	for row in csv.reader(in_f):
		output_row = []

		for original_data in row[:-1]:
			output_row.append(original_data)

		for freq in matching:
			freq_array = []
			for loc in freq:
				freq_array.append(int(row[loc]))

			for data in np.diff(freq_array).tolist():
				output_row.append(data)
		output_row.append(row[-1])	
		final_output.append(output_row)
	
	out_f = open('../data/'+FILE_NAME+'-diff.csv','w')
	w = csv.writer(out_f) 
	w.writerows(final_output)
	out_f.close() 

for s in subjects:
	for t in seconds:
		differential(s+"-"+t)
'''
##################################################################
def sel_attr(f_name,tar_array):
	
	in_f = open("../data/"+f_name+".csv",'r')
	attrs = in_f.readline().split(',')


	matching = []
	for tar in tar_array:
		for s in attrs:
			if tar in s:
				matching.append(s)

	results = []
	for similiar_word in matching:
		results.append(attrs.index(similiar_word))

	out_f = open("../data/"+f_name+"_attr.csv","w")

	new_attrs = []
	new_data = []
	for old_attr in attrs:
		if old_attr not in matching:
			
			new_attrs.append(old_attr) 
	new_data.append(new_attrs)
	new_data[0][-1]='state'
	for row in csv.reader(in_f):
		new_row = []
		for i in range(0,len(row)):
			if i not in results:
				new_row.append(row[i])

		new_data.append(new_row)

	w = csv.writer(out_f)  
	w.writerows(new_data)  
	in_f.close()
	out_f.close() 


for s in subjects:
	for t in seconds:
		sel_attr(s+"-"+t,filter_array)