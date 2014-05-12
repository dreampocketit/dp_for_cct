# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import json
import numpy as np
from NeuroPy import NeuroPy
import time
import random

sys_state={}
object1=NeuroPy("/dev/tty.MindWaveMobile-DevA",57600)

ANSWER_SHEET = '/Users/changchengtu/Google Drive/dp_for_cct/cct_experiment/4-answer_sheet.txt'
doc_id = ANSWER_SHEET.split('/')[-1].split('-')[0]
RECORD_TIME=8

###################### sequence and answer #####################
progress = 0
audio_seq = []
ques = []
answer = []
for i in range(11,41):
	audio_seq.append(i)
random.shuffle(audio_seq)

answer_sheet = open(ANSWER_SHEET,'r')
for row in answer_sheet:
	ques.append(row.split('::')[0]+row.split('::')[1])
	answer.append(row.split('::')[2])

###################### write data ####################

f_out = open('output'+doc_id+'.csv','w')
f_out.write('delta,theta,lowalpha,highalpha,lowbeta,highbeta,lowgamma,midgamma,state,answer\n')

######################################################
row_data = []


try:
	object1.start()
	sys_state['bluetooth']='yes'
	print "neurosky is connected"
except:
	sys_state['bluetooth']='no'
	print "neurosky is not connected"

sys_state['next']='yes'
sys_state['end']='no'



def index(request):
	return render(request, "cct_experiment/index.html")

def get_sys_state(request):
	global sys_state
	global object1
	global audio_seq
	global progress
	global doc_id

	sys_state['poorSignal'] = object1.poorSignal
	sys_state['theta'] = object1.theta
	if int(progress)==30:
		sys_state['audio_seq'] = audio_seq[29]
	else:
		sys_state['audio_seq'] = audio_seq[int(progress)]

	sys_state['progress'] = progress
	sys_state['doc_id'] = int(doc_id)

	if int(progress)==30:
		tmp_ques = ques[audio_seq[29]-11].split('(')
		sys_state['quesA'] = tmp_ques[1]
		sys_state['quesB'] = tmp_ques[2]
		sys_state['quesC'] = tmp_ques[3]		
	else:
		tmp_ques = ques[audio_seq[int(progress)]-11].split('(')
		sys_state['quesA'] = tmp_ques[1]
		sys_state['quesB'] = tmp_ques[2]
		sys_state['quesC'] = tmp_ques[3]

	print tmp_ques[0]


	return HttpResponse(json.dumps(sys_state), content_type="application/json")


def start_record(request):
	global progress
	global object1
	global sys_state


	if progress == 30:
		print 'No more question'
		sys_state['end']='yes'
	else:
		delta = []
		midgamma = []
		lowgamma = []
		theta = []
		highalpha = []
		lowalpha = []
		highbeta = []
		lowbeta = []



		### start to record EEG ###
		for i in range(0,RECORD_TIME):
			if object1.poorSignal!=0:
				print "because signal("+str(object1.poorSignal)+") is bad, we skip this round."
				break
			else:
				sys_state['test'] = i
				delta.append(object1.delta)
				midgamma.append(object1.midGamma)
				lowgamma.append(object1.lowGamma)
				theta.append(object1.theta)
				highalpha.append(object1.highAlpha)
				lowalpha.append(object1.lowAlpha)
				highbeta.append(object1.highBeta)
				lowbeta.append(object1.lowBeta)


				print 'theta:'+str(object1.theta)
				print 'recording'
				time.sleep(1)

		### if all 7 secs is good, save data ###
		if len(delta)==RECORD_TIME:

			row_data.append(delta)
			row_data.append(theta)
			row_data.append(lowalpha)
			row_data.append(highalpha)
			row_data.append(lowbeta)
			row_data.append(highbeta)
			row_data.append(lowgamma)
			row_data.append(midgamma)

			progress+=1

			print 'progress : '+str(progress)

			
		return HttpResponse(json.dumps(sys_state), content_type="application/json")

def write_data(request):
	global f_out
	global row_data
	print '#############################'
	state = request.GET.get('diff')
	correct = 'no'
	if answer[int(audio_seq[progress-1])-11][0] == request.GET.get('ans'):
		correct = 'yes'
	else:
		correct = 'no'

	print request.GET.get('diff')
	print correct
	for ele in row_data:
		for data in ele[:-1]:
			f_out.write(str(data)+'-')
		f_out.write(str(ele[-1]))
		f_out.write(',')
	f_out.write(state+','+correct+'\n')
	row_data = []
	print 'write:'+state+','+correct+'\n'
	return HttpResponse('successed to server', content_type="application/json")



