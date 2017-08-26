from collections import namedtuple
from struct import Struct
from binascii import b2a_hex

from uuids import *

ThingyChar = namedtuple('ThingyChar', ['uuid', 'common_name', 'conversion_func'])

c_type_double = Struct('< d').unpack

def unpack_float(struct, data):
    (integer, decimal) = struct.unpack(data)
    temperature = float(integer + decimal / 100)
    return temperature


def unpack_bool(data):
    val = Struct('< B').unpack(data)
    return bool(val[0])


def temp(data):
    s = Struct('< bB')  # < (little endian) B (unsigned int single byte)
    temperature = unpack_float(s, data)
    return temperature


def pressure(data):
    s = Struct('< iB')  # < (little endian) B (integer single byte)
    return unpack_float(s, data)


def humidity(data):
    s = Struct('< B')
    return s.unpack(data)


def extract_gas_data(data):
    """ Extract gas data from data string. """
    teptep = b2a_hex(data)
    eco2 = int(teptep[:2]) + (int(teptep[2:4]) << 8)
    tvoc = int(teptep[4:6]) + (int(teptep[6:8]) << 8)
    return eco2, tvoc


def _extract_tap_data(data):
    """ Extract tap data from data string. """
    teptep = b2a_hex(data)
    direction = teptep[0:2]
    count = teptep[2:4]
    return (direction, count)


temperature = ThingyChar(Nordic_UUID(E_TEMPERATURE_CHAR_UUID), 'temperature', temp)
pressure = ThingyChar(Nordic_UUID(E_PRESSURE_CHAR_UUID), 'pressure', pressure)
humidity = ThingyChar(Nordic_UUID(E_HUMIDITY_CHAR_UUID), 'humidity', humidity)
gas = ThingyChar(Nordic_UUID(E_GAS_CHAR_UUID), 'gas', extract_gas_data)
color = ThingyChar(Nordic_UUID(E_COLOR_CHAR_UUID), 'color', b2a_hex)
ui_button = ThingyChar(Nordic_UUID(UI_BUTTON_CHAR_UUID), 'ui_button', unpack_bool)
m_tap = ThingyChar(Nordic_UUID(M_TAP_CHAR_UUID), 'm_tap', _extract_tap_data)
m_orient = ThingyChar(Nordic_UUID(M_ORIENTATION_CHAR_UUID), 'm_orient', c_type_double)
m_quaternion = ThingyChar(Nordic_UUID(M_QUATERNION_CHAR_UUID), 'm_quaternion', b2a_hex)
m_stepcnt = ThingyChar(Nordic_UUID(M_STEP_COUNTER_UUID), 'm_stepcnt', b2a_hex)
m_rawdata = ThingyChar(Nordic_UUID(M_RAW_DATA_CHAR_UUID), 'm_rawdata', b2a_hex)
m_euler = ThingyChar(Nordic_UUID(M_EULER_CHAR_UUID), 'm_euler', b2a_hex)
m_rotation = ThingyChar(Nordic_UUID(M_ROTATION_MATRIX_CHAR_UUID), 'm_rotation', b2a_hex)
m_heading = ThingyChar(Nordic_UUID(M_HEAIDNG_CHAR_UUID), 'm_heading', b2a_hex)
m_gravity = ThingyChar(Nordic_UUID(M_GRAVITY_VECTOR_CHAR_UUID), 'm_gravity', b2a_hex)
s_speaker_status = ThingyChar(Nordic_UUID(S_SPEAKER_STATUS_CHAR_UUID), 's_speaker_status', b2a_hex)
s_microphone = ThingyChar(Nordic_UUID(S_MICROPHONE_CHAR_UUID), 's_microphone', b2a_hex)

thingy_chars = [
    temperature,
    pressure,
    humidity,
    gas,
    color,
    ui_button,
    m_tap,
    m_orient,
    m_quaternion,
    m_stepcnt,
    m_rawdata,
    m_euler,
    m_rotation,
    m_heading,
    m_gravity,
    s_speaker_status,
    s_microphone,
]

thingy_chars_map = {c.uuid: c for c in thingy_chars}
