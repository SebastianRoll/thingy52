import atexit
from time import time

from demos.thingyaudio import RecordingDelegate1, RecordingDelegate2, RecordingDelegate3, RecordingDelegate4, RecordingDelegate5
from thingy52.thingy52 import Thingy52

# use your thingy's MAC address printed on the device.
THINGY_ADDRESS = "EF:D5:24:2C:FE:73"
RECORD_DURATION_SECONDS = 10
RECORDING_DELEGATE = RecordingDelegate1

t = Thingy52(THINGY_ADDRESS)
# Set mic mode to ADPCM
t.sound.activate_speaker_stream(speaker_mode=1, mic_mode=1)

atexit.register(t.disconnect)
rec = RECORDING_DELEGATE(t.handles)
t.setDelegate(rec)
atexit.register(rec.finish)
t.sound.toggle_notifications(characteristic="microphone", enable=True)

# Record for specified duration. Audio file is written
now = time()
while time() - now < RECORD_DURATION_SECONDS:
    t.waitForNotifications(1.0)
