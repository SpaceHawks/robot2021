# Numpy
import numpy as np

# Tuple - basic Python structure
shape = (3, 3)

# Make a matrix with all zeroes that is 3x3
m1 = np.zeros(shape)
# print(m1)

# If we want it to be all ints
m2 = np.zeros(shape, dtype=np.int16)
# print(m2)

# Identity matrix, 5x5
m3 = np.eye(5, dtype=np.uint8)
# print(m3)

# We can create matrices of any dimensions - this one makes a 2x2x2x2 matrix with all 10s
shape = (2, 2, 2, 2)
m4 = np.full(shape, 10)
# print(m4)

# Determinant
m5 = np.array([
    [1, 2],
    [3, 4]
])

# We know this should be 1 * 4 - 3 * 2 = -2
# print(np.linalg.det(m5))

# Good luck solving a 5x5 matrix by hand
m6 = np.random.randint(5, 15, size=(5, 5))
# print(np.linalg.det(m6))

# Solving a simple Ax=B
a = np.array([
    [1, 2],
    [3, 4]
])

b = np.array([
    [9],
    [29]
])

# The answer should be [11, -1]
# print(np.linalg.solve(a, b))

# Filtering
a = np.random.randint(-5, 5, (4, 4))
print(a)

# a_0 = a[a > 0]
# print(f"\nValues greater than zero:\n{a_0}\n")

a_1 = np.amax(a)
print(f"Max value:\n{a_1}\n")

# If the max is at [0, 2] and [1, 3], where returns ([0, 1], [2, 3])
(xs, ys) = np.where(a == a_1)

print(f"xs: {xs}\nys: {ys}\n")

# zip pairs together things in the first list with what is in the second
# i.e. we will get (0, 2) and (1, 3)
pts = list(zip(xs, ys))

print(f"Indices of max value:\n{pts}\n")