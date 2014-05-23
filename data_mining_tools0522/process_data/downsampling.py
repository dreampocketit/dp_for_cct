import csv
import random
FILE_NAME = '../subjects/27.csv'

difficult = []
easy = []
attr = ''
final = []

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


if len(easy)>len(difficult):
	random.shuffle(easy)
	for i in range(len(difficult)):
		final.append(easy[i])
		final.append(difficult[i])

else:
	random.shuffle(difficult)
	for i in range(len(easy)):
		final.append(easy[i])
		final.append(difficult[i])

fwrite = open(FILE_NAME[0:-4]+'-rev'+FILE_NAME[-4:],'w')
fwrite.write(attr)
for row in final:
	for data in row[:-1]:
		fwrite.write(data+',')
	fwrite.write(row[-1]+'\n')

fwrite.close()


