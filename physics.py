from pyfrc.physics.drivetrains import four_motor_drivetrain
from pyfrc.physics.visionsim import VisionSim

from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

from robotmap import config

from networktables.util import ntproperty

class PhysicsEngine:
    # Found, distance, angle
    target = ntproperty("/camera/target", (0.0, 0.0, 0.0))

    def __init__(self, controller):
        # Initialize the Sim and Gyro.
        self.controller = controller
        self.controller.add_device_gyro_channel('navxmxp_spi_4_angle')

        targets = [
            # left loading station
            VisionSim.Target(0, 2, 270, 90),
            # right loading station
            VisionSim.Target(0, 25, 270, 90)
        ]

        self.vision = VisionSim(
            targets, 61.0, 1.5, 15, 15, physics_controller=controller
        )
    """
        Keyword arguments:
        hal_data -- Data about motors and other components.
        now -- Current time in milliseconds
        tm_diff -- Difference between current time and time when last checked
    """

    def update_sim(self, hal_data, now, tm_diff):

        # Simulate the drivetrain motors.
        lf_motor = hal_data['CAN'][config["drivetrain"]["motors"]["lf"]]['value'] * -1
        lr_motor = hal_data['CAN'][config["drivetrain"]["motors"]["lr"]]['value'] * -1
        rf_motor = hal_data['CAN'][config["drivetrain"]["motors"]["rf"]]['value'] * -1
        rr_motor = hal_data['CAN'][config["drivetrain"]["motors"]["rr"]]['value'] * -1

        # Simulate movement.
        speed, rotation = four_motor_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor, speed=10)
        self.controller.drive(speed, rotation / 1.5, tm_diff)

        # x, y, angle = self.drivetrain.get_distance(lf_motor, rf_motor, tm_diff)
        # self.controller.distance_drive(x, y, angle)

        # Simulate encoders (NOTE: These values have not been calibrated yet.)
        hal_data['CAN'][config["drivetrain"]["motors"]["lf"]]['quad_position'] -= int(lf_motor / 5 * config["drivetrain"]["encoders"]["tpr"])
        hal_data['CAN'][config["drivetrain"]["motors"]["lr"]]['quad_position'] += int(rf_motor / 5 * config["drivetrain"]["encoders"]["tpr"])
        
        x, y, angle = self.controller.get_position()

        data = self.vision.compute(now, x, y, angle)
        if data is not None:
            data = data[0]
            info = (data[0], data[2], data[3] * 2)
            # print(info)
            self.target = info