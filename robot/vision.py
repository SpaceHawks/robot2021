#vision.py
from hokuyolx import HokuyoLX
import numpy as np
import math
import sys
from time import time
from termcolor import colored, cprint
from kalman import KalmanFilter


class LIDAR:
    def __init__(self, ip="192.168.1.10", port=10940):
        self.lidar = HokuyoLX(addr=(ip, port))
        self.kalman = KalmanFilter(adaptive=False, dt=0.025)

    def scan(self) -> list[tuple[float, float, float]]:
        return self.lidar.get_filtered_intens()[1].tolist()

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __hash__(self):
        return hash(self.__repr__())
    
    def __repr__(self):
        return f"{self.x},{self.y}"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

#Localization
class Locator(LIDAR):
    OUTLIER_CONSTANT = 1.5 # Threshold for considering a data point an outlier
    REFLECTIVITY_THRESHOLD = 3000 # Threshold for detecting light part of the target
    NUM_POINTS = 6 # Number of edges on the target
    LAST_STRIPE_BRIGHT = True # Whether or not the last stripe is white

    x = 0.0
    y = 0.0
    angle = 0.0
    last_updated = 0.0

    def locate(self):
        # Get LiDAR readings
        data_points = self.scan()


        # Setup some variables
        points_left = self.NUM_POINTS
        look_bright = self.LAST_STRIPE_BRIGHT # Are we looking for dark -> light transition (True) or light -> dark transition (False)?

        edges = [] # Stripe transitions that will be used for triangles

        # Iterate through the readings
        for point in data_points:
            d_ang, d_dist, intensity = point
            #print((np.degrees(d_ang), d_dist, intensity))
            is_bright = intensity >= self.REFLECTIVITY_THRESHOLD

            if points_left <= 0:
                break

            # Detect a change in dark -> light or light ->  dark
            if (look_bright is is_bright): # Both true or both false
                edges.append(point)
                look_bright = not look_bright # Now we look for opposite transition
                points_left -= 1
        
        if points_left > 0:
            print("Target not found")
	    #raise RuntimeError("Target not found")

        y = self._calculateY(edges)
        x = self._calculateX(y, edges)
        angle = self._calculateAngle(x, y, edges)
        
        self.kalman.addMeasurement([[x], [y], [angle]], [[0], [0]])
                
        [x, y, angle] = self.kalman.getXYA()
        # print(self.kalman.getXYAPrime())
        self.x = x
        self.y = y
        self.angle = angle
        # print(angle)
        self.last_updated = time()


    def _calculateX(self, y: float, edges: list[tuple[float, float, float]]):
        xs = []
        a1, d1, _ = edges[0] # The origin (last edge) will always be p1

        for i in range(1, len(edges)):
            a2, d2, _ = edges[i]

            alpha = a2 - a1
            w = math.sqrt(d1 ** 2 + d2 ** 2 - 2 * d1 * d2 * math.cos(alpha))

            dsin = d2 * math.sin(alpha)

            abs_x = abs(y * math.sqrt(w ** 2 - dsin ** 2) / dsin)

            # Need to figure out sign of x
            d_neg = math.sqrt(y ** 2 + (abs_x + w) ** 2)
            d_pos = math.sqrt(y ** 2 + (abs_x - w) ** 2)

            x = abs_x if abs(d_pos - d2) < abs(d_neg - d2) else -abs_x
            xs.append(x)
        # print([x * 0.03937008 for x in xs])
        xs_clean = self._removeOutliers(xs)
        return np.average(xs_clean)



    def _calculateY(self, edges: list[tuple[float, float, float]]):
        ys = []
        for i in range(len(edges) - 1):
            # Iterate over every sequential pair of edges
            a1, d1, _ = edges[i]
            a2, d2, _ = edges[i + 1]

            alpha = a1 - a2 # The sign doesn't matter for this calculation
            d1d2 = d1 * d2 # Used more than once might as well be efficient

            w = math.sqrt(d1 ** 2 + d2 ** 2 - 2 * d1d2 * math.cos(alpha))
            y = abs(d1d2 * math.sin(alpha) / w) # y is always positive

            ys.append(y)
        
        ys_clean = self._removeOutliers(ys)
        return np.average(ys_clean)


    def _calculateAngle(self, x: float, y: float, points: list[tuple[float, float, float]]):
        alpha_origin, *_ = points[-1]
        arctanxy = math.atan2(x, y)
        return alpha_origin - arctanxy

    # Remove outliers from list of values
    def _removeOutliers(self, x):
        # Removes outliers before taking the average
        a = np.array(x)
        a = a[~np.isnan(a)]
        upper_quartile = np.percentile(a, 75)
        lower_quartile = np.percentile(a, 25)
        
        IQR = (upper_quartile - lower_quartile) * self.OUTLIER_CONSTANT
        lower_bound, upper_bound = (lower_quartile - IQR, upper_quartile + IQR)

        without_outliers = [num for num in a if lower_bound <= num <= upper_bound]

        return without_outliers

    def print_location(self):
        x_r = round(self.x * 0.03937008, 2)
        y_r = round(self.y * 0.03937008, 2)
        a_r = round(np.degrees(self.angle), 2)

        cprint(f"x: {x_r}, y: {y_r}, a: {a_r}°", "cyan")

# Obstacle Detection
class Detector(LIDAR):
    MAX_DIST = 3000 # How close should an obstacle be before we "care" about it?
    ROUND_TO = 5 # Number of mm to round to

    obstacles = set()

    def __init__(self):
        super().__init__("192.168.0.11", 10940) # Uses non-default IP address to avoid interfering with Locator

    def detect(self, rob_x, rob_y, rob_a):
        # Set of new obstacles
        discovered = set()
        # Get LiDAR readings
        data_points = self.scan()

        # Iterate through the readings
        for point in data_points:
            alpha, dist, _ = point

            # We don't care about far away obstacles bc inaccuracy
            if dist > self.MAX_DIST:
                continue

            angle = alpha - rob_a

            x = dist * math.sin(angle)
            y = dist * math.cos(angle)

            x += rob_x
            y += rob_y

            # TODO: Depends on angle
            y += 38.375 # height of robot
            # Round x and y to nearest ROUND_TO
            x = math.floor(x / self.ROUND_TO) * self.ROUND_TO
            y = math.floor(y / self.ROUND_TO) * self.ROUND_TO

            obs_pt = Point(x,y)
            discovered.add(obs_pt)
            if obs_pt not in self.obstacles:
                #discovered.add(obs_pt)
                self.obstacles.add(obs_pt)

        return discovered

    def print_obstacles(self):
        cprint(f"There are {len(self.obstacles)} obstacles", "red")
        # for o in self.obstacles:
        #     print(f"[{o.x}, {o.y}],")
            
