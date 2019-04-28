import magicbot
import wpilib

from components.lowlevel.drivebase.drivetrain import DriveTrain
from components.lowlevel.pneumatics.compressor import Compressor

from components.highlevel.triggerdrive import TriggerDrive
from components.highlevel.controlcompressor import ControlCompressor

from common.logger import Logger

class Robot(magicbot.MagicRobot):
    """
    Main robot class. 

    All robot code is managed and executed here.
    """

    # High level components that require variable injection
    trigger_drive: TriggerDrive
    control_compressor: ControlCompressor


    def createObjects(self):
        """Starts all low level components"""
        self.drivetrain = DriveTrain()
        self.compressor = Compressor()
        self.console = Logger()
    
    def robotPeriodic(self):
        self.console.push()
    
    def teleopPeriodic(self):
        """Called every 20ms during teleop"""
        self.trigger_drive.execute()
        self.control_compressor.execute()


if __name__ == "__main__":
    wpilib.run(Robot)