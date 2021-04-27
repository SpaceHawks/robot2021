# vision.py
from hokuyolx import HokuyoLX
import numpy as np
from scipy import stats
import math
import sys
from time import time
from termcolor import colored, cprint
from kalman import KalmanFilter


class LIDAR:
    def __init__(self, ip="192.168.1.10", port=10940):
        self.lidar = HokuyoLX(addr=(ip, port))
        self.kalman = KalmanFilter(adaptive=False, dt=0.025)

    def scan(self):
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

# Localization
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

class Locator(LIDAR):
    OUTLIER_CONSTANT = 1.5  # Threshold for considering a data point an outlier
    REFLECTIVITY_THRESHOLD = 3000  # Threshold for detecting light part of the target
    NUM_POINTS = 6  # Number of edges on the target
    LAST_STRIPE_BRIGHT = True  # Whether or not the last stripe is white

    x = 0.0
    y = 0.0
    angle = 0.0
    last_updated = 0.0

    def locate(self):
        # Get LiDAR readings
        data_points = self.scan()

        # Setup some variables
        points_left = self.NUM_POINTS
        # Are we looking for dark -> light transition (True) or light -> dark transition (False)?
        look_bright = self.LAST_STRIPE_BRIGHT

        edges = []  # Stripe transitions that will be used for triangles

        # Iterate through the readings
        for point in data_points:
            _, _, intensity = point
            is_bright = intensity >= self.REFLECTIVITY_THRESHOLD

            # If the current point is on the target
            if points_left < self.NUM_POINTS:
                edges.append(point)

            # a
            if points_left <= 0:
                break


            # Detect a change in dark -> light or light ->  dark
            if (look_bright is is_bright):  # Both true or both false
                look_bright = not look_bright  # Now we look for opposite transition
                points_left -= 1

        if points_left > 0:
            print("Target not found")
            return  # Don't update anything

        # Calculate the relative (x, y) coordinates of the target points
        points = [(p[1] * math.sin(p[0]), p[1] * math.cos(p[0])) for p in edges]

        # Calculate the linear regression for the points
        slope, intercept, *_ = stats.linregress(points)

        # The angle of the robot is simply the angle of this linear regression
        theta = math.atan(slope)

        # Get the point representing right edge of target, need to rotate it
        mid_idx = len(points) // 2
        ref_point = (points[mid_idx][0], points[mid_idx][1]) # np.array((ref_x, slope * ref_x + intercept))  # The linear regressed point
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))  # Rotation matrix

        # Rotate the point, extract x and y values
        res = np.matmul(ref_point, R)
        x, y = res

        # Kalman filter
        self.kalman.addMeasurement([[x], [y], [theta]], [[0], [0]])
        #[x, y, theta] = self.kalman.getXYA()

        self.x = x
        self.y = y
        self.angle = theta
        self.last_updated = time()

    def print_location(self):
        x_r = round(self.x * 0.03937008, 2)
        y_r = round(self.y * 0.03937008, 2)
        a_r = round(np.degrees(self.angle), 2)

        cprint(f"x: {x_r}, y: {y_r}, a: {a_r}°", "cyan")

# Obstacle Detection


class Detector(LIDAR):
    MAX_DIST = 3000  # How close should an obstacle be before we "care" about it?
    ROUND_TO = 5  # Number of mm to round to

    obstacles = set()

    def __init__(self):
        # Uses non-default IP address to avoid interfering with Locator
        super().__init__("192.168.0.11", 10940)

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

            x = dist * math.sin(alpha)
            y = dist * math.cos(alpha) + 38.375

            x += rob_x
            y += rob_y

            x, y = rotate((rob_x, rob_y), (x, y), -rob_a)

            # Round x and y to nearest ROUND_TO
            x = math.floor(x / self.ROUND_TO) * self.ROUND_TO
            y = math.floor(y / self.ROUND_TO) * self.ROUND_TO

            obs_pt = Point(x, y)
            discovered.add(obs_pt)
            if obs_pt not in self.obstacles:
                # discovered.add(obs_pt)
                self.obstacles.add(obs_pt)

        return discovered

    def print_obstacles(self):
        cprint(f"There are {len(self.obstacles)} obstacles", "red")
        # for o in self.obstacles:
        #     print(f"[{o.x}, {o.y}],")
