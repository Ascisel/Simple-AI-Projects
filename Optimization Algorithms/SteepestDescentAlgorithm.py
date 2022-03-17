from sympy import *
import math
import numpy as np


def calc_gradient(funct, point):  # funkcja wyliczająca gradient w podanym punkcie
    x, y = symbols('x y')         # ustawienie x oraz y jako zmienne matematyczne
    f_prime_x = funct.diff(x)     # pochodna z podanej funkcji po x
    f_prime_y = funct.diff(y)     # pochodna z podanej funckji po y

    return np.matrix([[f_prime_x.subs([(x, point.item(0)), (y, point.item(1))])],[f_prime_y.subs([(x, point.item(0)), (y, point.item(1))])]], dtype='float') # zwracamy gradient w postaci macierzy 2x1


def SteepestDescentAlgorithm(function, starting_point, epsG, betha, max_iterations):
    x, y = symbols('x y')
    path = [starting_point]  # sciezka algorytmu, juz na starcie dodajemy punkt startowy
    func = lambda x1, y1: function.subs([(x, x1), (y, y1)])  # zapisujemy funkcję w takiej postaci aby łatwo wyliczać jej wartość
    k = 1   # liczba kroków
    while k <= max_iterations:  # warunek stopu - warunek maksymalnej liczy iteracji
        gradient = calc_gradient(function, starting_point)  # obliczanie gradientu dla podanej funkcji i punktu startowego
        current_point = starting_point + betha * -1 * gradient  # obliczanie współrzędnych punktu po przesunięciu o wyliczony krok
        path.append(current_point)  # dodanie wyznaczonego punktu do ścieżki
        if abs(func(starting_point.item(0), starting_point.item(1)) - func(current_point.item(0), current_point.item(1))) <= epsG:  # warunek stopu - sprawdzenie wartości funkcji dla dwóch kolejnych punktów i porównanie go do wyznaczonej granicy
            return path  # zwtacamy ścieżkę
        k += 1  # zwiększamy liczbę kroków
        starting_point = current_point  # ustawiamy jako punkt startowy dla następnej iteracji nowo wyznaczony punkt

    return path  # zwracamy ścieżkę


if __name__ == "__main__":
    x, y = symbols('x y')
    f = (x**2 + y - 11)**2 + (x + y**2 - 7)**2
    start = np.matrix([[2], [2]])
    path = SteepestDescentAlgorithm(f, start, 10**-8, 0.01, 10000)
    print(path[(len(path)-1)])
