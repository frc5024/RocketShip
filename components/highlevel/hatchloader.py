import wpilib
from magicbot.state_machine import *
from robotmap import config
from common.logger import Logger

from components.lowlevel.drivebase.drivetrain import DriveTrain

class HatchLoader(StateMachine):
    """Autonomously pick up a hatch"""

    console: Logger
    drivetrain: DriveTrain

    def __init__(self):
        super().__init__()
        self.xboxcontroller = wpilib.XboxController(config["xbox_controllers"]["driver"])

    def run(self):
        # Check if pressed for logging
        if self.xboxcontroller.getBumperPressed(wpilib.interfaces.GenericHID.Hand.kRight):
            self.console.log("Engaging hatch pickup")
        
        if self.xboxcontroller.getBumperReleased(wpilib.interfaces.GenericHID.Hand.kRight):
            self.console.log("Stopped hatch pickup")

        # Actually run the sequence
        if self.xboxcontroller.getBumper(wpilib.interfaces.GenericHID.Hand.kRight):
            self.engage()   

    @timed_state(duration=0.5, first=True)
    def roughTurn(self):
        self.drivetrain.arcadeDrive(0.0, 0.5)
    
    @timed_state(duration=1.0)
    def 
