import wpilib

from robotmap import config
from components.lowlevel.drivebase.drivetrain import DriveTrain

from common.slewlimiter import SlewLimiter

def limitTrigger(x):
    return x if x>=0 else 0

class TriggerDrive:
    """ High level component that reads from an xbox controller and commands the drivetrain"""
    drivetrain: DriveTrain

    def __init__(self):
        self.xboxcontroller = wpilib.XboxController(config["xbox_controllers"]["driver"])
        self.slew_limiter = SlewLimiter(0.1)
    
    def execute(self):
        """Called on every loop of the 'schedular'"""
        speed = 0
        rotation = 0

        speed += limitTrigger(self.xboxcontroller.getTriggerAxis(wpilib.interfaces.GenericHID.Hand.kRight))
        speed -= limitTrigger(self.xboxcontroller.getTriggerAxis(wpilib.interfaces.GenericHID.Hand.kLeft))

        speed = self.slew_limiter.Feed(speed)
        
        rotation = self.xboxcontroller.getX(wpilib.interfaces.GenericHID.Hand.kLeft)
        rotation = 0 if abs(rotation) < 0.1 else rotation

        self.drivetrain.arcadeDrive(speed, rotation)