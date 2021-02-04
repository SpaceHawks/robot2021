#vision.py
from hokuyolx import HokuyoLX
import numpy as np
import math
import sys
from termcolor import colored, cprint


class LIDAR:
	def __init__(self):
		self.lidar = HokuyoLX()
	
	def scan(self) -> list[tuple[float, float, float]]:
		return self.lidar.get_filtered_intens()[1].tolist()

class Locator(LIDAR):
	OUTLIER_CONSTANT = 1.5 # Threshold for considering a data point an outlier
	REFLECTIVITY_THRESHOLD = 3000 # Threshold for detecting light part of the target
	NUM_POINTS = 6 # Number of edges on the target
	LAST_STRIPE_BRIGHT = True # Whether or not the last stripe is white

	x = 0.0
	y = 0.0
	angle = 0.0

	def locate(self):
		# Get LiDAR readings
		data_points = self.scan()

		# Setup some variables
		points_left = self.NUM_POINTS
		look_bright = self.LAST_STRIPE_BRIGHT # Are we looking for dark -> light transition (True) or light -> dark transition (False)?

		edges = [] # Stripe transitions that will be used for triangles

		# Iterate through the readings
		for point in data_points:
			_, _, intensity = point
			is_bright = intensity >= self.REFLECTIVITY_THRESHOLD

			if points_left <= 0:
				break

			# Detect a change in dark -> light or light ->  dark
			if (look_bright is is_bright): # Both true or both false
				edges.append(point)
				look_bright = not look_bright # Now we look for opposite transition
				points_left -= 1
		
		if points_left > 0:
			raise RuntimeError("Target not found")

		y = self._calculateY(edges)
		x = self._calculateX(y, edges)
		angle = self._calculateAngle(x, y, edges)

		self.x = x
		self.y = y
		self.angle = angle


	def _calculateX(self, y: float, edges: list[tuple[float, float, float]]):
		xs = []
		a1, d1 = edges[-1] # The origin (last edge) will always be p1

		for i in range(1, len(edges)):
			a2, d2 = edges[i]

			alpha = a1 - a2
			w = math.sqrt(d1 ** 2 + d2 ** 2 - 2 * d1 * d2 * math.cos(alpha))

			dsin = d2 * math.sin(alpha)

			abs_x = abs(y * math.sqrt(w ** 2 - dsin ** 2) / dsin)

			# Need to figure out sign of x
			d_neg = math.sqrt(y ** 2 + (abs_x + w) ** 2)
			d_pos = math.sqrt(y ** 2 + (abs_x - w) ** 2)

			x = abs_x if abs(d_pos - d2) < abs(d_neg - d2) else -abs_x
			xs.append(x)
		
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
		upper_quartile = np.percentile(a, 75)
		lower_quartile = np.percentile(a, 25)
		IQR = (upper_quartile - lower_quartile) * self.OUTLIER_CONSTANT
		quartileSet = (lower_quartile - IQR, upper_quartile + IQR)

		without_outliers = []
		for num in a:
			if num >= quartileSet[0] and num <= quartileSet[1]:
				without_outliers.append(num)

		return without_outliers

	def print_location(self):
		x_r = round(self.x, 2)
		y_r = round(self.y, 2)
		a_r = round(self.angle, 2)

		cprint(f"x: {x_r}, y: {y_r}, a: {a_r}", "cyan")

