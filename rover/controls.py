from adafruit_servokit import ServoKit
import board
import busio
import time
from approxeng.input.selectbinder import ControllerResource

MAX_THROTTLE = 60
MIN_THROTTLE = 35
SERVO_CHANNEL = 0
THROTTLE_CHANNEL = 1


class Controls:
    def __init__(self):
        print("Initializing Servos")
        i2c_bus1=(busio.I2C(board.SCL, board.SDA))
        print("Initializing ServoKit")
        self.kit = ServoKit(channels=16, i2c=i2c_bus1)
        print("Done initializing")

    
    def forward(self, speed):
        speed = MAX_THROTTLE if (speed + MIN_THROTTLE) > MAX_THROTTLE else (speed + MIN_THROTTLE)
        print(f"Speeding up to {speed} \n")
        self.kit.continuous_servo[THROTTLE_CHANNEL].throttle = speed/100

    def brake(self):
        print(f"Braking \n");
        self.kit.continuous_servo[THROTTLE_CHANNEL].throttle = 0

    def turn_center(self):
        print(f"Centered \n")
        self.kit.servo[SERVO_CHANNEL].angle = 90

    def turn(self, angle):
        self.kit.servo[SERVO_CHANNEL].angle = angle

    def turn_right(self, angle):
        print(f"Turned right {angle} degrees \n")
        self.kit.servo[SERVO_CHANNEL].angle = 90 + angle

    def turn_left(self, angle):
        print(f"Turned left {angle} degrees \n")
        self.kit.servo[SERVO_CHANNEL].angle = 90 - angle