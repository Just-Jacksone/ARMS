from unittest import removeResult
from rover.controls import Controls
import time

rover = Controls()
rover.turn_left(angle = 90)
time.sleep(1)
rover.turn_right(angle = 90)
time.sleep(1)
rover.turn_center()
time.sleep(1)
rover.forward(speed=1)
time.sleep(1)
rover.brake()