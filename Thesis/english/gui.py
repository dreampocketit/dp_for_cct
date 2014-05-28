from Tkinter import *
import numpy as np
from NeuroPy import NeuroPy
import time
from AppKit import NSSound
import random


RECORD_TIME=10

class App:


    try:
        object1=NeuroPy("/dev/tty.MindWaveMobile-DevA",57600)
    except:
        print 'bluetooth error'

    row_data = []
    f_out = open('output.csv','w')
    f_out.write('delta,midgamma,lowgamma,state\n')

    progress = 0
    audio_seq = []

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Understand", command=self.know)
        self.hi_there.pack(side=LEFT)

        self.hi_there = Button(frame, text="Don't understand", command=self.dont_know)
        self.hi_there.pack(side=LEFT)

        self.hi_there = Button(frame, text="Start", command=self.start_record)
        self.hi_there.pack(side=LEFT)

        for i in range(1,12):
            self.audio_seq.append(i)
        random.shuffle(self.audio_seq)

        print "english audio sequence:"+str(self.audio_seq)


        self.object1.start()


    def know(self):
        print 'I know'
        print self.row_data
        self.write_data('know')

    def dont_know(self):
        print 'dont know'
        print self.row_data
        self.write_data("don't know")

    def start_record(self):
        if self.object1.poorSignal!=0:
            print 'signal is poor'
        
        else:
            delta = []
            midgamma = []
            lowgamma = []


            print str(self.audio_seq[self.progress])

            sound = NSSound.alloc()
            sound.initWithContentsOfFile_byReference_(str(self.audio_seq[self.progress])+'.mp3', True)
            self.progress+=1 
            sound.play()


            for i in range(0,RECORD_TIME):
                if self.object1.poorSignal!=0:
                    print "because signal("+str(self.object1.poorSignal)+") is bad, we skip this round."
                    break
                else:
                    delta.append(self.object1.delta)
                    midgamma.append(self.object1.midGamma)
                    lowgamma.append(self.object1.lowGamma)
                    print 'recording'
                    time.sleep(1)
            if len(delta)==RECORD_TIME:
                print "std(delta)="+str(int(np.std(np.array(delta))))
                print "std(midgamma)="+str(int(np.std(np.array(midgamma))))
                print "std(lowgamma)="+str(int(np.std(np.array(lowgamma))))

                self.row_data=[int(np.std(np.array(delta))),int(np.std(np.array(midgamma))),int(np.std(np.array(lowgamma)))]

            sound.stop()

    def write_data(self,state):

        for ele in self.row_data:
            self.f_out.write(str(ele)+',')
        self.f_out.write(state+'\n')





root = Tk()

app = App(root)

root.mainloop()
root.destroy()