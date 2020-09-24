# Classes

import math

class Point:
    # The constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # An instance method
    def distTo(self, other):
        if not isinstance(other, Point):
            raise TypeError("Must be to another point")
        return math.dist((self.x, self.y), (other.x, other.y))
        # OR
        # return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

# You'll see why this is necessary in example3.py
if __name__ == "__main__":
    p1 = Point(5, 20)
    p2 = Point(-15, 5)
    print(p1, p2)


    print(p1.distTo(p2))

    # try:
    #     print(p1.distTo(p2))
    # except TypeError as e:
    #     print(f"This is just wrong \nError: {e}")
    # else:
    #     print("That worked")
    
