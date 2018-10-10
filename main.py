# Main python file
import sys

from AFSK import AFSK
from AudioRecorder import AudioRecorder
from bitarray import bitarray
import audiogen

if (sys.argv[1] == "modulate"):
    with open (sys.argv[2], "rb") as f:
        barray = bitarray()
        barray.fromfile(f)
        afsk = AFSK()
        modulated_audio = afsk.encode(barray)
        audiogen.sampler.write_wav(sys.stdout, modulated_audio)
        exit(0)
#
# with open (sys.argv[2], "rb") as f:
#     afsk = AFSK()
#     bits = bitarray(afsk.decode(f))
#     print bits.tobytes()

recorder = AudioRecorder()
recorder.listen()