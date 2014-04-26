# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import json

@csrf_exempt
def index(request):
	return render(request, "cct_experiment/index.html")
@csrf_exempt
def get_data(request):
	if request.method == "POST":
		print "\nconnected\n"
	print "receive data:"
	print request.POST
	return HttpResponse(json.dumps({'state':'yes'}), content_type="application/json")

