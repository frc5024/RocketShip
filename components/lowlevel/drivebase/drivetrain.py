import wpilib
import ctre
from navx import AHRS
from wpilib.drive import DifferentialDrive

from .gearbox import GearBox
from robotmap import config

from common.stackedsystem import StackedSystem
from common.pidcontroller import PIDController

class DriveTrain:
    """Low level component for controlling the robot's drivebase"""
    def __init__(self):
        self.left_gearbox = GearBox(config["drivetrain"]["motors"]["lf"], config["drivetrain"]["motors"]["lr"])
        self.right_gearbox = GearBox(config["drivetrain"]["motors"]["rf"], config["drivetrain"]["motors"]["rr"])
        
        self.left_gearbox.setInverted(False)
        self.right_gearbox.setInverted(False)
        
        self.drivebase = DifferentialDrive(self.left_gearbox.speedcontroller, self.right_gearbox.speedcontroller)
        self.drivebase.setSafetyEnabled(False)

        self.gyro = AHRS.create_spi()
        self.gyro.reset()

        self.rotation_controller = PIDController(0.01, 0, 0)
        self.forward_rotation_controller = PIDController(0.01, 0, 0)
        
        self.bang_bang_ticks_offset = 0
    
    def rotateToSetpoint(self):
        rotation = self.rotation_controller.Feed(self.gyro.getAngle())
        self.arcadeDrive(0.0, rotation)
    
    def driveAndRotateToSetpoint(self, camera_angle):
        rotation = self.forward_rotation_controller.Feed(camera_angle)
        self.arcadeDrive(0.5, rotation)
    
    def bangBangToTicks(self, ticks, speed):
        if self.left_gearbox.front.getSelectedSensorPosition() - self.bang_bang_ticks_offset < ticks:
            self.arcadeDrive(speed, 0.0)
        elif self.left_gearbox.front.getSelectedSensorPosition() - self.bang_bang_ticks_offset > ticks:
            self.arcadeDrive(-speed, 0.0)
        else:
            self.arcadeDrive(0.0, 0.0)
    
    def resetBangBang(self):
        self.bang_bang_ticks_offset = self.left_gearbox.front.getSelectedSensorPosition()
    
    def arcadeDrive(self, speed, rotation, is_squared=False):
        """Best drive function to use for tank drive with an xbox controller"""
        self.drivebase.arcadeDrive(speed, rotation, is_squared)
        