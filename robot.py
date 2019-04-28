import magicbot
import wpilib

from components.drive.drivetrain import DriveTrain
from components.drive.triggerdrive import TriggerDrive

class Robot(magicbot.MagicRobot):
    """
    Main robot class. 

    All robot code is managed and executed here.
    """

    # High level components that require variable injection
    trigger_drive: TriggerDrive


    def createObjects(self):
        """Starts all low level components"""
        self.drivetrain = DriveTrain()
    
    def teleopPeriodic(self):
        """Called every 20ms during teleop"""
        self.trigger_drive.execute()


if __name__ == "__main__":
    wpilib.run(Robot)