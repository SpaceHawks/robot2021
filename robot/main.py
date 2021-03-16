# import motors
from tether import Tether
from time import sleep
import asyncio
import random
# import linear_actuator
import sys
from vision import Detector

def receive_msg(msg, conn):
    # format is operator:arguments
    cmd, *args = msg.split(':')

    print(f"cmd: {cmd}, args: {args}")

# begin accepting connections
loop = asyncio.get_event_loop()
t = Tether(handler=receive_msg, loop=loop)

lidar = Detector()

async def obstacleTest():
    while True:
        new_obs = lidar.detect(theta=0)
        obs_strs = [f"{o.x},{o.y}" for o in new_obs]
        cmd = "O:" + ",".join(obs_strs)
        await t.send(cmd)
        await asyncio.sleep(5)


loop.create_task(obstacleTest())

# Start the event loop
print(f"IP Address: {t.get_ip_address()}")
print("Starting event loop")
loop.run_forever()

# Create obstacle detector
# detector = Detector()

# while True:
#     sleep(1)
#     print(cmd + "\n\n")