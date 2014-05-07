import csv

f = open('power2-4.csv','r')
f.next()
for row in csv.reader(f):
	print row[:-1]