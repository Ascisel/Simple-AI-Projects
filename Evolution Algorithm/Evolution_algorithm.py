import numpy as np
import math


def calc_distance_between_cities(first_city, second_city):
    return math.sqrt((first_city.coordinates[0] - second_city.coordinates[0])**2 + (first_city.coordinates[1] - second_city.coordinates[1])**2)


def calc_route_length(route):               # oblicznie długości całej trasy między miastami
    cities_in_route = route.route
    length = 0
    for i in range(len(cities_in_route)-1):
        j = i + 1
        length += calc_distance_between_cities(cities_in_route[i], cities_in_route[j])

    return length


def evaluate_population(population):        # ustawianie atrybutu length obiektów klasy Route
    for individual in population:
        individual.length = calc_route_length(individual)


def mutation(individual, factor):   # zmieniamy kolejność ( wymieniamy ) losowe chromosomy w liczbie factor
    i = 0
    chosen_indexes = []             # już wybrane indeksy
    chosen_chromosomes = []         # wybrane chromosomy
    while i < factor and len(chosen_indexes) != len(individual.route):
        chosen_index = np.random.randint(len(individual.route))     # wybierz indeks chromosomu
        if chosen_index not in chosen_indexes:                      # jeżeli nie był jeszcze wybrany to kontynuuj
            chosen_indexes.append(chosen_index)
            chosen_chromosomes.append(individual.route[chosen_index])   # dodaj go do chromosomów oraz jego indeks do już wybranych indeksów
            i += 1
    np.random.shuffle(chosen_indexes)                               # przelosowanie chromosomów w liście
    j = 0
    for index in chosen_indexes:
        individual.route[index] = chosen_chromosomes[j]             # umieszczenie chromosomów na odpowiednich miejscach w genomie
        j += 1

    return Route(individual.route.copy())                           # zwracamy nowy obiekt


def make_population(size, available_chromosomes, genom_name):  # available chromosomes - w naszym przypadku lista dostępnych miast
    population = []
    for i in range(size):
        np.random.shuffle(available_chromosomes)               # losowo ustawiamy chromosomy dla każdego następnego osobnika
        population.append(genom_name(available_chromosomes.copy()))

    return population


def choose_best(population):                                    # zwraca osobnika z najmniejszym atrybutem length z populacji
    best_individual = population[0]
    for individual in population:
        if individual.length < best_individual.length:
            best_individual = individual

    return best_individual


def choose_for_tournament(tournament_size, population):           # wybiera losowe elementy z populacji ( tournament_size elementów)
    chosen_individuals = population.copy()
    np.random.shuffle(chosen_individuals)
    chosen_individuals = chosen_individuals[0:tournament_size]

    return chosen_individuals


class City:
    def __init__(self, coordinates):
        self.coordinates = coordinates  # współrzędne miasta na mapie

    def __str__(self):
        return f"{self.coordinates}"


class Route:    # pojedyncza trasa jest osobnikiem naszej populacji
    def __init__(self, route):
        self.route = route  # lista miast, które po kolei odwiedzamy
        self.length = 0


def evolution_algorithm(population_size, mutation_factor, tournament_size, budget, chromosomes, genom_name): # algorytm ewolucyjny, ganom_name to klasa osobnika naszej populacji
    basic_population = make_population(population_size, chromosomes, genom_name)
    evaluate_population(basic_population)                                                                     # oceniamy jakość osobników populacji bazowej
    budget -= population_size                                                                                 # oceniamy całą populację więc odejmujemy od budżetu rozmiar populacji
    t = 0                                                                                                     # licznik pokoleń
    current_population = basic_population
    while budget > 0:
        temp_population = []
        for i in range(population_size):
            players = choose_for_tournament(tournament_size, current_population)                               # wybieramy osobniki do turnieju
            best = choose_best(players)                                                                        # wybieramy najlepszego z tych osobników
            temp_population.append(best)
        current_population = temp_population
        for i in range(population_size):
            current_population[i] = mutation(current_population[i], mutation_factor)                           # poddajemy mutacji każdy z elementów
        evaluate_population(current_population)                                                                # ocena populacji
        budget -= population_size                                                                              # kolejne zubożenie budżetu po ocenie
        t += 1
                                                                                                               # kolejnym pokoleniem jest to po mutacji - sukcesja generacyjna
    return current_population, basic_population, t


if __name__ == "__main__":
    pass
