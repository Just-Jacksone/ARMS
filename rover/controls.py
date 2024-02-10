from adafruit_servokit import ServoKit
import board
import busio
import time
from approxeng.input.selectbinder import ControllerResource

MAX_THROTTLE = 60
MIN_THROTTLE = 30
SERVO_CHANNEL = 0
THROTTLE_CHANNEL = 1


class Controls:
    def __init__(self):
        print("Initializing Servos")
        i2c_bus1=(busio.I2C(board.SCL, board.SDA))
        print("Initializing ServoKit")
        self.kit = ServoKit(channels=16, i2c=i2c_bus1)
        print("Done initializing")

    
    def forward(self, speed, duration=0):
        speed = MAX_THROTTLE if (speed + MIN_THROTTLE) > MAX_THROTTLE else (speed + MIN_THROTTLE)
        print(f"Speeding up to {speed} for {duration}s\n")
        self.kit.continuous_servo[THROTTLE_CHANNEL].throttle = speed/100
        time.sleep(duration)

    def brake(self, duration=0):
        print(f"Braking for {duration}s\n")
        self.kit.continuous_servo[THROTTLE_CHANNEL].throttle = 0

    def turn_center(self, duration=0):
        print(f"Centered for {duration}s\n")
        self.kit.servo[SERVO_CHANNEL].angle = 90

    def turn_right(self, angle, duration=0):
        print(f"Turned right {angle} degrees for {duration}s\n")
        self.kit.servo[SERVO_CHANNEL].angle = 90 + angle

    def turn_left(self, angle, duration=0):
        print(f"Turned left {angle} degrees for {duration}s\n")
        self.kit.servo[SERVO_CHANNEL].angle = 90 - angle





