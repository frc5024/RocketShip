import wpilib
from magicbot.state_machine import StateMachine
from robotmap import config
from common.logger import Logger

class HatchLoader(StateMachine):
    """Autonomously pick up a hatch"""

    console: Logger

    def __init__(self):
        super().__init__()
        self.xboxcontroller = wpilib.XboxController(config["xbox_controllers"]["driver"])

    def execute(self):
        # Check if pressed for logging
        if self.xboxcontroller.getBumperPressed(wpilib.GenericHID.Hand.kRight):
            self.console.log("Engaging hatch pickup")

        # Actually run the sequence
        if self.xboxcontroller.getBumper(wpilib.GenericHID.Hand.kRight):
            self.engage()
    
    @timed_state(duration=2.0)
    def align(self):
        pass
