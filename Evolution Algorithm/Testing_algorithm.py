import matplotlib.pyplot as plt
import numpy as np
import math
from Evolution_algorithm import evolution_algorithm, City, Route, choose_best

# słownik schematów

Cities_lokations_diagrams = {
    "3 groups": [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (4, 2), (1, 3), (2, 3), (3, 3),
                 (15, 1), (16, 1), (17, 1), (14, 2), (15, 2), (16, 2), (17, 2), (15, 3), (16, 3), (17, 3),
                 (9, 12), (8, 13), (9, 13), (10, 13), (8, 14), (9, 14), (10, 14), (8, 15), (9, 15), (10, 15)],
    "6 groups": [(0, 1), (1, 0), (1, 1), (2, 1), (1, 2), (9, 0), (8, 1), (9, 1), (10, 1), (9, 2),
                 (0, 9), (1, 8), (1, 9), (2, 9), (1, 10), (9, 8), (8, 9), (9, 9), (10, 9), (9, 10),
                 (0, 17), (1, 16), (1, 17), (2, 17), (1, 18), (9, 16), (8, 17), (9, 17), (10, 17), (9, 18)],
    "2 groups": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                 (2, 0), (2, 1),(2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                 (19, 0), (19, 1), (19, 2), (20, 0), (20, 1), (20, 2), (21, 0), (21, 1), (21, 2), (18, 1)]
}


def make_random_setup(number_of_points, x_max, y_max):  # tworzy i zwraca listę o długości number_of_points krotek o losowych parametrach 0 oraz 1 z przedziału x_max, y_max
    cords = []
    for i in range(number_of_points):
        x = np.random.randint(x_max)
        y = np.random.randint(y_max)
        cords.append((x, y))

    return cords


def make_chessmap_setup():  # tworzy i zwraca listę z 30 punktów tworzących regularną siatkę o wymiarach 5x6
    cords = []
    for i in range(5):
        for j in range(6):
            cords.append((2*i, 2*j))

    return cords


def make_line_setup(number_of_points):  # tworzy i zwraca listę punktów leżących w jednej linii w równych odległościach
    cords = []
    for i in range(number_of_points):
        cords.append((i, 0))

    return cords


def make_circle_setup(number_of_points, radius):    # tworzy i zwraca listę punktów na okręgu o promieniu radius o środku w punkcie (0, 0)
    cords = []
    for i in range(number_of_points):
        alpha = 2 * math.pi * np.random.random()
        x = radius * math.cos(alpha)
        y = radius * math.sin(alpha)

        cords.append((x, y))

    return cords


def combinate_cities_from_points(points):   # tworzy z listy punktów listę objektów klasy City o atrybutach coordinate zgodnych z listą punktów
    cities = []
    for point in points:
        cities.append(City(point))

    return cities


def create_points_plot(points, x_range, y_range, do_plot=False):    # tworzy wizualizację 3D podanych punktów z listy
    ax = plt.axes(projection='3d')

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    xdata = [point[0] for point in points]
    ydata = [point[1] for point in points]

    ax.scatter(xdata, ydata, 0, c='black', cmap='viridis', linewidth=0.5, alpha=1, s=20)

    ax.set_zlim(0, 1)
    ax.set_xlim(-x_range, x_range)
    ax.set_ylim(-x_range, y_range)

    if do_plot:
        ax.plot(xdata, ydata, 0)


    plt.show()


if __name__ == "__main__":
    pass
