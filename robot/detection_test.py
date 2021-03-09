# import keyboard
from time import sleep
from vision import Detector

detector = Detector()

def run_detect_test():
    for i in range(10):
        try:
            d = len(detector.detect(theta=0)) # For now, just place the robot at 0 deg so we don't have to test with 2 lidars
            print(d)
        except RuntimeError as e:
            print(e)
        # sleep(0.5)
        
    detector.print_obstacles()
    
run_detect_test()
