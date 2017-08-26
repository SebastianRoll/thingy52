# -*- coding: utf-8 -*-

"""Main module."""
import atexit
from bluepy.btle import Peripheral, UUID, DefaultDelegate

from thingy52.services import EnvironmentService, MotionService, UserInterfaceService, SoundService
from thingy52.uuids import Nordic_UUID, ENVIRONMENT_SERVICE_UUID, MOTION_SERVICE_UUID, USER_INTERFACE_SERVICE_UUID, \
    SOUND_SERVICE_UUID, BATTERY_SERVICE_UUID
from thingy52.characteristics import thingy_chars_map
from thingy52.delegates import ThingyCharDelegate

# Write this to CCCD to enable notifications
NOTIFY_ON = (1).to_bytes(2, byteorder='little')
NOTIFY_OFF = (0).to_bytes(2, byteorder='little')


class Thingy52(Peripheral):
    """
    Thingy:52 module. Instance the class and enable to get access to the Thingy:52 Sensors.
    The addr of your device has to be know, or can be found by using the hcitool command line
    tool, for example. Call "> sudo hcitool lescan" and your Thingy's address should show up.
    """

    handles = {}

    def __init__(self, addr):
        Peripheral.__init__(self, addr, addrType="random")

        # Thingy configuration service not implemented
        # self.battery = BatterySensor(self)
        self.environment = EnvironmentService(self)
        self.ui = UserInterfaceService(self)
        self.motion = MotionService(self)
        self.sound = SoundService(self)
        # DFU Service not implemented

    """
    @property
    def services(self):
        service_mapping = {
            Nordic_UUID(ENVIRONMENT_SERVICE_UUID): EnvironmentService,
        }
        peripheral_services = super(Thingy52, self).services
        thingy_services = [service_mapping.get(s.uuid, s) for s in peripheral_services]
        return thingy_services
    """

    def toggle_notify(self, char, enable):
        thingy_char = thingy_chars_map.get(char.uuid, None)
        self.handles[char.getHandle()] = thingy_char
        self.writeCharacteristic(char.getHandle() + 1, NOTIFY_ON if enable else NOTIFY_OFF)


def listen_to_thingy(address):
    t = Thingy52(address)
    atexit.register(t.disconnect)
    t.setDelegate(ThingyCharDelegate(t.handles))
    #t.motion.toggle_notifications(characteristic="rotation")
    t.environment.toggle_notifications()
    while True:
        t.waitForNotifications(1.0)
        print("Waiting...")


if __name__ == "__main__":
    # Initialisation
    # Peripheral mac adress
    address = "E2:D9:D5:C6:30:26"
    t = Thingy52(address)
    print("services:", t.services)
    try:

        t.setDelegate(ThingyCharDelegate(t.handles))

        # t.environment.enable_pressure()
        # t.environment.toggle_notifications()
        print(t.motion.list_notifications())
        t.motion.toggle_notifications(characteristic="rotation")
        # t.sound.toggle_notifications()
        # t.ui.toggle_notifications()
        # t.battery.toggle_notifications()

        # Main loop --------
        i = 0
        while i < 10:
            if t.waitForNotifications(1.0):
                # handleNotification() was called
                pass

            print("Waiting...")
            i += 1

            # Perhaps do something else here
    except Exception as e:
        raise
    finally:
        t.disconnect()
