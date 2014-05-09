import neurolab as nl
import numpy as np
import csv


input = []
target = []
f = open('power2-3.csv','rU')
for row in csv.reader(f):
	print row
	input.append(row[:-1])
	target.append([row[-1]])
input = np.array(input)
target  = np.array(target)

print input