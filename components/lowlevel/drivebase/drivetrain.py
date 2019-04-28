import wpilib
import ctre
from wpilib.drive import DifferentialDrive

from .gearbox import GearBox
from robotmap import config

from common.stackedsystem import StackedSystem

class DriveTrain:
    """Low level component for controlling the robot's drivebase"""
    def __init__(self):
        self.left_gearbox = GearBox(config["drivetrain"]["motors"]["lf"], config["drivetrain"]["motors"]["lr"])
        self.right_gearbox = GearBox(config["drivetrain"]["motors"]["rf"], config["drivetrain"]["motors"]["rr"])
        
        self.left_gearbox.setInverted(False)
        self.right_gearbox.setInverted(False)
        
        self.drivebase = DifferentialDrive(self.left_gearbox.speedcontroller, self.right_gearbox.speedcontroller)
        self.drivebase.setSafetyEnabled(False)
    
    def arcadeDrive(self, speed, rotation, is_squared=False):
        """Best drive function to use for tank drive with an xbox controller"""
        self.drivebase.arcadeDrive(speed, rotation, is_squared)
        