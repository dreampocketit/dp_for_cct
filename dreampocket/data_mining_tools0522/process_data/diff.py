import csv
import numpy as np

def differential():
	tar_array=['delta_c','theta_c','lowalpha_c','highalpha_c','lowbeta_c','highbeta_c','lowgamma_c','midgamma_c']
	in_f = open("../data/34-3-7.csv",'r')
	attrs = in_f.readline().split(',')


	matching = []
	matching_name = []
	for tar in tar_array:
		tmp_array = []
		for s in attrs:
			if tar in s:
				matching_name.append(s)
				tmp_array.append(attrs.index(s))
		matching.append(tmp_array)
	time_len = (len(matching_name)/8)-1

	final_output = []
	attr_name_array = []

	for original_attr in attrs[:8]:
		attr_name_array.append(original_attr)


	for attr_name in tar_array:
		for i in range(time_len):
			attr_name_array.append(attr_name+'c'+str(i))
	attr_name_array.append(attrs[-1])
	final_output.append(attr_name_array)

	for row in csv.reader(in_f):
		output_row = []

		for original_data in row[:8]:
			output_row.append(original_data)

		for freq in matching:
			freq_array = []
			for loc in freq:
				freq_array.append(int(row[loc]))

			for data in np.diff(freq_array).tolist():
				output_row.append(data)
		output_row.append(row[-1])	
		final_output.append(output_row)
	
	out_f = open('../data/34-3-7-diff.csv','w')
	w = csv.writer(out_f) 
	w.writerows(final_output)
	out_f.close() 
			



differential()
