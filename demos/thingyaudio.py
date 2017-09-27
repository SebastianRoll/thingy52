"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""
from bluepy.btle import DefaultDelegate
import pyaudio
import wave
import audioop
from struct import Struct
import struct
import numpy as np
import scipy.signal as signal

CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 1
# https://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.rds%2Fdita%2Frds%2Fdesigns%2Fthingy%2Fintro%2Fkey_features.html
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

SILENCE = chr(0)*2

# Intel ADPCM step variation table
INDEX_TABLE = [-1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8, ]

# ADPCM step size table
STEP_SIZE_TABLE = [7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45, 50, 55, 60, 66, 73, 80,
                   88, 97, 107, 118, 130, 143, 157, 173, 190, 209,
                   230, 253, 279, 307, 337, 371, 408, 449, 494, 544, 598, 658, 724, 796, 876, 963, 1060, 1166, 1282,
                   1411, 1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
                   5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899, 15289, 16818, 18500, 20350, 22385,
                   24623, 27086, 29794, 32767]


class RecordingDelegate(DefaultDelegate):
    def __init__(self, handles):
        DefaultDelegate.__init__(self)
        self.handles = handles

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  output=True,
                                  frames_per_buffer=CHUNK)

        self.stream.start_stream()
        print("* recording")

        self.frames = []

        self.state = None
        self.numframes = 0

    def handleNotification(self, cHandle, data):
        pcm, self.state = audioop.adpcm2lin(data, 2, self.state)
        # self.frames.append(pcm)
        self.stream.write(pcm)
        self.numframes += 1

    def finish(self):
        print("* done recording", self.numframes, "frames")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()


class RecordingDelegate3(DefaultDelegate):
    def __init__(self, handles):
        DefaultDelegate.__init__(self)
        self.handles = handles
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.state = None

        self.adpcmfile = open("recording.adpcm", "wb")

        print("* recording")
        self.numframes = 0

    def handleNotification(self, cHandle, data):
        self.adpcmfile.write(data)
        self.numframes += 1

    def finish(self):
        self.adpcmfile.close()
        print("* done recording", self.numframes, "frames")

        with open('recording.adpcm', 'rb') as f:
            adpcm = f.read()
        pcm, _ = audioop.adpcm2lin(adpcm, 2, None)
        # data length is 20 bytes, pcm length is 80 bytes
        self.wavfile = wave.open("out2" + '.wav', 'wb')
        self.wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        self.wavfile.close()

# b,a=signal.iirdesign(0.03,0.07,5,40)
# fulldata = np.array([])
# def callback(in_data, frame_count, time_info, flag):
#     global audiodatas
#     print(audiodatas)
#     if len(audiodatas) == 0:
#         return (SILENCE, pyaudio.paContinue)
#     global b, a, fulldata  # global variables for filter coefficients and array
#     audio_data = np.fromstring(audiodatas, dtype=np.float32)
#     # do whatever with data, in my case I want to hear my data filtered in realtime
#     audio_data = signal.filtfilt(b, a, audio_data, padlen=200).astype(np.float32).tostring()
#     fulldata = np.append(fulldata, audio_data)  # saves filtered data in an array
#     return (audio_data, pyaudio.paContinue)
# audiodatas = b'00x'
class RecordingDelegate4(DefaultDelegate):
    def __init__(self, handles):
        DefaultDelegate.__init__(self)
        self.handles = handles
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.state = None

        self.wavfile = wave.open("out2" + '.wav', 'wb')
        self.wavfile.setnchannels(CHANNELS)
        self.wavfile.setsampwidth(self.p.get_sample_size(FORMAT))
        self.wavfile.setframerate(RATE)

        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1, rate=16000, frames_per_buffer=20,
            output=True) #, stream_callback=callback)#, start=False)
        self.stream.start_stream()

        self.numframes = 0
        print("recording")

    def handleNotification(self, cHandle, data):
        # global audiodatas
        # thingy_char = self.handles[cHandle]
        # data = thingy_char.conversion_func(data)
        pcm = adpcm_decode(data)
        # audiodatas = pcm
        self.stream.write(pcm)
        # free = self.stream.get_write_available()  # How much space is left in the buffer?
        # if free > CHUNK:  # Is there a lot of space in the buffer?
        #     tofill = free - CHUNK
        #     self.stream.write(SILENCE * tofill)  # Fill it with silence

        # self.wavfile.writeframes(pcm)
        self.numframes += 1

    def finish(self):
        print("* done recording", self.numframes, "frames")

        self.stream.stop_stream()
        self.stream.close()

        self.p.terminate()
        self.wavfile.close()


class RecordingDelegate5(DefaultDelegate):
    def __init__(self, handles):
        DefaultDelegate.__init__(self)
        self.handles = handles
        self.p = pyaudio.PyAudio()
        self.wavfile = wave.open("out4" + '.wav', 'wb')
        self.wavfile.setnchannels(CHANNELS)
        self.wavfile.setsampwidth(self.p.get_sample_size(FORMAT))
        self.wavfile.setframerate(int(RATE/60))
        # self.wavfile.setnframes(256)
        # self.wavfile.setframerate(RATE)
        self.numframes = 0
        print("* recording")
        self.state = None

    def handleNotification(self, cHandle, data):
        pcm = adpcm_decode(data)
        pcm2, self.state = audioop.adpcm2lin(data, 2, self.state)

        # p1 = Struct('< 40h').unpack(pcm)
        # p2 = Struct('< 40h').unpack(pcm2)
        self.wavfile.writeframes(pcm2)
        self.numframes += 1

    def finish(self):
        print("* done recording", self.numframes, "frames")
        self.wavfile.close()


if __name__ == "__main__":
    CHUNK = 256
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
    """
    Attempt to replicate node implementation from
    https://github.com/NordicSemiconductor/Nordic-Thingy52-Nodejs/blob/master/examples/microphone.js
    :param adpcm: bytes array
    :return: pcm
    """
    s = Struct('< hb17s')
    (valuePredicted, index, data) = s.unpack(adpcm)

    # Allocate output buffer
    # pcm = new Buffer(adpcm.data.length*4)
    # pcm = []*len(adpcm)*4
    pcm = b''
    # The first 2 bytes of ADPCM frame are the predicted value
    # valuePredicted = adpcm.header.readInt16BE(0)
    # The 3rd byte is the index value
    # index = adpcm.header.readInt8(2)

    if index < 0:
        index = 0
    if index > 88:
        index = 88

    # diff #/* Current change to valuePredicted */
    bufferStep = False
    inputBuffer = 0
    delta = 0
    sign = 0
    step = STEP_SIZE_TABLE[index]
    _in = 0
    _out = 0
    # for (var _in = 0, _out = 0; _in < adpcm.data.length; _out += 2) {
    # for _out in range(0, adpcm.data.length, step=2):
    # for _out in range(0, len(data), 2):
    while _in < len(adpcm):

        # Step 1 - get the delta value */
        if bufferStep:
            delta = inputBuffer & 0x0F
            _in += 1
        else:
            # inputBuffer = adpcm.data.readInt8(_in)
            inputBuffer = adpcm[_in]
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

        # /* Step 5 - clamp output value */
        if valuePredicted > 32767:
            valuePredicted = 32767
        elif valuePredicted < -32768:
            valuePredicted = -32768

        # /* Step 6 - Update step value */
        step = STEP_SIZE_TABLE[index]

        # /* Step 7 - Output value */
        # pcm.writeInt16LE(valuePredicted,  _out)
        pcm += struct.pack('< h', valuePredicted)

        _out += 2

    return pcm
