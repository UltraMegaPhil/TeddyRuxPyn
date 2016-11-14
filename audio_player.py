import alsaaudio as aa
import audioop
import wave
import time

class AudioPlayer:

    def __init__(self, chunkListener):
        self.chunkSize = 1024
        self.audioOutput = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
        self.audioOutput.setchannels(1)
        self.audioOutput.setrate(18000)
        self.audioOutput.setformat(aa.PCM_FORMAT_S16_LE)
        self.audioOutput.setperiodsize(self.chunkSize)
        self.chunkListener = chunkListener

    def play(self,fileName):
        wav = wave.open(fileName,'r')
        samplewidth = wav.getsampwidth()
        chunk = 0
        playLoop = True
        while playLoop:
            data = wav.readframes(self.chunkSize)
            if(data != ''):
                print "Audio Update"
                self.chunkListener.setCurrentChunk(chunk)
                self.audioOutput.write(data)
                
            time.sleep(0.02)
            
            chunk = (chunk + 1)
            playLoop = (data != '')
        
        wav.close()
        
    def analyze(self, fileName):
        print "Analysing file (", fileName, ")..."
        wav = wave.open(fileName,'r')
        samplewidth = wav.getsampwidth()
        maxVolumes = []
        analyseLoop = True
        
        while analyseLoop:
            data = wav.readframes(self.chunkSize)
            if(data != ''):
                # Grab data from the left audio channel
                # and find the peak volume in the chunk
                try:
                    mono = audioop.tomono(data, samplewidth, 1.0, 0.0)
                    maxVol = audioop.max(mono, 2)
                    scaledVol = (maxVol / 100)
                    maxVolumes.append(scaledVol)
                except audioop.error, e:
                    if e.message !="not a whole number of frames":
                        raise e
                    else:
                        maxVolumes.append(0)
            analyseLoop = (data != '')
        wav.close()

        # Move through the max volumes array and analyse each chunk to see
        # whether it is part of a rising, falling or holding volume trend
        volumeChanges = []
        for chunk in range(len(maxVolumes)):
            if(chunk < (len(maxVolumes) - 1)):
                if(maxVolumes[chunk + 1] > maxVolumes[chunk]):
                    volumeChanges.append(1)
                elif(maxVolumes[chunk + 1] < maxVolumes[chunk]):
                    volumeChanges.append(-1)
                else:
                    volumeChanges.append(0)
            else:
                # Last sample.
                volumeChanges.append(-1)
        return volumeChanges

    def volumeIncreasing(self):
        self.volumeSink.sinkVolumeChange(1)

    def volumeDecreasing(self):
        self.volumeSink.sinkVolumeChange(-1)

    def volumeHolding(self):
        self.volumeSink.sinkVolumeChange(0)
