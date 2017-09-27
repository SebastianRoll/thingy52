import atexit
from time import time

from demos.thingyaudio import RecordingDelegate, RecordingDelegate4, RecordingDelegate5
from thingy52.thingy52 import Thingy52

address = "E2:D9:D5:C6:30:26"
address = "DB:B7:18:34:E3:9E"

t = Thingy52(address)
# Set mic mode to ADPCM
t.sound.activate_speaker_stream(speaker_mode=1, mic_mode=1)

atexit.register(t.disconnect)
rec = RecordingDelegate5(t.handles)
t.setDelegate(rec)
atexit.register(rec.finish)
t.sound.toggle_notifications(characteristic="microphone", enable=True)
now = time()
while time() - now < 2:
    t.waitForNotifications(1.0)
