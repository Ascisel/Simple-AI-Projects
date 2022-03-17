import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import NewtonAlgorithm as na
import SteepestDescentAlgorithm as sda
from sympy import *


def pointMatrix(coord1, coord2):
    return np.matrix([[coord1], [coord2]])


fig = plt.figure()
ax = plt.axes(projection='3d')


def f(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2


x_el = np.linspace(-10, 10, 30)
y_el = np.linspace(-10, 10, 30)

X, Y = np.meshgrid(x_el, y_el)
Z = f(X, Y)

ax = plt.axes(projection='3d')
ax.contour3D(X, Y, Z, 50, cmap=cm.coolwarm)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

x, y = symbols('x y')
func = (x**2 + y - 11)**2 + (x + y**2 - 7)**2  # podanie wzoru funkcji
start = pointMatrix(-2, -3)  # wyznaczenie punktu startowego
# wybranie algorytmu oraz jego parametrów (wzór funkcji, punkt startowy, epsilon, betha, maksymalna liczba iteracji)
path = na.NewtonAlgorithm(func, start, 10**-20, 1, 10000)
# path = sda.SteepestDescentAlgorithm(func, start, 10**-20, 0.01, 10000)


xdata = [point.item(0) for point in path]
ydata = [point.item(1) for point in path]
zdata = [f(point.item(0), point.item(1)) for point in path]

ax.scatter(xdata, ydata, zdata, c='black', cmap='viridis', linewidth=0.5, alpha=1)
ax.plot(xdata, ydata, zdata)


plt.show()
