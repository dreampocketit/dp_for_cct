import csv



def coll(f_name):
	out_f = open('all.csv','a')
	in_f = open(f_name,'r')
	print f_name
	first = True
	for row in in_f:
		print row
		if first:
			print 1
			first = False
			continue
		else:
			out_f.write(row)
	in_f.close()
	out_f.close()


for i in range(10,31):
	f_name = str(i)+'-rev.csv'
	coll(f_name)


