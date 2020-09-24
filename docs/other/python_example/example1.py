# Lists

import random as rand

a = []


for i in range(10):
    ranNum = rand.randint(10, 50)
    a.append(ranNum)
    # a.insert(0, i)

print(a)


# # List builder
# b = [rand.randint(10, 50) for i in range(10)]
# print(f"{a}\n{b}")

# Keyword argument
# a.sort()
# print(a)

# lambda function
# a.sort(key=lambda n: abs(n - 30))
# print(a)


# List unpacking

[first, *rest] = a
# print(f"\nUnpacking:\t{rest}")

# # Alternative - slicing
first, rest = a[0], a[1:]
# print(f"Slice:\t\t{rest}")

# # Yet another alternative - but this modifies the original array!
first = a.pop(0)
# print(f"Pop:\t\t{a}")

# original = [first, *a]


# Swapping values
# a = 1
# b = 2

# print(f"a={a}, b={b}")
# a, b = b, a 

# print(f"a={a}, b={b}")


# Complex numbers

# c = 3 + 6j
# d = 4 - 10j

# print(c + d)
# print(c * d)
# print(c / d)