from sympy import *
import numpy as np


def calc_gradient(funct, point):
    x, y = symbols('x y')
    f_prime_x = funct.diff(x)
    f_prime_y = funct.diff(y)

    return np.matrix([[f_prime_x.subs([(x, point.item(0)), (y, point.item(1))])], [f_prime_y.subs([(x, point.item(0)), (y, point.item(1))])]], dtype='float')


def calc_hessian_matrix(funct, point):
    x, y = symbols('x y')
    deriv_xx = funct.diff(x).diff(x).subs([(x, point.item(0)), (y, point.item(1))])  # obliczamy drugą pochodną po x dla podanego punktu
    deriv_yy = funct.diff(y).diff(y).subs([(x, point.item(0)), (y, point.item(1))])  # obliczamy drugą pochodną po y dla podanego punktu
    deriv_xy = funct.diff(x).diff(y).subs([(x, point.item(0)), (y, point.item(1))])  # obliczamy pochodną y z pochodnej po x dla podanego punktu

    return np.matrix([[deriv_xx, deriv_xy], [deriv_xy, deriv_yy]], dtype='float')  # zwracamy macierz hessianu 2x2


def NewtonAlgorithm(function, starting_point, epsG, betha, max_iterations):
    x, y = symbols('x y')
    path = [starting_point]
    func = lambda x1, y1: function.subs([(x, x1), (y, y1)])
    k = 1
    while k <= max_iterations:
        gradient = calc_gradient(function, starting_point)
        inv_hessian = np.linalg.inv(calc_hessian_matrix(function, starting_point))  # obliczanie odwrotności hesjanu dla podanego punktu i funkcji
        d = np.matmul(inv_hessian, gradient)  # obliczenie kroku poprzez pomnożenie odwrotności hesjanu oraz gradientu
        current_point = starting_point + betha * -1 * d  # wyznaczenie kolejnego punktu przesunietego o wyznaczony krok oraz współcznynnik betha
        path.append(current_point)
        if abs(func(starting_point.item(0), starting_point.item(1)) - func(current_point.item(0), current_point.item(1))) <= epsG:
            return path
        k += 1
        starting_point = current_point

    return path


if __name__ == "__main__":
    x, y = symbols('x y')
    f = (x**2 + y - 11)**2 + (x + y**2 - 7)**2
    start = np.matrix([[2], [2]])
    path = NewtonAlgorithm(f, start, 10**-8, 1, 1000)
