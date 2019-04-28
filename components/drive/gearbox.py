import ctre
import wpilib

class GearBox:
    def __init__(self, front_motor: int, back_motor: int):
        """
        Given 2 motor ids, creates a gearbox with speedcontroller and assumes that the front motor is the master and is attached to an encoder
        """
        self.front = ctre.wpi_talonsrx.WPI_TalonSRX(front_motor)
        self.back = ctre.wpi_talonsrx.WPI_TalonSRX(back_motor)

        self.back.follow(self.front)

        self.speedcontroller = wpilib.SpeedControllerGroup(self.front, self.back)
    
    def configEncoders(self):
        """Wrapper around CTRE's configuration"""
        self.front.configFactoryDefault()
    
    def setPhase(self, phase):
        """Set to true if encoder counts down while motor spins forward"""
        self.front.setPhase(phase)
    
    def setInverted(self, isInverted):
        """Swaps front and back on motors"""
        self.front.setInverted(isInverted)
        self.back.setInverted(isInverted)
    

    