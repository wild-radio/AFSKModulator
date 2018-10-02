# Main python file
import sys

import argparse

from AFSK import AFSK
from bitarray import bitarray
import audiogen



with open (sys.argv[1], "rb") as f:
    barray = bitarray()
    barray.fromfile(f)
    afsk = AFSK()
    modulated_audio = afsk.encode(barray)
    audiogen.sampler.write_wav(sys.stdout, modulated_audio)