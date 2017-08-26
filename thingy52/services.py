from bluepy.btle import Service
from uuids import *
from characteristics import *

# Write this to CCCD to enable notifications
ENABLE = (1).to_bytes(2, byteorder='little')
DISABLE = (0).to_bytes(2, byteorder='little')

class ThingyService(object):
    def __init__(self, peripheral, uuid):
        self.peripheral = peripheral
        self.uuid = Nordic_UUID(uuid)
        self.service = self.peripheral.getServiceByUUID(self.uuid)

    def toggle_notifications(self, enable=True, characteristic=None):
        """
        Switches notifications on or off.
        :param enable: notifications on or off
        :param characteristic:
        :return:
        """
        chars = []
        if characteristic:
            pass
        else:
            # get all characteristics for service
            for c in self.service.getCharacteristics():
                self.peripheral.register_handle(c)
                chars.append(c)

        for char in chars:
            self.peripheral.writeCharacteristic(char.getHandle() + 1, ENABLE if enable else DISABLE)

class EnvironmentService(ThingyService):
    """
    Environment service module. Instance the class and enable to get access to the Environment interface.
    """

    serviceUUID =           Nordic_UUID(ENVIRONMENT_SERVICE_UUID)
    temperature_char_uuid = Nordic_UUID(E_TEMPERATURE_CHAR_UUID)
    pressure_char_uuid =    Nordic_UUID(E_PRESSURE_CHAR_UUID)
    humidity_char_uuid =    Nordic_UUID(E_HUMIDITY_CHAR_UUID)
    gas_char_uuid =         Nordic_UUID(E_GAS_CHAR_UUID)
    color_char_uuid =       Nordic_UUID(E_COLOR_CHAR_UUID)
    config_char_uuid =      Nordic_UUID(E_CONFIG_CHAR_UUID)

