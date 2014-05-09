from Tkinter import *
import numpy as np
from NeuroPy import NeuroPy
import time
from AppKit import NSSound
import random
import thread


RECORD_TIME=7



class App:


#    try:
#        object1=NeuroPy("/dev/tty.MindWaveMobile-DevA",57600)
#    except:
#        print 'bluetooth error'

    row_data = []
    f_out = open('output.csv','w')
    f_out.write('delta,midgamma,lowgamma,theta,highalpha,lowalpha,highbeta,lowbeta,state\n')
    sound = NSSound.alloc()
    sound.initWithContentsOfFile_byReference_('cnn.mp3', True)

    time_window = []

    delta = []
    theta = []
    lo_al = []
    hi_al = []
    lo_be = []
    hi_be = []
    lo_ga = []
    mi_ga = []

    read = True


    def __init__(self, master):
        
        try:
            thread.start_new_thread( start_to_record, ("Thread-1", 2, ) )
            
        except:
            print "Error: unable to start thread"

        frame = Frame(master)
        frame.pack()

        self.text = Text(root)
        self.text.insert(INSERT, "Hello.....")
        self.text['width']=150
        self.text.pack(side=LEFT)

        self.qui_btn = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.qui_btn.pack(side=LEFT)

        self.hard_btn = Button(frame, text="hard", command=self.hard)
        self.hard_btn.pack(side=LEFT)
        self.hard_btn['width']='15'

        self.sta_btn = Button(frame, text="Start", command=self.start_to_play)
        self.sta_btn.pack(side=LEFT)
        self.sta_btn['width']='15'

#        self.object1.start()



    def hard(self,):
        print 'hard'
        self.cor_or_not = "hard"
        self.text.insert(INSERT, 'hard\n')
        self.text.see(END)

        write_data()

        #self.sound.pause()


    def start_to_play(self):

        self.sound.play()
        self.sound.resume()


    def start_to_record(self):

        while self.read:
            
            delta.append(self.object1.delta)
            theta.append(self.object1.theta)
            lo_al.append(self.object1.lowAlpha)
            hi_al.append(self.object1.highAlpha)
            lo_be.append(self.object1.lowBeta)
            hi_be.append(self.object1.highBeta)
            lo_ga.append(self.object1.lowGamma)
            mi_ga.append(self.object1.minGamma)
            
            if len(delta)>8:
                delta.pop(0)
                theta.pop(0)
                lo_al.pop(0)
                hi_al.pop(0)
                lo_be.pop(0)
                hi_be.pop(0)
                lo_ga.pop(0)
                mi_ga.pop(0)

            print delta
            time.sleep(1)



    def write_data(self):
        for d in delta[:-1]:
            f_out.write(str(d)+'-')
        f_out.write(str(delta[-1])+',')

        for t in theta[:-1]:
            f_out.write(str(t)+'-')
        f_out.write(str(theta[-1])+',')
                
        for a in lo_al[:-1]:
            f_out.write(str(a)+'-')
        f_out.write(str(lo_al[-1])+',')

        for a in hi_al[:-1]:
            f_out.write(str(a)+'-')
        f_out.write(str(hi_al[-1])+',')

        for b in lo_be[:-1]:
            f_out.write(str(b)+'-')
        f_out.write(str(lo_be[-1])+',')

        for b in hi_be[:-1]:
            f_out.write(str(b)+'-')
        f_out.write(str(hi_be[-1])+',')

        for g in lo_ga[:-1]:
            f_out.write(str(g)+'-')
        f_out.write(str(lo_ga[-1])+',')

        for g in mi_ga[:-1]:
            f_out.write(str(g)+'-')
        f_out.write(str(mi_ga[-1])+',')

        f_out.write("hard\n")

root = Tk()

app = App(root)

root.mainloop()
root.destroy()