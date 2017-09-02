from bluepy.btle import DefaultDelegate

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

        if name is "button" and val is True :
            self.button_pressed()

        print("{}: {}".format(name, val))

    def button_pressed(self):
        self._button_activated = not self._button_activated
        self.thingy52.environment.toggle_notifications("temperature", enable=self._button_activated)


