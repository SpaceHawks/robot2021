import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import time, math
from generate_obstacles import generate_obstacles
from a_star import A_star

# False = average run time, True = show plot
mode = True
grid_size = 5

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

start = Point(180 // grid_size, 100 // grid_size)
goal = Point(180 // grid_size, 450 // grid_size)

def get_obs(obs, angle_drawn):
    obs_x = []
    obs_y = []

    for x in range(len(obs)):
        for y in range(len(obs[x])):
            if obs[x][y][10-angle_drawn]:
                obs_x.append(x)
                obs_y.append(y)



    return (obs_x, obs_y)

if mode:
    obs = generate_obstacles()
    path = A_star(start, goal, obs, width=360//grid_size, height=540//grid_size, grid_size=grid_size)
    path_x = [p.x for p in path]
    path_y = [p.y for p in path]


    (obs_x, obs_y) = get_obs(obs, 75//15)
    fig, ax = plt.subplots(figsize=(5.4, 8.1))
    plt.subplots_adjust(left=0.1, bottom=0.35)
    p_obs, = plt.plot(obs_x, obs_y, 'o', color="green")
    plt.plot(path_x, path_y, 'o', color="blue")
    plt.plot([start.x, goal.x], [start.y, goal.y], 'o', color="red")
    plt.axis([0, 360//grid_size, 0, 540//grid_size])

    ax_slider = plt.axes([0.1, 0.2, 0.8, 0.05])
    slider = Slider(ax_slider, "Angle", valmin=-75, valmax=90, valinit=0, valstep=15, valfmt="%d°")

    def update_obs(an):
        (obs_x, obs_y) = get_obs(obs, int(an+75)//15)
        p_obs.set_data(obs_x, obs_y)
        plt.draw()

    slider.on_changed(update_obs)
    plt.show()

else:
    total = 0
    max_val = 0
    for i in range(1000):
        obs = generate_obstacles()

        # Run and calculate time
        start_time = time.process_time()
        path = A_star(start, goal, obs)
        time_taken = time.process_time() - start_time

        total+=time_taken
        max_val = max(time_taken, max_val)

        print(f"PATH #{i+1}: {time_taken}\n{total/(i+1)} AVG\n\n")
        time.sleep(0.5)
