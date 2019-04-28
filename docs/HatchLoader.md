# Hatchloader
HatchLoader is a FSM that autonomously aligns the robot with a loading station and grabs a hatch

## Required sensors
| Sensor | Use |
| -- | -- |
| Gyro | Finds the robot's heading relitive to the loading station (robot must be placed correctly during the start of a match). The robot should use this as a referance point when calculating its path to follow towards the loading station. |
| Camera | Detects distance from a target for use in path calculation, and the robot's angle from the loading station to feed to the slider|

## Failsafes
There is a chance that the gyro may be reset during a match. To solve this, first, a raw gyro reading wil be accessed through a GyroInstance that allows scoped resets of the gyro (aka. other systems cannot interfere with eachother's gyro readings). In the worst case, if the RIO reboots during a match, Thr driver can control the slider with the right joystick and the pneumatics with the button pad.

A camera may break or the http server may drop. In this case, the driver and human player must communicate to manually align the robot using the controls described above.

## Procedure
```
Button press
Enable LED
PID turn to target
Finger down
drive forward and rotate and slide while encoder < length
Finger Up
drive back at 0.8 for 0.3
```