from threading import Thread
import time
import random
import smbus

class EyesController:

    def __init__(self, busInterface):
        self.doRun = False
        self.updateThread = Thread(target=self.run, name="EyesControllerThread")
        self.busInterface = busInterface
        self.eyesValue = 0;
        
    def startControlThread(self):
        self.doRun = True
        self.updateThread.start()
        
    def terminateControlThread(self):
        self.doRun = False
                
    def run(self):
        print "Eye control thread started"
        while (self.doRun):
            if(self.eyesValue == 3):
                # If eyes fully closed, fully open them, don't pick a random 
                # state
                self.eyesValue = 0
            else:
                # 15% chance of blinking
                if(random.random() > 0.85):
                    self.eyesValue = 3
                elif(random.random() > 0.95):
		            self.eyesvalue = 0
                else:
                    #self.eyesValue = random.randint(0, 1)
		            self.eyesValue = 0
            
            self.moveEyes(self.eyesValue)            
                            
            if(self.eyesValue == 3):
                time.sleep(0.1)
            else:
		time.sleep(0.3)
        print "Eye control thread finished!"
            
    def join(self):
        self.updateThread.join()

    def moveEyes(self, state):
        self.busInterface.motorMoveToState(state, False)

    def openEyes(self):
        self.busInterface.motorOpen(False)

    def closeEyes(self):
        self.busInterface.motorClose(False)

    def holdEyes(self):
        self.busInterface.motorHold(False)

