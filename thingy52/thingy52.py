# -*- coding: utf-8 -*-

"""Main module."""
from bluepy.btle import Peripheral

from thingy52.services import EnvironmentService, MotionService, UserInterfaceService, SoundService
from thingy52.characteristics import thingy_chars_map

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

        # self.battery = BatterySensor(self)
        self.environment = EnvironmentService(self)
        self.ui = UserInterfaceService(self)
        self.motion = MotionService(self)
        self.sound = SoundService(self)

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

