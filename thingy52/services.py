from thingy52.uuids import *
from thingy52.characteristics import *


class ThingyService(object):
    """
    Thing service base class
    """

    service_uid = None

    notify_chars = []

    def __init__(self, peripheral):
        self.peripheral = peripheral
        self.uuid = Nordic_UUID(self.service_uid)
        self.service = self.peripheral.getServiceByUUID(self.uuid)

        self.chars_map = {c.common_name: c for c in self.notify_chars}

    def list_notifications(self):
        return self.chars_map.keys()

    def toggle_notifications(self, characteristic=None, enable=True):
        """
        Switches notifications on or off.
        :param enable: notifications on or off
        :param characteristic:
        :return:
        """
        if characteristic:
            char_uuid = self.chars_map[characteristic].uuid
            char = self.service.getCharacteristics(forUUID=char_uuid)[0]
            self.peripheral.toggle_notify(char, enable)
        else:
            # get all characteristics for service
            for c in self.service.getCharacteristics():
                self.peripheral.toggle_notify(c, enable)


class EnvironmentService(ThingyService):
    """
    Environment service module. Instance the class and enable to get access to the Environment interface.
    """
    service_uid = ENVIRONMENT_SERVICE_UUID

    notify_chars = [
        ThingyChar(Nordic_UUID(E_TEMPERATURE_CHAR_UUID), 'temperature', temp),
        ThingyChar(Nordic_UUID(E_PRESSURE_CHAR_UUID), 'pressure', pressure),
        ThingyChar(Nordic_UUID(E_HUMIDITY_CHAR_UUID), 'humidity', humidity),
        ThingyChar(Nordic_UUID(E_GAS_CHAR_UUID), 'gas', extract_gas_data),
        ThingyChar(Nordic_UUID(E_COLOR_CHAR_UUID), 'color', b2a_hex),
        ThingyChar(Nordic_UUID(E_CONFIG_CHAR_UUID), 'config', b2a_hex),
    ]


class MotionService(ThingyService):
    """
    Environment service module. Instance the class and enable to get access to the Environment interface.
    """
    service_uid = MOTION_SERVICE_UUID

    notify_chars = [
        ThingyChar(Nordic_UUID(M_TAP_CHAR_UUID), 'tap', extract_tap_data),
        ThingyChar(Nordic_UUID(M_ORIENTATION_CHAR_UUID), 'orientation', c_type_double),
        ThingyChar(Nordic_UUID(M_QUATERNION_CHAR_UUID), 'quaternion', b2a_hex),
        ThingyChar(Nordic_UUID(M_STEP_COUNTER_UUID), 'step_cont', b2a_hex),
        ThingyChar(Nordic_UUID(M_RAW_DATA_CHAR_UUID), 'rawdata', b2a_hex),
        ThingyChar(Nordic_UUID(M_EULER_CHAR_UUID), 'euler', b2a_hex),
        ThingyChar(Nordic_UUID(M_ROTATION_MATRIX_CHAR_UUID), 'rotation', b2a_hex),
        ThingyChar(Nordic_UUID(M_HEAIDNG_CHAR_UUID), 'heading', b2a_hex),
        ThingyChar(Nordic_UUID(M_GRAVITY_VECTOR_CHAR_UUID), 'gravity', b2a_hex),
    ]


class UserInterfaceService(ThingyService):
    """
    Environment service module. Instance the class and enable to get access to the Environment interface.
    """
    service_uid = USER_INTERFACE_SERVICE_UUID

    notify_chars = [
        ThingyChar(Nordic_UUID(UI_BUTTON_CHAR_UUID), 'button', unpack_bool),
        ThingyChar(Nordic_UUID(UI_LED_CHAR_UUID), 'led', unpack_bool),
    ]


class SoundService(ThingyService):
    """
    Environment service module. Instance the class and enable to get access to the Environment interface.
    """
    service_uid = SOUND_SERVICE_UUID

    notify_chars = [
        ThingyChar(Nordic_UUID(S_SPEAKER_STATUS_CHAR_UUID), 'speaker_status', b2a_hex),
        ThingyChar(Nordic_UUID(S_MICROPHONE_CHAR_UUID), 'microphone', b2a_hex),
    ]
