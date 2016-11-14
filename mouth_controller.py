from threading import Thread
from time import sleep
import random

class MouthController:

    def __init__(self, busInterface):
        self.doRun = False
        self.updateThread = Thread(target=self.run, name="MouthControllerThread")
        self.busInterface = busInterface
        self.chunkAnalysisData = []
        self.currentChunk = -1

    def setCurrentChunk(self, chunk):
        self.currentChunk = chunk

    def startControlThread(self):
        self.doRun = True
        self.updateThread.start()
        
    def terminateControlThread(self):
        self.doRun = False
    
    def setChunkAnalysisData(self, data):
        self.chunkAnalysisData = data
                
    def run(self):
        print "Mouth control thread started"
        while (self.doRun):
            print "  Mouth update"
            if((self.currentChunk >= 0) and (self.currentChunk < len(self.chunkAnalysisData))):
                change = self.chunkAnalysisData[self.currentChunk]
                print "      CurrentChunk: ", self.currentChunk
                print "        ChunkValue: ", change
                if(change > 0):
                    self.openMouth()
                elif(change < 0):
                    self.closeMouth()
                else:
                    self.holdMouth()
            sleep(0.02)
        print "Mouth control thread finished!"

    def join(self):
        self.updateThread.join()

    def moveMouth(self, state):
        self.busInterface.motorMoveToState(state, True)

    def openMouth(self):
        self.busInterface.motorOpen(True)

    def closeMouth(self):
        self.busInterface.motorClose(True)

    def holdMouth(self):
        self.busInterface.motorHold(True)

