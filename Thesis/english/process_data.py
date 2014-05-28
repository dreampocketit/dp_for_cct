import csv
for row in csv.reader(open('output.csv')):
	print row[0].split('-')