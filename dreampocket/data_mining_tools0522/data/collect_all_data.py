import csv



def coll(f_name):
	out_f = open('all.csv','a')
	in_f = open(f_name,'r')

	print in_f.readline()
	for row in in_f:

		out_f.write(row)
	in_f.close()


for i in range(10,33):
	f_name = str(i)+'-3-7_attr.csv'
	coll(f_name)


