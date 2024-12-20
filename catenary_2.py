import matplotlib.pyplot as plt
import math
import numpy as np

x1, y1 = -0.5, 0.7
x2, y2 = 0.6, -0.2
L = 2

dx = x2 - x1
dy = y2 - y1
x_mean = (x1 + x2) / 2
y_mean = (y1 + y2) / 2

if dx**2 + dy**2 > L**2:
    exit("The string is too short!")

r = math.sqrt(L**2 - dy**2) / dx
da = 1e-10
A0 = math.sqrt(6 * (r - 1))
if r >= 3:
    A0 = math.log(2 * r) + math.log(math.log(2 * r))

A1 = A0 - (math.sinh(A0) - r * A0) / (math.cosh(A0) - r)

while abs(r - math.sinh(A1) / A1) > da:
    print(abs(r - math.sinh(A1) / A1))
    A0 = A1
    A1 = A0 - (math.sinh(A0) - r * A0) / (math.cosh(A0) - r)

A = A1
a = dx / (2 * A)
b = x_mean - a * math.atanh(dy / L) # b is center of the curve
c = y_mean - L / (2 * math.tanh(A)) # c is vertical offset

def f(x):
    return a * math.cosh((x - b)/ a) + c

xpoints = np.arange(x1, x2, 1e-2)
ypoints = [f(x) for x in xpoints]

plt.plot(xpoints, ypoints)
plt.grid()
plt.show()