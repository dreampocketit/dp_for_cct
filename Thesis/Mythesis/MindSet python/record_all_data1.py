#!/usr/bin/env python
# encoding: utf-8
"""
get meditation and rawEeg
"""

"""
DEPRECATED!!! DONT USE THIS OMG
"""
import thread
from datetime import datetime
from Tkinter import *
import time
from socket import *
import hashlib
import json
#from speech import say

HOST = '127.0.0.1'
PORT = 13854

#cs = socket(AF_INET, SOCK_STREAM)
#cs.connect(ADDR)

#auth_dict = {'appName':'TestApp', 'appKey':hashlib.sha1().hexdigest()}
conf_dict = {'enableRawOutput':True, 'format':'Json'}
#cs.send(json.dumps(auth_dict))
#cs.send(json.dumps(conf_dict))
#import code
#code.interact(local=locals())

#while True:
#	char = cs.recv(1)
#	if char=='\r':
#		print 'found delimiter'
#
#cs.close()
class ThinkGearConnection(object):
	
	def __init__(self, host=HOST, port=PORT, appName='Python', username='Anonymous'):
		self.host = host
		self.port = port
		self.appName = appName
		self.username = username
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.connect((self.host, self.port))
		self._sendMessage(conf_dict)
		self.recording = False
		self.is_running = True
		self.data_stream_active = False
			
	def data(self):
		self.data_stream_active = True
		my_data = None
		while self.is_running:
			temp_json = ''
			cur_char = self.sock.recv(1)
			while cur_char != '\r':
				temp_json += cur_char
				cur_char = self.sock.recv(1)
			my_data = json.decoder.JSONDecoder().decode(temp_json)
			yield my_data
		self.sock.close()
		self.data_stream_active = False
		
	def close(self):
		self.is_running = False		
		
	def setUser(self, userName):
		self._sendMessage({'setUser':{'userName':userName}})
		
	def getUsers(self):
		self._sendMessage({'getUsers':self.appName})
		
	def deleteUser(self, userName, userID):
		self._sendMessage({'deleteUser':{'userName':self.username, 'userId':userID}})
		
	def startRecording(self, rawEeg=True, poorSignalLevel=True, eSense=True, eegPower=True, blinkStrength=True):
		if self.data_stream_active:
			return
		self._sendMessage({'startRecording':{'rawEeg':rawEeg, 'poorSignalLevel':poorSignalLevel, 'sSense':eSense, 'eegPower':eegPower, 'blinkStrength':blinkStrength}, 'applicationName':self.appName})
		self.recording = True
		
	def stopRecording(self):
		if self.data_stream_active or not self.recording:
			return
		self._sendMessage({'stopRecording':self.appName})
		self.recording = False
		
	def cancelRecording(self):
		if self.data_stream_active or not self.recording:
			return
		self._sendMessage({'cancelRecording':self.appName})
		
	def getSessionIDs(self):
		self._sendMessage({'getSessionIds':self.appName})
		
	def retrieveSession(self, sessionID):
		self._sendMessage({'getSessionId':sessionID, 'applicationName':self.appName})
		
	def _sendMessage(self, messageDict):
		self.sock.send(json.dumps(messageDict))

def datastream(host=HOST, port=PORT):
	cs = socket(AF_INET, SOCK_STREAM)
	cs.connect((host, port))
	cs.send(json.dumps(conf_dict))
	data = None
	while True:
		temp_json = ''
		cur_char = cs.recv(1)
		while cur_char != '\r':
			temp_json += cur_char
			cur_char = cs.recv(1)
		data = json.decoder.JSONDecoder().decode(temp_json)
		yield data
		#if u'poorSignalLevel' in data and data[u'poorSignalLevel'] == 200:
		#	break
		#else:
		#	yield data 
	cs.close()
	yield data


#printed_connecting = False
#for d in datastream():
#	
#	if u'eSense' in d:
#		print 'attention: %f\tmeditation: %f' % (d[u'eSense'][u'attention'], d[u'eSense']['meditation'])
#		print d
#	else:
#		if not printed_connecting:
#			print 'connecting...'
#			printed_connecting = True
keybocard_input = '0'
def record_data():
	tgc = ThinkGearConnection()
	data_output = ""
	record_range = 0
	for d in tgc.data():
	
		if u'poorSignalLevel' in d:
			print 'poorSignalLevel' + str(float(d[u'poorSignalLevel']))

		if u'eegPower' in d:
			print 'delta' + str(float(d[u'eegPower'][u'delta']))
			print 'theta' + str(float(d[u'eegPower'][u'theta']))
			print 'lowAlpha' + str(float(d[u'eegPower'][u'lowAlpha']))
			print 'highAlpha' + str(float(d[u'eegPower'][u'highAlpha']))
			print 'lowBeta' + str(float(d[u'eegPower'][u'lowBeta']))
			print 'highBeta' + str(float(d[u'eegPower'][u'highBeta']))
			print 'lowGamma' + str(float(d[u'eegPower'][u'lowGamma']))
			print 'highGamma' + str(float(d[u'eegPower'][u'highGamma']))
			print keybocard_input

			

			record_range+=1

		if u'blinkStrength' in d:
			print 'blinkStrength' + str(float(d[u'blinkStrength']))
	
		if u'eSense' in d:
			print 'esense meditation' + str(float(d[u'eSense'][u'meditation']))+str(datetime.now())
			print 'esense attention' + str(float(d[u'eSense'][u'attention']))+str(datetime.now())

			if record_range>100:
				print('Exiting data collection')

				tgc.close()
		print d

	text_file = open("Output.txt", "w")
	#text_file.write(str(raw_data))
	text_file.write("delta, theta, lowAlpha, highAlpha, lowBeta, highBeta, lowGamma, highGamma, time, classification" + '\n')
	text_file.write(data_output)
	text_file.close()


def helloCallBack():
	try:
		thread.start_new_thread ( record_data,())
	except:
		print 'error'

def key(event):
	global keybocard_input
	keybocard_input = str(repr(event.char))

def callback(event):
    frame.focus_set()
    print "clicked at", event.x, event.y 

root = Tk()
Button = Button(root, text ="startRecording", command = helloCallBack)
Button.pack()
frame = Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.bind("<Button-1>", callback)
frame.pack()
root.mainloop()

print('Done with program')
