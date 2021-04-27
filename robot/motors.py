# Contains methods for the control and monitoring of various motors
#from board import SCL, SDA
#from adafruit_pca9685 import PCA9685
from pysabertooth import Sabertooth
# from analogio import AnalogIn
from enum import Enum
import board
import busio
import time
# import rotaryio

# each Sabertooth controls 2 motors
f_saber = Sabertooth('/dev/ttyS1', baudrate=9600, address=128, timeout=1000)
b_saber = Sabertooth('/dev/ttyS1', baudrate=9600, address=129, timeout=1000)
TD_saber = Sabertooth('/dev/ttyS1', baudrate=9600, address=130, timeout=1000)


# Motor Numbers
class Motor(Enum):
    FRONT_LEFT = 0
    BACK_LEFT = 1
    FRONT_RIGHT = 2
    BACK_RIGHT = 3

    @staticmethod
    def is_front(motor):
        return motor == Motor.FRONT_LEFT or motor == Motor.FRONT_RIGHT

    @staticmethod
    def is_back(motor):
        return motor == Motor.BACK_LEFT or motor == Motor.BACK_RIGHT

    @staticmethod
    def is_left(motor):
        return motor == Motor.FRONT_LEFT or motor == Motor.BACK_LEFT

    @staticmethod
    def is_right(motor):
        return motor == Motor.FRONT_RIGHT or motor == Motor.BACK_RIGHT


# Chassis motors


class DriveTrain:
    motor_speeds = [0, 0, 0, 0]

    # set speed for individual wheel [-100%,+100%]
    @staticmethod
    def set_motor_speed(motor, percent):
        print("set mot speed:", motor, percent)

        motor_side = 0 if Motor.is_left(motor) else 1  # Motor 0 is left, Motor 1 is right
        if Motor.is_front(motor):
            f_saber.drive(motor_side, percent)
        elif Motor.is_back(motor):
            b_saber.drive(motor_side, percent)
        else:
            raise Exception("bad motor number")

        DriveTrain.motor_speeds[motor] = percent

    @staticmethod
    def stop():
        f_saber.stop()
        b_saber.stop()
        DriveTrain.motor_speeds = [0, 0, 0, 0]

    # both arguments are percents [100%-100%]
    @staticmethod
    def arcade_drive(throttle, turn):
        v = (100 - abs(turn)) * (throttle / 100) + throttle
        w = (100 - abs(throttle)) * (turn / 100) + turn
        l = (v + w) / 2
        r = (v - w) / 2
        # send tank drive command
        DriveTrain.tank_drive(l, r)

    @staticmethod
    def tank_drive(left_percent, right_percent):
        DriveTrain.set_motor_speed(0, left_percent)
        DriveTrain.set_motor_speed(1, left_percent)
        DriveTrain.set_motor_speed(2, right_percent)
        DriveTrain.set_motor_speed(3, right_percent)


# class Trenchdigger:
#     TD_speed = 0

#     @staticmethod
#     def set_TD_speed(percent):
#         TD_saber.drive(0, percent)
#         TD_speed = percent

#     @staticmethod
#     def servo(angle):
#         dutyCycle = (angle + 45)/18  # convert degrees to duty cycle
#         GPIO.setmode(GPIO.ASUS)
#         GPIO.setwarnings(False)

#         servo = 32

#         GPIO.setup(servo, GPIO.OUT)
#         pwm = GPIO.PWM(servo, 50)
#         pwm.ChangeDutyCycle(dutyCycle)
#         time.sleep(1)

#     @staticmethod
#     def TD_stop():
#         TD_saber.drive(0, 0)
#         TD_speed = 0

    # @staticmethod
    # def get_encoder():
    #     position = enc.position
    #     last_position = position
    #     print(position)
    #     return position
    #     time.sleep(0.25)
