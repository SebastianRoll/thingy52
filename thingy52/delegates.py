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

        val = thingy_char.conversion_func(data)
        print("{}: {}".format(name, val))

