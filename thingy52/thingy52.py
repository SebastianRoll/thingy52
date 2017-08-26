# -*- coding: utf-8 -*-

"""Main module."""
from services import ThingyService, EnvironmentService
from uuids import Nordic_UUID, ENVIRONMENT_SERVICE_UUID, MOTION_SERVICE_UUID, USER_INTERFACE_SERVICE_UUID, SOUND_SERVICE_UUID, BATTERY_SERVICE_UUID
from bluepy.btle import Peripheral, UUID, DefaultDelegate
from characteristics import thingy_chars_map
from delegates import ThingyCharDelegate

service_mapping = {
    Nordic_UUID(ENVIRONMENT_SERVICE_UUID): EnvironmentService,
}

# Audun på Applications team - MakerFaire
# anbefaler 'getting started with bluetooth low energy'. Medforfatter Carles Cufi jobber på Nordic.

# service uuid(s) for your peripheral advertises
TCS_UUID = 'ef6801009b3549339b1052ffa9740042'
# characteristic to notify for enabling notifications
TES_UUID = 'ef6802009b3549339b1052ffa9740042'

# Peripheral mac adress
address = "E2:D9:D5:C6:30:26"


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
        # self.environment = EnvironmentService(self)
        # self.ui = UserInterfaceService(self)
        # self.motion = MotionService(self)
        # self.sound = SoundService(self)
        # DFU Service not implemented


        #self.battery = ThingyService(self, BATTERY_SERVICE_UUID)
        self.ui = ThingyService(self, USER_INTERFACE_SERVICE_UUID)
        self.environment = ThingyService(self, ENVIRONMENT_SERVICE_UUID)
        self.motion = ThingyService( self, MOTION_SERVICE_UUID)
        self.sound = ThingyService(self, SOUND_SERVICE_UUID)


    @property
    def services(self):
        peripheral_services = super(Thingy52, self).services
        thingy_services = [service_mapping.get(s.uuid, s) for s in peripheral_services]
        return thingy_services

    def register_handle(self, char):
        thingy_char = thingy_chars_map.get(char.uuid, None)
        self.handles[char.getHandle()] = thingy_char



# Initialisation
# t = Peripheral(address, "random")
t = Thingy52(address)
print("services:", t.services)
from thingy52_pr import MyDelegate as Delegate
try:

    t.setDelegate(ThingyCharDelegate(t.handles))

    # option 1: get characheristics notifications for service
    # svc = t.getServiceByUUID( TES_UUID )
    # cs = svc.getCharacteristics()
    # print([c.uuid.getCommonName() for c in cs])
    # c = cs[0]

    # option 2: enable notify directly on characteristic
    # t.environment.enable_pressure()
    #t.environment.toggle_notifications()
    t.motion.toggle_notifications()
    #t.sound.toggle_notifications()
    #t.ui.toggle_notifications()
    #t.battery.toggle_notifications()
    # c = t.getCharacteristics(uuid=TES_PRESS_UUID)[0]
    # print(c.uuid.getCommonName())
    # tempEnabler[0].write(enable)

    # print("Device name: {}".format(name.read()))
    # [c.write(enable) for c in cs]

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
    t.disconnect()
    raise
