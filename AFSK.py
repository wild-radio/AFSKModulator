# AFSK Modulation class

import audiogen
import math


class AFSK:
    MARK_HZ = 1200.0
    SPACE_HZ = 2200.0
    BAUD_RATE = 1200.0

    def encode(self, data):
        for bit in data.tolist():
            for samples in self.modulate(bit):
                yield samples

    def modulate(self, bit):
        seconds_per_audio_sample = 1.0 / audiogen.sampler.FRAME_RATE
        seconds_per_bit = 1.0 / self.BAUD_RATE
        frequency = (self.MARK_HZ if bit else self.SPACE_HZ)
        two_pi = 2 * math.pi
        phase_change_per_sample = two_pi / (audiogen.sampler.FRAME_RATE / frequency)

        seconds, phase = 0, 0

        while (seconds < seconds_per_bit):
            yield math.sin(phase)

            seconds += seconds_per_audio_sample
            phase += phase_change_per_sample

            if (phase > two_pi):
                phase -= two_pi