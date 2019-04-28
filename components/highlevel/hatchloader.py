import wpilib
from magicbot.state_machine import *
from robotmap import config
from common.logger import Logger

from components.lowlevel.drivebase.drivetrain import DriveTrain
from components.lowlevel.pneumatics.ledring import LEDRing

from networktables.util import ntproperty

class HatchLoader(StateMachine):
    """Autonomously pick up a hatch"""

    console: Logger
    drivetrain: DriveTrain
    led_ring: LEDRing

    target = ntproperty("/camera/target", (0.0, 0.0, 0.0))

    def __init__(self):
        super().__init__()
        self.xboxcontroller = wpilib.XboxController(config["xbox_controllers"]["driver"])

    def run(self):
        """ 
        Called by teleopPeriodic 

        Manages logging and starting the state machine
        """
        # Check if pressed for logging
        if self.xboxcontroller.getBumperPressed(wpilib.interfaces.GenericHID.Hand.kRight):
            self.console.log("Engaging hatch pickup")
            self.first_run = True
        
        if self.xboxcontroller.getBumperReleased(wpilib.interfaces.GenericHID.Hand.kRight):
            self.console.log("Stopped hatch pickup")

        # Actually run the sequence
        if self.xboxcontroller.getBumper(wpilib.interfaces.GenericHID.Hand.kRight):
            self.engage()

    @state(first=True)
    def enableLED(self):
        self.led_ring.setEnabled(True)
        self.next_state('findStation')
    
    @state()
    def findStation(self):
        # Only continue if a target is found, else send haptic feedback
        if self.target[0]:
            self.console.log(f"Rotation point set to {self.target[1]} degrees")
            self.console.log(f"Shortest distance set to {self.target[2]} units")
            self.drivetrain.rotation_controller.setSetpoint(self.drivetrain.gyro.getAngle() + self.target[1])
            self.next_state('turn')
        else:
            self.console.log("No vision target found")
            self.next_state('vibrate')

    @timed_state(duration=1.0, next_state='disableLED')
    def turn(self):
        self.drivetrain.rotateToSetpoint()
    
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
