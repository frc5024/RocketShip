import wpilib
from magicbot.state_machine import *
from robotmap import config
from common.logger import Logger

from components.lowlevel.drivebase.drivetrain import DriveTrain
from components.lowlevel.pneumatics.ledring import LEDRing

class HatchLoader(StateMachine):
    """Autonomously pick up a hatch"""

    console: Logger
    drivetrain: DriveTrain
    led_ring: LEDRing

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
        
        if self.xboxcontroller.getBumperReleased(wpilib.interfaces.GenericHID.Hand.kRight):
            self.console.log("Stopped hatch pickup")

        # Actually run the sequence
        if self.xboxcontroller.getBumper(wpilib.interfaces.GenericHID.Hand.kRight):
            self.engage()   

    @state(first=True)
    def enableLED(self):
        self.led_ring.setEnabled(True)
        self.next_state('getRoughAngle')
    
    @state()
    def getRoughAngle(self):
        self.drivetrain.rotation_controller.setSetpoint(0)
        self.next_state('roughTurn')

    @timed_state(duration=0.5, next_state='disableLED')
    def roughTurn(self):
        self.drivetrain.rotateToSetpoint()
    
    @state()
    def disableLED(self):
        self.led_ring.setEnabled(False)
    
    def done(self):
        super().done()
        self.led_ring.setEnabled(False)
