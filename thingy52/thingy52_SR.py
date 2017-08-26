# -*- coding: utf-8 -*-

"""Main module."""

from bluepy import btle
import struct

# Audun på Applications team - MakerFaire
# anbefaler 'getting started with bluetooth low energy'. Medforfatter Carles Cufi jobber på Nordic.

# service uuid(s) for your peripheral advertises
TCS_UUID = 'ef6801009b3549339b1052ffa9740042'
# characteristic to notify for enabling notifications
TES_UUID = 'ef6802009b3549339b1052ffa9740042'

# Environment
TES_GAS_UUID = 'ef6802049b3549339b1052ffa9740042'
TES_TEMP_UUID = 'ef6802019b3549339b1052ffa9740042'
TES_PRESS_UUID = 'ef6802029b3549339b1052ffa9740042'

# Write this to CCCD to enable notifications
enable = (1).to_bytes(2, byteorder='little')
# Peripheral mac adress
address = "E2:D9:D5:C6:30:26"


def unpack_float(struct, data):
    (integer, decimal) = struct.unpack(data)
    temperature = float(integer + decimal / 100)
    return temperature


def temp(data):
    s = struct.Struct('< bB')  # < (little endian) B (unsigned int single byte)
    temperature = unpack_float(s, data)
    return temperature


def pressure(data):
    s = struct.Struct('< iB')  # < (little endian) B (integer single byte)
    return unpack_float(s, data)


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        print("handling", cHandle, data)

        print(["0x%02x" % b for b in data])
        print(pressure(data))
        # ... perhaps check cHandle
        # ... process 'data'


# Initialisation
p = btle.Peripheral(address, "random")

try:

    p.setDelegate(MyDelegate())

    # option 1: get characheristics notifications for service
    # svc = p.getServiceByUUID( TES_UUID )
    # cs = svc.getCharacteristics()
    # print([c.uuid.getCommonName() for c in cs])
    # c = cs[0]

    # option 2: enable notify directly on characteristic
    c = p.getCharacteristics(uuid=TES_PRESS_UUID)[0]
    print(c.uuid.getCommonName())
    # tempEnabler[0].write(enable)

    # print("Device name: {}".format(name.read()))
    # [c.write(enable) for c in cs]
    p.writeCharacteristic(c.getHandle() + 1, enable)  # +1 writes to cccd instead of main value

    # Main loop --------
    i = 0
    while i < 7:
        if p.waitForNotifications(1.0):
            # handleNotification() was called
            print("Notified!")
            continue

        print("Waiting...")
        i += 1

        # Perhaps do something else here
except Exception as e:
    print(e)
finally:
    p.disconnect()
