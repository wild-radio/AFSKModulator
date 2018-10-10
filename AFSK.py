# AFSK Modulation and Demodulation class
import itertools

import audiogen
import math

import numpy
import scipy.signal.signaltools as signaltools
import scipy.signal as signal
from bitarray import bitarray
from scipy.io.wavfile import read

class AFSK:
    MARK_HZ = 1200.0
    SPACE_HZ = 2200.0
    BAUD_RATE = 1200.0
    TWO_PI = 2.0 * math.pi
    SAMPLE_RATE = audiogen.sampler.FRAME_RATE

    def encode(self, data):
        data = itertools.chain(
            bitarray("00000001"),
            data,
        )
        for sample in itertools.chain(
                audiogen.silence(0.15),
                self.modulate(data),
                audiogen.silence(0.15),
        ):
            yield sample

    def modulate(self, data):
        seconds_per_sample = 1.0 / self.SAMPLE_RATE
        phase, seconds= 0, 0

        clock = (x / self.BAUD_RATE for x in itertools.count(1))
        tones = (self.MARK_HZ if bit else self.SPACE_HZ for bit in data)

        for boundary, frequency in itertools.izip(clock, tones):
            phase_change_per_sample = self.TWO_PI / (self.SAMPLE_RATE / frequency)

            while seconds < boundary:
                yield math.sin(phase)

                seconds += seconds_per_sample
                phase += phase_change_per_sample

                if phase > self.TWO_PI:
                    phase -= self.TWO_PI


    def decode(self, file):
        audio_input = numpy.array(read(file)[1], dtype=float)
        filtered_signal = self.filterAFSK(audio_input)

        bits = self.getBits(filtered_signal)
        bits = self.removeStartSilence(bits)
        return self.removeHeader(bits)

    def removeStartSilence(self, bits):
        silence = True
        for bit in bits:
            if bit == False:
                silence = False
            if silence == False:
                yield bit

    def removeHeader(self, bits):
        header = True
        for bit in bits:
            if header == False:
                yield bit
            if bit:
                header = False

    def filterAFSK(self, audio_input):
        differential = numpy.diff(audio_input, 1)
        frequency_domain = numpy.abs(signaltools.hilbert(differential))
        pir_filter = signal.firwin(numtaps=2, cutoff=1800, fs=self.SAMPLE_RATE)

        return signal.filtfilt(pir_filter, [1.0], frequency_domain)

    def getBits(self, filtered_signal):
        bits_decoded = bitarray()

        step = self.SAMPLE_RATE / self.BAUD_RATE

        index = numpy.arange(step / 2.0, len(filtered_signal), step)
        index = index.astype(int)
        sampled_signal = filtered_signal[index]

        mean = numpy.mean(numpy.abs(filtered_signal))

        for bit in sampled_signal:
            if bit > mean:
                bits_decoded.append(False)
            else:
                bits_decoded.append(True)

        return bits_decoded


