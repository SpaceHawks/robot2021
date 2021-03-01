# import keyboard
from time import sleep
from vision import Detector

detector = Detector()

def wait_keyboard():
    print("Running obstacle LiDAR...")
    
    for i in range(10):
        print(i)
        try:
            detector.detect(theta=0) # For now, just place the robot at 0 deg so we don't have to test with 2 lidars
        except RuntimeError as e:
            print(e)
        sleep(0.5)
        
    detector.print_obstacles()
    
wait_keyboard()
