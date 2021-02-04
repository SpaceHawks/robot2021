import keyboard
from time import sleep
from vision import Locator

locator = Locator()

def wait_keyboard():
    print("Press t to test LiDAR...")
    keyboard.wait("t")
    print("Grabbing location...")
    
    locator.locate()
    locator.print_location()

    sleep(0.1)
    wait_keyboard()

wait_keyboard()