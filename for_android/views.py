# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import json
import ast

f_out = open('output.csv','w')
f_out.write('delta,theta,lowalpha,highalpha,lowbeta,highbeta,lowgamma,midgamma,state,answer\n')

@csrf_exempt
def index(request):
	return render(request, "for_android/index.html")

def trans_data(source_data):

	data = ast.literal_eval(source_data)['data']
	
	delta = ast.literal_eval(data)[0]
	theta = ast.literal_eval(data)[1]
	lowAlpha = ast.literal_eval(data)[2]
	highAlpha = ast.literal_eval(data)[3]
	lowBeta = ast.literal_eval(data)[4]
	highBeta = ast.literal_eval(data)[5]
	lowGamma = ast.literal_eval(data)[6]
	midGamma = ast.literal_eval(data)[7]

	print "delta:"+str(delta)
	print "theta:"+str(theta)
	print "lowAlpha:"+str(lowAlpha)
	print "highAlpha:"+str(highAlpha)
	print "lowBeta:"+str(lowBeta)
	print "highBeta:"+str(highBeta)
	print "lowGamma:"+str(lowGamma)
	print "midGamma:"+str(midGamma)

	new_data = []
	new_data.append(delta)
	new_data.append(theta)
	new_data.append(lowAlpha)
	new_data.append(highAlpha)
	new_data.append(lowBeta)
	new_data.append(highBeta)
	new_data.append(lowGamma)
	new_data.append(midGamma)

	return new_data

@csrf_exempt
def get_diff_data(request):

	if request.method == "POST":
		print "\nconnected\n"
	print "difficult"

	write_data(trans_data(request.POST['details']), "diff")

	return HttpResponse(json.dumps({'state':'yes'}), content_type="application/json")


@csrf_exempt
def get_easy_data(request):

	if request.method == "POST":
		print "\nconnected\n"
	print "easy"

	write_data(trans_data(request.POST['details']), "easy")

	return HttpResponse(json.dumps({'state':'yes'}), content_type="application/json")

def write_data(row_data,state):
	global f_out
	for ele in row_data:
		print ele
		for data in ele[:-1]:
			f_out.write(str(data)+'-')
		f_out.write(str(ele[-1]))
		f_out.write(',')
	f_out.write(state+',null\n')

	print 'write:'+state+'\n'
