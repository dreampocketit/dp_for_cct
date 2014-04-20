from Tkinter import *
import numpy as np
from NeuroPy import NeuroPy
import time
from AppKit import NSSound
import random
import tkMessageBox

ANSWER_SHEET = '2-answer_sheet.txt'
doc_id = ANSWER_SHEET.split('-')[0]
RECORD_TIME=7

class App:


    try:
        object1=NeuroPy("/dev/tty.MindWaveMobile-DevA",57600)
    except:
        print 'bluetooth error'

    row_data = []
    f_out = open('output.csv','w')
    f_out.write('delta,theta,lowalpha,highalpha,lowbeta,highbeta,lowgamma,midgamma,state,answer\n')

    dif_or_not = ''

    progress = 0
    audio_seq = []

    win = None

    ques = []
    answer = []



    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.text = Text(root)
        self.text.insert(INSERT, "Hello.....")
        self.text['width']=150
        self.text.pack(side=LEFT)

        self.qui_btn = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.qui_btn.pack(side=LEFT)


        self.sta_btn = Button(frame, text="Start", command=self.start_record)
        self.sta_btn.pack(side=LEFT)
        self.sta_btn['width']='15'

        for i in range(11,41):
            self.audio_seq.append(i)
        random.shuffle(self.audio_seq)

        answer_sheet = open(ANSWER_SHEET,'r')

        for row in answer_sheet:

            self.ques.append(row.split('::')[1])
            self.answer.append(row.split('::')[2])

        print "english audio sequence:"+str(self.audio_seq)


        self.object1.start()


    def easy(self):
        print 'easy'
        self.dif_or_not = 'easy'
        self.dif_win.destroy()
        self.dialog()

    def hard(self,):
        print 'hard'
        self.dif_or_not = "hard"
        self.dif_win.destroy()
        self.dialog()

    def process_A(self):
        print 'choose A'

        if self.answer[int(self.audio_seq[self.progress])-11][0] == 'A':
            print 'the answer is:'+self.answer[int(self.audio_seq[self.progress])-11]
            print 'correct'
            self.write_data(self.dif_or_not,'correct')
        else:
            print 'the answer is:'+self.answer[int(self.audio_seq[self.progress])-11]
            print 'wrong'
            self.write_data(self.dif_or_not,'wrong')
        self.progress+=1
        self.win.destroy()
        self.start_record()

    def process_B(self):
        print 'choose B'

        if self.answer[int(self.audio_seq[self.progress])-11][0] == 'B':
            print 'the answer is:'+self.answer[int(self.audio_seq[self.progress])-11]
            print 'correct'
            self.write_data(self.dif_or_not,'correct')
        else:
            print 'the answer is:'+self.answer[int(self.audio_seq[self.progress])-11]
            print 'wrong'
            self.write_data(self.dif_or_not,'wrong')
        self.progress+=1
        self.win.destroy()
        self.start_record()

    def process_C(self):
        print 'choose C'

        if self.answer[int(self.audio_seq[self.progress])-11][0] == 'C':
            print 'the answer is:'+self.answer[int(self.audio_seq[self.progress])-11]
            print 'correct'
            self.write_data(self.dif_or_not,'correct')
        else:
            print 'the answer is:'+self.answer[int(self.audio_seq[self.progress])-11]
            print 'wrong'
            self.write_data(self.dif_or_not,'wrong')
        self.progress+=1
        self.win.destroy()
        self.start_record()


    def difficulty(self):

        print 'difficulty'
        self.dif_win = Toplevel()
        self.dif_win.geometry("300x150")
        Label(self.dif_win,  text='Is it diffucult to you?').pack()
        Button(self.dif_win, text='difficult', command=self.hard).pack(side=RIGHT)
        Button(self.dif_win, text='easy', command=self.easy).pack(side=RIGHT)

        

    def dialog(self):

        self.win = Toplevel()
        self.win.geometry("400x150")
        tmp_s = ''
        choices = self.ques[int(self.audio_seq[self.progress])-11].split('(')
        for cho in choices:
            tmp_s+= cho+'\n'
        self.text.see(END)                                     
        Label(self.win,  text=tmp_s).pack()
        Button(self.win, text='C', command=self.process_C).pack(side=RIGHT)
        Button(self.win, text='B', command=self.process_B).pack(side=RIGHT)
        Button(self.win, text='A', command=self.process_A).pack(side=RIGHT)
           


    def start_record(self):

        if self.object1.poorSignal!=0:
            print 'signal is poor:'+str(self.object1.poorSignal)
            self.text.insert(INSERT, 'bad signal\n')
            self.sta_btn['state'] = 'normal'
        
        else:
            delta = []
            midgamma = []
            lowgamma = []
            theta = []
            highalpha = []
            lowalpha = []
            highbeta = []
            lowbeta = []

            self.text.insert(INSERT,'\n\n')
            self.text.insert(INSERT, 'progress:'+str(self.progress)+':\n')
            self.text.insert(INSERT, 'question:'+str(self.audio_seq[self.progress])+':\n')
            self.text.see(END)
            print str(self.audio_seq[self.progress])

            sound = NSSound.alloc()
            sound.initWithContentsOfFile_byReference_(str(doc_id)+'-'+str(self.audio_seq[self.progress])+'.mp3', True)
            sound.play()


            for i in range(0,RECORD_TIME):
                if self.object1.poorSignal!=0:
                    print "because signal("+str(self.object1.poorSignal)+") is bad, we skip this round."
                    break
                else:
                    delta.append(self.object1.delta)
                    midgamma.append(self.object1.midGamma)
                    lowgamma.append(self.object1.lowGamma)
                    theta.append(self.object1.theta)
                    highalpha.append(self.object1.highAlpha)
                    lowalpha.append(self.object1.lowAlpha)
                    highbeta.append(self.object1.highBeta)
                    lowbeta.append(self.object1.lowBeta)

                    print 'delta:'+str(self.object1.delta)
                    print 'theta:'+str(self.object1.theta)
                    print 'highalpha:'+str(self.object1.highAlpha)
                    print 'midgamma:'+str(self.object1.midGamma)
                    print 'recording'
                    print self.object1.poorSignal
                    time.sleep(1)
            sound.stop()

            if len(delta)==RECORD_TIME:

                self.row_data.append(delta)
                self.row_data.append(theta)
                self.row_data.append(lowalpha)
                self.row_data.append(highalpha)
                self.row_data.append(lowbeta)
                self.row_data.append(highbeta)
                self.row_data.append(lowgamma)
                self.row_data.append(midgamma)
                print self.row_data
                self.sta_btn['state'] = 'disabled'

                self.difficulty()
            else:
                self.start_record()


    def write_data(self,state,correct):

        for ele in self.row_data:
            for data in ele[:-1]:
                self.f_out.write(str(data)+'-')
            self.f_out.write(str(ele[-1]))
            self.f_out.write(',')
        self.f_out.write(state+','+correct+'\n')
        self.row_data = []
        print '=============write=============='





root = Tk()

app = App(root)


root.mainloop()
root.destroy()