import wpilib

from robotmap import config
from components.lowlevel.pneumatics.compressor import Compressor

from common.logger import Logger

class ControlCompressor:
    """Use the controller's start and select buttons to control the compressor"""

    compressor: Compressor
    console: Logger

    def __init__(self):
        self.xboxcontroller = wpilib.XboxController(config["xbox_controllers"]["driver"])
    
    def execute(self):
        """Called on every loop of the 'schedular'"""
        
        # Start the compressor with start button
        if self.xboxcontroller.getStartButtonReleased():
            self.compressor.setEnabled(True)
            self.console.log("Compressor enabled")

        # Stop the compressor with back button
        if self.xboxcontroller.getBackButtonReleased():
            self.compressor.setEnabled(False)
            self.console.log("Compressor disabled")
