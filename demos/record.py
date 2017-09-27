import atexit
from time import time

from demos.thingyaudio import RecordingDelegate4, RecordingDelegate5
from thingy52.thingy52 import Thingy52

address = "E2:D9:D5:C6:30:26"

t = Thingy52(address)
# Set mic mode to ADPCM
t.sound.activate_speaker_stream(1, 1)

atexit.register(t.disconnect)
rec = RecordingDelegate5(t.handles)
t.setDelegate(rec)
atexit.register(rec.finish)
t.sound.toggle_notifications(characteristic="microphone", enable=True)
now = time()
while time() - now < 2:
    t.waitForNotifications(1.0)
