
import sys
import time
import os
import numpy as np
from MACRO import *
from CameraMotors import *


class CameraHandler:

    def __init__(self, bus):
        self.camera_motor_driver = Focuser(bus)

    def setFocusValue(self, val):
        self.camera_motor_driver.set(Focuser.OPT_FOCUS, val)
        print('focus val: ', val)
    
    def setZoomValue(self, val):
        self.camera_motor_driver.set(Focuser.OPT_ZOOM, val)
    
    def setCameraAGC_on_off(self, isOn):
        pass

    def setCameraAgcValue(self, val):
        pass