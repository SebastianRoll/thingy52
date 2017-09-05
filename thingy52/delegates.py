from bluepy.btle import DefaultDelegate
import math

from thingy52.services import AudioSample


class ThingyCharDelegate(DefaultDelegate):
    def __init__(self, handles):
        DefaultDelegate.__init__(self)
        self.handles = handles

    def handleNotification(self, cHandle, data):
        thingy_char = self.handles[cHandle]
        name = thingy_char.common_name

        print(name)
        print(len(["0x%02x" % b for b in data]), "BYTES")
        print(["0x%02x" % b for b in data])

        val = thingy_char.conversion_func(data)
        print("{}: {}".format(name, val))


class Demo1Delegate(DefaultDelegate):
    def __init__(self, thingy52, handles):
        DefaultDelegate.__init__(self)
        self.thingy52 = thingy52
        self.handles = handles
        self._button_activated = False

    def handleNotification(self, cHandle, data):
        thingy_char = self.handles[cHandle]
        name = thingy_char.common_name
        val = thingy_char.conversion_func(data)

        if name is "button" and val is True:
            self.on_button_pressed()
        elif name is "heading":
            r = abs(int(255 * math.sin(math.radians(val))))
            g = 0
            b = abs(int(255 * math.cos(math.radians(val))))
            self.thingy52.ui.rgb_constant(r, g, b)

    def on_button_pressed(self):
        self._button_activated = not self._button_activated
        if self._button_activated:
            self.thingy52.sound.play_sample(AudioSample.COIN_1)
            self.thingy52.ui.rgb_constant(0, 255, 0)
        else:
            self.thingy52.sound.play_sample(AudioSample.HIT)
            self.thingy52.ui.rgb_constant(255, 0, 0)
        self.thingy52.motion.toggle_notifications("heading", enable=self._button_activated)
