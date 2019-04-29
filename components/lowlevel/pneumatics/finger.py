import wpilib

from robotmap import config

class Finger:
    def __init__(self):
        self.solenoid = wpilib.solenoid.Solenoid(config["pcm"]["can_id"], config["pcm"]["finger"])
        self.solenoid.set(True)
    
    def setEnabled(self, is_enabled):
        """ Control the LED ring """
        self.solenoid.set(is_enabled)