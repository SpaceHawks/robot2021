# import motors
from tether import Tether
from time import sleep
import asyncio
import random
# import linear_actuator
import sys
from vision import Detector, Locator
from xbox_drive import XboxController
from termcolor import colored, cprint

def receive_msg(msg, conn):
    # format is operator:arguments
    cmd, *args = msg.split(':')

    print(f"cmd: {cmd}, args: {args}")

# begin accepting connections
loop = asyncio.get_event_loop()
t = Tether(handler=receive_msg, loop=loop)

detector = Detector()
locator = Locator()
xbox = XboxController()

async def lidar_test():
    i = 0
    while True:
        locator.locate()
        new_obs = detector.detect(rob_x=locator.x, rob_y=locator.y, rob_a=locator.angle)
        if i % 10 == 0:
            print(f"Detected {len(new_obs)} obstacles")
            print(f"Location: ({locator.x}mm, {locator.y}mm, {locator.angle}rad)")
            i = 0

        obs_strs = [f"{o.x},{o.y}" for o in new_obs]
        obs_cmd = "O:" + ",".join(obs_strs)
        await t.send(obs_cmd)
        await t.send(f"R:{locator.x},{locator.y},{locator.angle}")
        await asyncio.sleep(0.25)
        i += 1

async def manual_control():
    i = 0
    while True:
        xbox.read_controller()
        if i % 10 == 0:
            print("\n--- READ XBOX VALUES ---")
            print(xbox.motor_xy)
            print(xbox.td_xy)
            print("------------------------\n")
            i = 0
        await asyncio.sleep(0.5)
        i += 1

loop.create_task(lidar_test())
loop.create_task(manual_control())

# Start the event loop
cprint(f"IP Address: {t.get_ip_address()}", "cyan")
print("Starting event loop")
loop.run_forever()

# Create obstacle detector
# detector = Detector()

# while True:
#     sleep(1)
#     print(cmd + "\n\n")
