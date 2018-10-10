# Main python file
import sys

import pyaudio
import wave

from AFSK import AFSK
from AudioRecorder import AudioRecorder
from bitarray import bitarray
import audiogen
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(0o10, GPIO.OUT)

def play():
    chunk = 1024
    f = wave.open(r"temp_wav.wav", "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=44100,
                              input=False,
                              output=True,
                              frames_per_buffer=chunk)
    data = f.readframes(chunk)

    while data:
        stream.write(data)
        data = f.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()

if (sys.argv[1] == "modulate"):
    with open (sys.argv[2], "rb") as f:
        barray = bitarray()
        barray.fromfile(f)
        afsk = AFSK()
        modulated_audio = afsk.encode(barray)
        GPIO.output(0o10, True)
        with open ("temp_wav.wav", "wb") as out:
            audiogen.sampler.write_wav(out, modulated_audio)
        
	play()
        GPIO.output(0o10, False)
        exit(0)
#
# with open (sys.argv[2], "rb") as f:
#     afsk = AFSK()
#     bits = bitarray(afsk.decode(f))
#     print bits.tobytes()

recorder = AudioRecorder()
recorder.listen()
