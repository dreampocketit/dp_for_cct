from Tkinter import *
import numpy as np
from NeuroPy import NeuroPy
import time
from AppKit import NSSound
import random
import thread


RECORD_TIME=7



class App:


    try:
        object1=NeuroPy("/dev/tty.MindWaveMobile-DevA",57600)
    except:
        print 'bluetooth error'

    row_data = []
    f_out = open('CNN_output.csv','w')
    f_out.write('delta,midgamma,lowgamma,theta,highalpha,lowalpha,highbeta,lowbeta,state\n')
    sound = NSSound.alloc()
    sound.initWithContentsOfFile_byReference_('cnn.mp3', True)

    time_window = []

    state = 'easy'

    delta = []
    theta = []
    lo_al = []
    hi_al = []
    lo_be = []
    hi_be = []
    lo_ga = []
    mi_ga = []


    def __init__(self, master):
        
        thread.start_new_thread(self.start_to_record, ())


        frame = Frame(master)
        frame.bind("<Key>", self.key)
        frame.pack()
        frame.focus_set()

#        self.text = Text(root)
#        self.text.insert(INSERT, "Hello.....")
#        self.text['width']=150
#s        self.text.pack(side=LEFT)

        self.qui_btn = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.qui_btn.pack(side=LEFT)

        self.sta_btn = Button(frame, text="Start", command=self.start_to_play)
        self.sta_btn.pack(side=LEFT)
        self.sta_btn['width']='15'

        self.object1.start()


    def key(self, event):
        #print "pressed", repr(event.char)
        self.state = 'hard'

    def start_to_play(self):

        self.sound.play()
        self.sound.resume()


    def start_to_record(self):


        while True:
            replay = False    

            while self.object1.poorSignal != 0:
                print self.object1.poorSignal
                self.sound.pause()
                replay = True
                time.sleep(1)
                self.delta = []
                self.theta = []
                self.lo_al = []
                self.hi_al = []
                self.lo_be = []
                self.hi_be = []
                self.lo_ga = []
                self.mi_ga = []

            if replay:
                self.sound.resume()


            self.delta.append(self.object1.delta)
            self.theta.append(self.object1.theta)
            self.lo_al.append(self.object1.lowAlpha)
            self.hi_al.append(self.object1.highAlpha)
            self.lo_be.append(self.object1.lowBeta)
            self.hi_be.append(self.object1.highBeta)
            self.lo_ga.append(self.object1.lowGamma)
            self.mi_ga.append(self.object1.midGamma)
            
            if len(self.delta)>8:
                self.delta.pop(0)
                self.theta.pop(0)
                self.lo_al.pop(0)
                self.hi_al.pop(0)
                self.lo_be.pop(0)
                self.hi_be.pop(0)
                self.lo_ga.pop(0)
                self.mi_ga.pop(0)
                print self.state
                print self.delta
                self.write_data()
                self.state = 'easy'

            time.sleep(1)
        print self.object1.poorSignal



    def write_data(self):
        for d in self.delta[:-1]:
            self.f_out.write(str(d)+'-')
        self.f_out.write(str(self.delta[-1])+',')

        for t in self.theta[:-1]:
            self.f_out.write(str(t)+'-')
        self.f_out.write(str(self.theta[-1])+',')
                
        for a in self.lo_al[:-1]:
            self.f_out.write(str(a)+'-')
        self.f_out.write(str(self.lo_al[-1])+',')

        for a in self.hi_al[:-1]:
            self.f_out.write(str(a)+'-')
        self.f_out.write(str(self.hi_al[-1])+',')

        for b in self.lo_be[:-1]:
            self.f_out.write(str(b)+'-')
        self.f_out.write(str(self.lo_be[-1])+',')

        for b in self.hi_be[:-1]:
            self.f_out.write(str(b)+'-')
        self.f_out.write(str(self.hi_be[-1])+',')

        for g in self.lo_ga[:-1]:
            self.f_out.write(str(g)+'-')
        self.f_out.write(str(self.lo_ga[-1])+',')

        for g in self.mi_ga[:-1]:
            self.f_out.write(str(g)+'-')
        self.f_out.write(str(self.mi_ga[-1])+',')

        self.f_out.write(self.state+"\n")

root = Tk()

app = App(root)

root.mainloop()
root.destroy()