from thingy52.thingy52 import Thingy52
from thingy52.delegates import DefaultDelegate

import atexit
import socket
from time import sleep, time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

t = Thingy52("E2:D9:D5:C6:30:26")

# minimum delta sum of pan+tilt angles for new request
MANHATTAN_ANGLE_THRESHOLD = 1
# minimum elapsed time between requests
MIN_ELAPSED_TIME = 0.05
URL = "192.168.1.109"
PORT = 6789

class PicamDelegate(DefaultDelegate):
    def __init__(self, thingy52, handles):
        DefaultDelegate.__init__(self)
        self.thingy52 = thingy52
        self.handles = handles

        self.yaw = 0
        self.roll = 0
        self.pitch = 0
        self.min_elapsed_time = MIN_ELAPSED_TIME

        self.time = time()
        self.url = URL
        self.port = PORT
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.tilt_url = 'tilt:{}'
        self.pan_url = 'pan:{}'
        self.led_url = 'led:{}'
        self._button_activated = False

    def handleNotification(self, cHandle, data):

        thingy_char = self.handles[cHandle]
        name = thingy_char.common_name
        val = thingy_char.conversion_func(data)
        logging.debug("{}: {}".format(name, val))

        if name is "button" and val is True:
            self.on_button_pressed()

        tick = time()
        if tick - self.time < self.min_elapsed_time:
            return
        else:
            self.time = tick

        if name == "euler":
            # roll: [-180, 180]
            # pitch: [-90, 90]
            # yaw: [-180, 180]

            (roll, pitch, yaw) = val

            logging.debug("roll {} - pitch {} - yaw {}".format(roll, pitch, yaw))

            if abs(roll - self.roll) + abs(yaw - self.yaw) > 1:
                self.roll = roll
                tilt = roll

                self.tilt_camera(tilt)

                self.yaw = yaw

                self.pan_camera(yaw, roll)

    def pan_camera(self, yaw, roll):
        if yaw < 0 and roll > 90:
            pan = 180 - (180 + yaw)
        elif yaw > 0 and roll < 90:
            pan = 180 - yaw
        else:
            self.thingy52.ui.rgb_constant(255, 0, 0)
            return
        self.thingy52.ui.rgb_constant(0, 0, 255)
        try:
            req_yaw = self.pan_url.format(int(pan))
            self.clientSock.sendto(str.encode(req_yaw), (self.url, self.port))
        except Exception as e:
            logger.warning(e)

    def tilt_camera(self, tilt):
        try:
            req_roll = self.tilt_url.format(int(tilt))
            self.clientSock.sendto(str.encode(req_roll), (self.url, self.port))
        except Exception as e:
            logger.warning(e)

    def on_button_pressed(self):
        self._button_activated = not self._button_activated
        brightness = 255 if self._button_activated else 0
        try:
            self.clientSock.sendto(str.encode(self.led_url.format(brightness)), (self.url, self.port))
        except Exception as e:
            logger.warning(e)


atexit.register(t.disconnect)
t.setDelegate(PicamDelegate(t, t.handles))

# button toggles LED
t.ui.toggle_notifications(characteristic="button", enable=True)

t.motion.toggle_notifications(characteristic="euler", enable=True)
while True:
    t.waitForNotifications(0.1)
