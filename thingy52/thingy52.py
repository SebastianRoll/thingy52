# -*- coding: utf-8 -*-

"""Main module."""
from bluepy.btle import Peripheral
import struct
from thingy52.services import EnvironmentService, MotionService, UserInterfaceService, SoundService
from thingy52.characteristics import thingy_chars_map
from thingy52.uuids import CCCD_UUID
# Write this to CCCD to enable notifications
# NOTIFY_ON = b"\x01\x00"
# NOTIFY_OFF =b"\x00\x00"
NOTIFY_ON = struct.pack('<bb', 0x01, 0x00)
NOTIFY_OFF = struct.pack('<bb', 0x00, 0x00)
# NOTIFY_OFF = (0).to_bytes(2, byteorder='little')
# NOTIFY_OFF = (0).to_bytes(2, byteorder='little')
# NOTIFY_ON = (1).to_bytes(2, byteorder='big')
# NOTIFY_OFF = (0).to_bytes(2, byteorder='big')


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
        # char.write(NOTIFY_ON)
        thingy_char = thingy_chars_map.get(char.uuid, None)


        ccds = char.getDescriptors(forUUID=CCCD_UUID)
        print(thingy_char.common_name, ccds)
        try:
            temperature_cccd = ccds[0]
        except IndexError:
            return
        temperature_cccd.write(b"\x01\x00" if enable else b"\x00\x00", True)
        self.handles[char.getHandle()] = thingy_char


        # temperature_char = self.environment_service.getCharacteristics(thingy_char.uuid)[0]
        # temperature_cccd = thingy_char.getDescriptors(forUUID=CCCD_UUID)[0]
        # self.handles[char.getHandle()] = thingy_char
        # self.writeCharacteristic(temperature_cccd.handle, NOTIFY_ON if enable else NOTIFY_OFF, True)
        # self.writeCharacteristic(temperature_cccd.getHandle(), NOTIFY_ON if enable else NOTIFY_OFF)
        # self.writeCharacteristic(char.getHandle() + 15, NOTIFY_ON if enable else NOTIFY_OFF)
        # for i in range(100):
        #     self.writeCharacteristic(char.getHandle() + i, struct.pack('<bb', 0x01, 0x00) if enable else NOTIFY_OFF)

    def write(self, char, command):
        # Todo: Exception handling for char.uuid not found in dict
        thingy_char = thingy_chars_map[char.uuid]
        print(thingy_char)
        self.handles[char.getHandle()] = thingy_char
        self.writeCharacteristic(char.getHandle(), command)
