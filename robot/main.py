# import motors
from tether import Tether
from time import sleep
# import linear_actuator
import sys
from vision import Detector

def receive_msg(msg, conn):
    # format is operator:arguments
    cmd, args = msg.split(':')

    print(f"cmd: {cmd}, args: {args}")

    # arcade drive
    # if cmd == 'AD':
    #     throttle, turn = map(int, args.split(','))
    #     motors.DriveTrain.arcade_drive(throttle, turn)

    # # tank drive
    # elif cmd == 'TD':
    #     left, right = map(int, args.split(','))
    #     motors.DriveTrain.tank_drive(left, right)

    # # stop all movement
    # elif cmd == 'STOP':
    #     motors.DriveTrain.stop()
    #     motors.Trenchdigger.set_TD_speed(0)

    # # emergency stop
    # elif cmd == 'DIE':
    #     motors.DriveTrain.stop()
    #     sys.exit(1)

    # # switch to autonomous mode
    # elif cmd == 'AI':
    #     motors.DriveTrain.tank_drive(0, 0)
    #     conn.send("MSG: TODO: autonomous")
    #     print('auto command received')

    # # read trench digger encoder
    # elif cmd == 'ENC':
    #     e = motors.Trenchdigger.get_encoder()
    #     conn.send("ENC: e")

    # # activate hopper servo
    # elif cmd == 'SER':
    #     motors.Trenchdigger.servo(90)

    # # read potentiometer
    # elif cmd == 'POT':
    #     p = motors.Trenchdigger.get_pot()
    #     conn.send("POT: p")

    # #start trench digger
    # elif cmd == 'DIG':
    #     motors.Trenchdigger.set_TD_speed(1)
    #     print('trench digger active')

    # elif cmd == 'DEPLOY':
    #     motors.Trenchdigger.set_TD_speed(0.5)
    #     linear_actuator.LinearActuatorPair.set_position(1)
    #     motors.Trenchdigger.set_TD_speed(0)

    # elif cmd == 'RETRACT':
    #     motors.Trenchdigger.set_TD_speed(0)
    #     linear_actuator.LinearActuatorPair.set_position(0)

    # elif cmd == 'DUMP':
    #     linear_actuator.Hopper.set_hopper(1)
    #     linear_actuator.Hopper.set_hopper(0)

    # else:
    #     motors.DriveTrain.tank_drive(0,0)
    #     conn.send("WARN: invalid command")
    #     print('invalid command: ', msg)

# begin accepting connections
t = Tether(receive_msg)


# Create obstacle detector
# detector = Detector()

# while True:
#     sleep(1)
#     new_obs = detector.detect(theta=0)
#     obs_strs = [f"{o.x},{o.y}" for o in new_obs]
#     cmd = "O:" + ",".join(obs_strs)
#     print(cmd + "\n\n")