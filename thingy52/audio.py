"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""
from bluepy.btle import DefaultDelegate
import pyaudio
import wave
import audioop
import binascii

CHUNK = 20
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 11025
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Intel ADPCM step variation table
INDEX_TABLE = [-1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8,]

# ADPCM step size table
STEP_SIZE_TABLE = [7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45, 50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130, 143, 157, 173, 190, 209,
        230, 253, 279, 307, 337, 371, 408, 449, 494, 544, 598, 658, 724, 796, 876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
        5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767]

class RecordingDelegate(DefaultDelegate):
    def __init__(self, handles):
        DefaultDelegate.__init__(self)
        self.handles = handles


        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        self.frames = []

        self.state = None

    def handleNotification(self, cHandle, data):
        thingy_char = self.handles[cHandle]

        val = thingy_char.conversion_func(data)
        #print(val)
        pcm, self.state = audioop.adpcm2lin(val, 4, self.state)
        #pcm, self.state = audioop.adpcm2lin(binascii.a2b_hex(data), 4, self.state)
        self.frames.append(pcm)

        # data = self.stream.read(CHUNK)
        """
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = self.stream.read(CHUNK)
            self.frames.append(data)"""

    def finish(self):
        print("* done recording")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()



if __name__ == "__main__":
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def adpcm_decode(adpcm):

    # Allocate output buffer
    #pcm = new Buffer(adpcm.data.length*4)
    pcm = []
    # The first 2 bytes of ADPCM frame are the predicted value
    valuePredicted = adpcm.header.readInt16BE(0)
    # The 3rd byte is the index value
    index = adpcm.header.readInt8(2)

    if index < 0:
        index = 0
    if index > 88:
        index = 88

    #diff #/* Current change to valuePredicted */
    bufferStep = False
    inputBuffer = 0
    delta = 0
    sign = 0
    step = STEP_SIZE_TABLE[index]
    _in = 0
    for _out in range(0, adpcm.data.length, step=2):

        #for (var _in = 0, _out = 0; _in < adpcm.data.length; _out += 2) {
        # Step 1 - get the delta value */
        if bufferStep:
            delta = inputBuffer & 0x0F
            _in += 1
        else:
            inputBuffer = adpcm.data.readInt8(_in)
            delta = (inputBuffer >> 4) & 0x0F
        bufferStep = not bufferStep

        # /* Step 2 - Find new index value (for later) */
        index += INDEX_TABLE[delta]
        if index < 0:
            index = 0
        if index > 88:
            index = 88


        # /* Step 3 - Separate sign and magnitude */
        sign = delta & 8
        delta = delta & 7

        # /* Step 4 - Compute difference and new predicted value */
        diff = step >> 3
        if (delta & 4) > 0:
            diff += step
        if (delta & 2) > 0:
            diff += step >> 1
        if (delta & 1) > 0:
            diff += step >> 2

        if sign > 0:
            valuePredicted -= diff
        else:
            valuePredicted += diff

        #/* Step 5 - clamp output value */
        if valuePredicted > 32767:
            valuePredicted = 32767
        elif valuePredicted < -32768:
            valuePredicted = -32768

        # /* Step 6 - Update step value */
        step = STEP_SIZE_TABLE[index]

        # /* Step 7 - Output value */
        pcm.writeInt16LE(valuePredicted,  _out)

    return pcm
