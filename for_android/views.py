# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import json
import ast

@csrf_exempt
def index(request):
	return render(request, "cct_experiment/index.html")
@csrf_exempt
def get_data(request):
	if request.method == "POST":
		print "\nconnected\n"
	print "receive data:"
	data = ast.literal_eval(request.POST['details'])['data']
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



	return HttpResponse(json.dumps({'state':'yes'}), content_type="application/json")