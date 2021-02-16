import keyboard
from time import sleep
from vision import Locator
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
    results_x = []
    results_y = []
    results_a = []
    for i in range(num):
        try:
            locator.locate()
            locator.print_location()
            results_x.append(locator.x)
            results_y.append(locator.y)
            results_a.append(locator.angle)
        except RuntimeError as e:
            print(e)
        sleep(0.1)
    
    # t = [(i+1) for i in range(num)]
    print(results_x)
    print(results_y)
    print(results_a)
    # plt.plot(t, results_x, 'r--', t, results_y, 'bs')
    #plt.ylabel("Distance (mm)")
    # plt.show()
    
run_tests(1000)
# wait_keyboard()
