import csv
import random
import numpy as np
FILE_NAME = '../subjects/shumin.csv'

len_d = 0
len_e = 0
d_delta = []
d_theta = []
d_lowalpha = []
d_highalpha = []
d_lowbeta = []
d_highbeta = []
d_lowgamma = []
d_midgamma = []

e_delta = []
e_theta = []
e_lowalpha = []
e_highalpha = []
e_lowbeta = []
e_highbeta = []
e_lowgamma = []
e_midgamma = []


for row in csv.reader(open(FILE_NAME,'rU')):
	if row[8]=='difficult':
		d_delta.append(row[0].split('-'))
		d_theta.append(row[1].split('-'))
		d_lowalpha.append(row[2].split('-'))
		d_highalpha.append(row[3].split('-'))
		d_lowbeta.append(row[4].split('-'))
		d_highbeta.append(row[5].split('-'))
		d_lowgamma.append(row[6].split('-'))
		d_midgamma.append(row[7].split('-'))
		len_d+=1
	if row[8]=='easy':
		e_delta.append(row[0].split('-'))
		e_theta.append(row[1].split('-'))
		e_lowalpha.append(row[2].split('-'))
		e_highalpha.append(row[3].split('-'))
		e_lowbeta.append(row[4].split('-'))
		e_highbeta.append(row[5].split('-'))
		e_lowgamma.append(row[6].split('-'))
		e_midgamma.append(row[7].split('-'))
		len_e+=1


#d_delta = np.rot90(d_delta)
#d_delta = d_delta.tolist()
print d_delta