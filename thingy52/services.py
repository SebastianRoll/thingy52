from thingy52.uuids import *
from thingy52.characteristics import *
from enum import Enum
from random import randint
import binascii

class Color(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PURPLE = 5
    CYAN = 6
    WHITE = 7


class LedMode(Enum):
    OFF = 0
    CONSTANT = 1
    BREATHE = 2
    ONE_SHOT = 3


class AudioSample(Enum):
    COIN_1 = 0
    COIN_2 = 1
    EXPLOSION_1 = 2
    EXPLOSION_2 = 3
    HIT = 4
    PICKUP_1 = 5
    PICKUP_2 = 6
    SHOOT_1 = 7
    SHOOT_2 = 8


class ThingyService(object):
    """
    Thing service base class
    """

    service_uid = None

    notify_chars = []

    write_chars = []

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

    """write_chars = [
        ThingyChar(Nordic_UUID(UI_LED_CHAR_UUID), 'led', unpack_bool),
    ]"""

    def rgb_read(self):
        char_uuid = self.chars_map["led"].uuid
        char = self.service.getCharacteristics(forUUID=char_uuid)[0]
        handle = char.getHandle()
        data = self.peripheral.readCharacteristic(handle)
        (mode, r, g, b, _) = Struct('> 5B').unpack(data)
        return data[0]

    def rgb_off(self):
        char_uuid = self.chars_map["led"].uuid
        char = self.service.getCharacteristics(forUUID=char_uuid)[0]
        s = Struct('> B')
        led_command = s.pack(LedMode.OFF.value)
        char.write(led_command, True)

    def rgb_constant(self, r, g, b):
        char_uuid = self.chars_map["led"].uuid
        char = self.service.getCharacteristics(forUUID=char_uuid)[0]

        s = Struct('> 4B')
        values = (LedMode.CONSTANT.value, r, g, b)
        led_command = s.pack(*values)
        char.write(led_command, True)

    def rgb_breathe(self, color=Color.RED, intensity=100, delay=1):
        char_uuid = self.chars_map["led"].uuid
        char = self.service.getCharacteristics(forUUID=char_uuid)[0]

        s = Struct('> 3BH')
        values = (LedMode.BREATHE.value, color.value, intensity, delay)
        led_command = s.pack(*values)
        char.write(led_command, True)

    def rgb_one_shot(self, color=Color.RED, intensity=100):
        char_uuid = self.chars_map["led"].uuid
        char = self.service.getCharacteristics(forUUID=char_uuid)[0]

        s = Struct('> 3B')
        values = (LedMode.ONE_SHOT.value, color.value, intensity)
        led_command = s.pack(*values)
        char.write(led_command, True)


class SoundService(ThingyService):
    """
    Environment service module. Instance the class and enable to get access to the Environment interface.
    """
    service_uid = SOUND_SERVICE_UUID

    notify_chars = [
        ThingyChar(Nordic_UUID(S_SPEAKER_STATUS_CHAR_UUID), 'speaker_status', b2a_hex),
        ThingyChar(Nordic_UUID(S_CONFIG_CHAR_UUID), 'config_characteristic', b2a_hex),
        ThingyChar(Nordic_UUID(S_SPEAKER_DATA_CHAR_UUID), 'speaker_characteristic', b2a_hex),
        ThingyChar(Nordic_UUID(S_MICROPHONE_CHAR_UUID), 'microphone', b2a_hex),
    ]

    def activate_speaker_stream(self, speaker_mode=2, mic_mode=1):
        char_uuid_config = self.chars_map["config_characteristic"].uuid
        char_config = self.service.getCharacteristics(forUUID=char_uuid_config)[0]
        bytes = Struct('> 2B').pack(speaker_mode, mic_mode)
        char_config.write(bytes, True)

    def stream_speaker(self):
        char_uuid = self.chars_map["speaker_characteristic"].uuid
        char = self.service.getCharacteristics(forUUID=char_uuid)[0]
        s = Struct('> 120B')
        m = (randint(0, 100) for i in range(120))
        command = s.pack(*m)
        print("packed")
        char.write(command, True)
        print("written")

    def stream_frequency(self, frequency, duration, volume):
        char_uuid = self.chars_map["speaker_characteristic"].uuid
        char = self.service.getCharacteristics(forUUID=char_uuid)[0]
        s = Struct('> HHB')
        command = s.pack(frequency, duration, volume)
        char.write(command, True)

    def play_sample(self, sample=AudioSample.SHOOT_1):
        char_uuid_config = self.chars_map["config_characteristic"].uuid
        char_config = self.service.getCharacteristics(forUUID=char_uuid_config)[0]
        bytes = Struct('> 2B').pack(3, 1)
        char_config.write(bytes, True)

        char_uuid = self.chars_map["speaker_characteristic"].uuid
        char = self.service.getCharacteristics(forUUID=char_uuid)[0]

        s = Struct('> B')
        command = s.pack(sample.value)
        char.write(command, True)
