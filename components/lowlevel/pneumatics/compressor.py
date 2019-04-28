import wpilib

from robotmap import config

class Compressor:
    """Wrapper around wpilib compressor"""

    def __init__(self):
        self.compressor = wpilib.Compressor()

        # Force the compressor to ignore enable signals from the pressure switch
        # This ensures the the compressor does not automatically turn on
        self.compressor.setClosedLoopControl(False)
    
    def setEnabled(self, is_enabled):
        """
        Control the compressor
        
        If set to true, the compressor will automatically turn on when the pressure switch is tripped
        """
        self.compressor.setClosedLoopControl(is_enabled)
