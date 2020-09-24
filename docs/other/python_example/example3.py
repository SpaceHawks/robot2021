# Importing from another file
from example2 import Point

# We are "extending" the Point class
# Any methods defined there are also defined here
class PointV2(Point):
    # We don't HAVE to define an __init__ since we're extending Point

    # def __init__(self, x, y, z=0):
    #     super().__init__(x, y)
    #     self.z = z

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, Point):
            return PointV2(self.x + other.x, self.y + other.y)
        if isinstance(other, (int, float)):
            return PointV2(self.x + other, self.y + other)
        raise TypeError("Not a valid operation")


p1 = PointV2(30, 60)
p2 = PointV2(40, 50)

# The printed values look much nicer now!
print(p1, p2)

# What would we want this result in?
print(p1 + p2)


# What about this?
print(p1 + p2 + 50)

# You implement this one (hint: Come up with a way to make use of __add__ without copying everything)
# __neg__ and __sub__ are also class methods you can override
print(p1 - p2)