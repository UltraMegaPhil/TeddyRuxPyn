from mouth_controller import MouthController
from eyes_controller import EyesController
from audio_player import AudioPlayer
from smbus_interface import SMBusInterface

import sys
from time import sleep

smbusDummyMode = True

# Get wave file parameter
if(len(sys.argv) != 2):
    print "Error: Incorrect number of arguments"
    print "    Usage: ", sys.argv[0], " <wav file>"
    sys.exit(1)
wavFile = sys.argv[1]


# Setup the SMB bus interface
busInterface = SMBusInterface(smbusDummyMode)        

        
# Setup the controllers
mouthController = MouthController(busInterface)
eyesController = EyesController(busInterface)
audioPlayer = AudioPlayer(mouthController)
print "Controllers configured"


# Set initial states
mouthController.closeMouth()
eyesController.openEyes()
sleep(0.5)
mouthController.holdMouth()
eyesController.holdEyes()
print "Initial facial states set"


# Analyze file
result = audioPlayer.analyze(wavFile)
mouthController.setChunkAnalysisData(result)
print "Wav file analysis complete"


# Start the controller threads
mouthController.startControlThread()
print "Mouth controller started"
eyesController.startControlThread()
print "Eye controller started"


# Play the audio
audioPlayer.play(wavFile)


# Terminate everything and wait for completion
mouthController.terminateControlThread()
eyesController.terminateControlThread()
mouthController.join()
eyesController.join()


# Set final states
mouthController.closeMouth()
eyesController.openEyes()
sleep(0.5)
mouthController.holdMouth()
eyesController.holdEyes()


print "Done"
