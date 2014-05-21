import csv
FILE_NAME = '../subjects/16.csv'

difficult = []
easy = []

first = True
for row in csv.reader(open(FILE_NAME,'rU')):
	if first:
		first = False
		continue
	if row[-2]=='difficult':
		difficult.append(row)
	else:
		easy.append(row)
print 'difficult'
print difficult
print 'easy'
print easy

if len(easy)>len(difficult):
	