import wpilib

from robotmap import config

class LEDRing:
    def __init__(self):
        self.led = wpilib.solenoid.Solenoid(config["pcm"]["light_ring"])
    
    def setEnabled(self, is_enabled):
        """ Control the LED ring """
        self.led.set(is_enabled)