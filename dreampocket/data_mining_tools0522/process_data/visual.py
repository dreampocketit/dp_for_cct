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

print len_e
print len_d

ave_d_delta = [0,0,0,0,0,0,0,0]
ave_d_theta = [0,0,0,0,0,0,0,0]
ave_d_lowalpha = [0,0,0,0,0,0,0,0]
ave_d_highalpha = [0,0,0,0,0,0,0,0]
ave_d_lowbeta = [0,0,0,0,0,0,0,0]
ave_d_highbeta = [0,0,0,0,0,0,0,0]
ave_d_lowgamma = [0,0,0,0,0,0,0,0]
ave_d_midgamma = [0,0,0,0,0,0,0,0]

ave_e_delta = [0,0,0,0,0,0,0,0]
ave_e_theta = [0,0,0,0,0,0,0,0]
ave_e_lowalpha = [0,0,0,0,0,0,0,0]
ave_e_highalpha = [0,0,0,0,0,0,0,0]
ave_e_lowbeta = [0,0,0,0,0,0,0,0]
ave_e_highbeta = [0,0,0,0,0,0,0,0]
ave_e_lowgamma = [0,0,0,0,0,0,0,0]
ave_e_midgamma = [0,0,0,0,0,0,0,0]



for row in d_delta:
	for i in range(8):
		ave_d_delta[i] += float(row[i])/len_d

for row in d_theta:
	for i in range(8):
		ave_d_theta[i] += float(row[i])/len_d

for row in d_lowalpha:
	for i in range(8):
		ave_d_lowalpha[i] += float(row[i])/len_d

for row in d_highalpha:
	for i in range(8):
		ave_d_highalpha[i] += float(row[i])/len_d

for row in d_lowbeta:
	for i in range(8):
		ave_d_lowbeta[i] += float(row[i])/len_d

for row in d_highbeta:
	for i in range(8):
		ave_d_highbeta[i] += float(row[i])/len_d

for row in d_lowgamma:
	for i in range(8):
		ave_d_lowgamma[i] += float(row[i])/len_d

for row in d_midgamma:
	for i in range(8):
		ave_d_midgamma[i] += float(row[i])/len_d

#################################################

for row in e_delta:
	for i in range(8):
		ave_e_delta[i] += float(row[i])/len_e

for row in e_theta:
	for i in range(8):
		ave_e_theta[i] += float(row[i])/len_e

for row in e_lowalpha:
	for i in range(8):
		ave_e_lowalpha[i] += float(row[i])/len_e

for row in e_highalpha:
	for i in range(8):
		ave_e_highalpha[i] += float(row[i])/len_e

for row in e_lowbeta:
	for i in range(8):
		ave_e_lowbeta[i] += float(row[i])/len_e

for row in e_highbeta:
	for i in range(8):
		ave_e_highbeta[i] += float(row[i])/len_e

for row in e_lowgamma:
	for i in range(8):
		ave_e_lowgamma[i] += float(row[i])/len_e

for row in e_midgamma:
	for i in range(8):
		ave_e_midgamma[i] += float(row[i])/len_e

fwrite = open('visual'+FILE_NAME[12:-4]+'.csv','w')
fwrite.write('name,first,second,third,forth,fifth,sixth,seventh,eighth\n')

fwrite.write('ave_d_delta,')
for data in ave_d_delta[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_d_delta[-1])+'\n')

fwrite.write('ave_d_theta,')
for data in ave_d_theta[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_d_theta[-1])+'\n')

fwrite.write('ave_d_lowalpha,')
for data in ave_d_lowalpha[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_d_lowalpha[-1])+'\n')

fwrite.write('ave_d_highalpha,')
for data in ave_d_highalpha[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_d_highalpha[-1])+'\n')

fwrite.write('ave_d_lowbeta,')
for data in ave_d_lowbeta[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_d_lowbeta[-1])+'\n')

fwrite.write('ave_d_highbeta,')
for data in ave_d_highbeta[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_d_highbeta[-1])+'\n')

fwrite.write('ave_d_lowgamma,')
for data in ave_d_lowgamma[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_d_lowgamma[-1])+'\n')

fwrite.write('ave_d_midgamma,')
for data in ave_d_midgamma[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_d_midgamma[-1])+'\n')

########################################

fwrite.write('ave_e_delta,')
for data in ave_e_delta[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_e_delta[-1])+'\n')

fwrite.write('ave_e_theta,')
for data in ave_e_theta[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_e_theta[-1])+'\n')

fwrite.write('ave_e_lowalpha,')
for data in ave_e_lowalpha[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_e_lowalpha[-1])+'\n')

fwrite.write('ave_e_highalpha,')
for data in ave_e_highalpha[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_e_highalpha[-1])+'\n')

fwrite.write('ave_e_lowbeta,')
for data in ave_e_lowbeta[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_e_lowbeta[-1])+'\n')

fwrite.write('ave_e_highbeta,')
for data in ave_e_highbeta[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_e_highbeta[-1])+'\n')

fwrite.write('ave_e_lowgamma,')
for data in ave_e_lowgamma[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_e_lowgamma[-1])+'\n')

fwrite.write('ave_e_midgamma,')
for data in ave_e_midgamma[:-1]:
	fwrite.write(str(data)+',')
fwrite.write(str(ave_e_midgamma[-1])+'\n')

fwrite.close()