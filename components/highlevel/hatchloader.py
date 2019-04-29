import wpilib
from magicbot.state_machine import *
from robotmap import config
from common.logger import Logger

from components.lowlevel.drivebase.drivetrain import DriveTrain
from components.lowlevel.pneumatics.ledring import LEDRing
from components.lowlevel.pneumatics.finger import Finger

from networktables.util import ntproperty
from common.slewlimiter import MultipleSlewLimiter


class HatchLoader(StateMachine):
    """Autonomously pick up a hatch"""

    console: Logger
    drivetrain: DriveTrain
    led_ring: LEDRing
    finger: Finger

    target = ntproperty("/camera/target", (0.0, 0.0, 0.0))

    def __init__(self):
        super().__init__()
        self.xboxcontroller = wpilib.XboxController(config["xbox_controllers"]["driver"])
        self.rotation_smoother = MultipleSlewLimiter(0.2)

    def run(self):
        """ 
        Called by teleopPeriodic 

        Manages logging and starting the state machine
        """
        # Check if pressed for logging
        if self.xboxcontroller.getBumperPressed(wpilib.interfaces.GenericHID.Hand.kRight):
            self.console.log("Engaging hatch pickup")
        
        if self.xboxcontroller.getBumperReleased(wpilib.interfaces.GenericHID.Hand.kRight):
            self.console.log("Stopped hatch pickup")

        # Actually run the sequence
        if self.xboxcontroller.getBumper(wpilib.interfaces.GenericHID.Hand.kRight):
            self.engage()

    @state(first=True)
    def enableLED(self):
        self.led_ring.setEnabled(True)
        self.next_state('detectStation')
    
    @state()
    def detectStation(self):
        # Only continue if a target is found, else send haptic feedback
        if self.target[0]:
            self.console.log(f"Prelim rotation point set to {self.target[1]} degrees")
            self.drivetrain.rotation_controller.setSetpoint(self.drivetrain.gyro.getAngle() + self.target[1])
            self.next_state('turn')
        else:
            self.console.log("No vision target found")
            self.next_state('vibrate')

    @timed_state(duration=0.5, next_state='lowerFinger')
    def turn(self):
        self.drivetrain.rotateToSetpoint()
    
    @state()
    def lowerFinger(self):
        self.finger.setEnabled(False)
        self.next_state('initAlign')
    
    @state()
    def initAlign(self):
        self.drivetrain.forward_rotation_controller.setSetpoint(0)
        self.next_state('align')
    
    # def getStationPosition(self):
    #     # Only continue if a target is found, else send haptic feedback
    #     if self.target[0]:
    #         # return 0.8, self.rotation_smoother.Feed(self.target[1] * 0.1)
    #         if abs(self.target[1]) > config["loading_limits"]["min_angle"]:
    #             return config["loading_limits"]["tracking_speed"], self.target[1] * 0.1
    #         else:
    #             return config["loading_limits"]["ontrack_speed"], 0.0
    #     else:
    #         self.console.log("Lost track of loading station")
    #         return 0.0, 0.0

    @timed_state(duration=2.0, next_state='raiseFinger')
    def align(self):
        # speed, rotation = self.getStationPosition()
        if (self.target[2] > config["loading_limits"]["min_distance"] and self.target[0]) or not self.target[0]:
            # self.drivetrain.arcadeDrive(speed, rotation)
            self.drivetrain.driveAndRotateToSetpoint(self.target[1]*-1)
        else:
            self.next_state('raiseFinger')
    
    @state()
    def raiseFinger(self):
        self.finger.setEnabled(True)
        self.next_state('velcroPause')
    
    @timed_state(duration=0.3, next_state="pullBack")
    def velcroPause(self):
        pass
    
    @timed_state(duration=0.3, next_state='disableLED')
    def pullBack(self):
        self.drivetrain.arcadeDrive(-0.8, 0.0)

    @state()
    def disableLED(self):
        self.led_ring.setEnabled(False)

    @timed_state(duration=0.2, next_state='finish')
    def vibrate(self):
        self.xboxcontroller.setRumble(wpilib.interfaces.GenericHID.RumbleType.kLeftRumble, 0.5)
    
    @state()
    def finish(self):
        pass
    
    def done(self):
        super().done()
        self.led_ring.setEnabled(False)
        self.xboxcontroller.setRumble(wpilib.interfaces.GenericHID.RumbleType.kRightRumble, 0.0)
