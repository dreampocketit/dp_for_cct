import csv


def sel_attr(f_name):
	tar_array=['gamma','beta']
	in_f = open("../data/"+f_name+".csv",'r')
	attrs = in_f.readline().split(',')


	matching = []
	for tar in tar_array:
		for s in attrs:
			if tar in s:
				matching.append(s)

	results = []
	for similiar_word in matching:
		results.append(attrs.index(similiar_word))


	out_f = open("../data/"+f_name+"_attr.csv","w")

	new_attrs = []
	new_data = []
	for old_attr in attrs:
		if old_attr not in matching:
			
			new_attrs.append(old_attr) 
	new_data.append(new_attrs)
	new_data[0][-1]='state'
	for row in csv.reader(in_f):
		new_row = []
		for i in range(0,len(row)):
			if i not in results:
				new_row.append(row[i])

		new_data.append(new_row)

	w = csv.writer(out_f)  
	w.writerows(new_data)  
	in_f.close()
	out_f.close() 

subjects = ['01','02','03','04','05','06','07','08','09','10',
			'11','12','13','14','15','16','17','18','19','20',
			'21','22','23','24','25','26','27','28','29','30','31','32','33']
#subjects=['01']
seconds=['3-5','3-6','3-7']

for s in subjects:
	for t in seconds:
		sel_attr(s+"-"+t)