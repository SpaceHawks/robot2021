import keyboard
from time import sleep
from vision import Locator
import numpy as np
# import matplotlib.pyplot as plt


locator = Locator()

def wait_keyboard():
    print("Press t to test LiDAR...")
    keyboard.wait("t")
    print("\bGrabbing location...")
    
    try:
        locator.locate()
        locator.print_location()
    except RuntimeError as e:
        print(e)
    
    sleep(0.1)
    wait_keyboard()

def run_tests(num):
    NUM_TESTS = 1
    results_x = []
    results_y = []
    results_a = []
    for i in range(NUM_TESTS):
        print(f"{i+1}/{NUM_TESTS}")
        try:
            locator.locate()
            # locator.print_location()
            results_x.append(locator.x)
            results_y.append(locator.y)
            results_a.append(locator.angle)
        except RuntimeError as e:
            print(e)
    
    # t = [(i+1) for i in range(num)]
    print(f"x_std: {np.std(results_x)} ({results_x[-1]})")
    print(f"y_std: {np.std(results_y)} ({results_y[-1]})")
    print(f"a_std: {np.std(results_a)}")
    # plt.plot(t, results_x, 'r--', t, results_y, 'bs')
    #plt.ylabel("Distance (mm)")
    # plt.show()
