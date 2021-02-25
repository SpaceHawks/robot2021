import keyboard
from time import sleep
from vision import Detector

detector = Detector()

def wait_keyboard():
    print("Press t to test obstacle LiDAR...")
    keyboard.wait("t")
    print("\bLooking for obstacles...")
    
    try:
        detector.detect(theta=0) # For now, just place the robot at 0 deg so we don't have to test with 2 lidars
        detector.print_obstacles()
    except RuntimeError as e:
        print(e)
    
    sleep(0.1)
    wait_keyboard()

    
wait_keyboard()
