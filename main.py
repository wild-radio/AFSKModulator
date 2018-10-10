# Main python file
import sys

from AFSK import AFSK
from AudioRecorder import AudioRecorder
from bitarray import bitarray
from time import sleep
import audiogen
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(0o10, GPIO.OUT)


if (sys.argv[1] == "modulate"):
    with open (sys.argv[2], "rb") as f:
        barray = bitarray()
        barray.fromfile(f)
        afsk = AFSK()
        modulated_audio = afsk.encode(barray)
        GPIO.output(0o10, True)
        with open ("temp_wav.wav", "wb") as out:
            audiogen.sampler.write_wav(out, modulated_audio)
        
        GPIO.output(0o10, False)
        exit(0)
#
# with open (sys.argv[2], "rb") as f:
#     afsk = AFSK()
#     bits = bitarray(afsk.decode(f))
#     print bits.tobytes()

recorder = AudioRecorder()
recorder.listen()
