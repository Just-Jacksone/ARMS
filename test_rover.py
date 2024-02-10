from unittest import removeResult
from rover.controls import Controls

rover = Controls()
rover.turn_right(angle = 90, duration=10)
rover.turn_center()

rover.forward(speed=1, duration=10)

rover.brake()