import csv
import time
import random
import numpy as np
FILE_NAME = '../subjects/01.csv'

difficult = []
easy = []
attr = ''


first = True
for row in csv.reader(open(FILE_NAME,'rU')):

	if first:
		for name in row[:-1]:
			attr += name+','

		attr+=row[-1]+'\n'
		first = False
		continue

	if row[-2]=='difficult':
		difficult.append(row)
	else:
		easy.append(row)

def downsa(num,easy,difficult):

	final = []
	global attr
	
	new_easy = easy[:]
	new_difficult = difficult[:]

	if len(new_easy)>len(new_difficult):
		random.shuffle(new_easy)
		for i in range(len(new_difficult)):
			final.append(new_easy[i])
			final.append(new_difficult[i])

	else:
		random.shuffle(new_difficult)
		for i in range(len(new_easy)):
			final.append(new_easy[i])
			final.append(new_difficult[i])

	fwrite = open(FILE_NAME[0:-4]+'-rev'+str(num)+FILE_NAME[-4:],'w')
	fwrite.write(attr)
	for row in final:
		for data in row[:-1]:
			fwrite.write(data+',')
		fwrite.write(row[-1]+'\n')

	fwrite.close()

for i in range(1,4):
	downsa(i,easy,difficult)


