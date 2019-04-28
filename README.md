# RocketShip
Driver-assisted autonomous for DeepSpace

The goal of the RocketShip project is to ler computers take full control of the robot as often as possible. This way, alignment and planning tasks will allways be completed as efficiently as possible.

## Autonomous hatch pickup
At the press of a button, the robot will follow the HatchLoader routine outlined [HERE](./docs/HatchLoader.md) 

This routine takes full control of the robot and uses camera and gyro data to pick up a hatch from either loading station.

## Controls
Driving is the standard triggerdrive used on all of our robots, and Holding the right bumper will automatically pick up a hatch from the nearest loading station.