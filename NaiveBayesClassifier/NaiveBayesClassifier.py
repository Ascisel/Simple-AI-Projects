import math
import numpy as np


class BayesNaiveClassifier:

    def __init__(self):
        self.learning_data = None
        self.parameters_data = []
        self.no_of_param = 0
        self.classes = []
        self.ex_for_classes = []
        self.vx_for_classes = []
        self.classes_probablity = []

    def organize_the_data(self):    # stworz tablice dla kazdego parametru ktorej element bedzie posiadal jego wartosc oraz klase do ktorej nalezy
        first_line = self.learning_data[0]
        self.no_of_param = len(first_line) - 1
        for i in range(self.no_of_param):
            parametr_list = []
            for line in self.learning_data:
                parametr_list.append((float(line[i]), int(line[self.no_of_param]))) # zmień format danych na bardziej przystepny do obliczen
                if int(line[self.no_of_param]) not in self.classes:
                    self.classes.append(int(line[self.no_of_param]))
            self.parameters_data.append(parametr_list)

    def calculate_param_EX(self, spec_class, params):
        count_param = 0
        value = 0
        for param in params:
            if param[1] == spec_class:
                value += param[0]
                count_param += 1

        return value/count_param

    def calculate_param_VX(self, spec_class, params, ex):
        count_param = 0
        value = 0
        for param in params:
            if param[1] == spec_class:
                value += (param[0] - ex)**2
                count_param += 1

        return value/count_param

    def gauss(self, vx, ex, param):
        return (1 / (math.sqrt(2 * vx * math.pi))) * math.exp(-1 * ((param - ex) ** 2) / (2 * vx))

    def calculate_class_EXVX(self, spec_class):
        class_ex = []
        class_vx = []
        for params in self.parameters_data:
            ex = self.calculate_param_EX(spec_class, params)
            class_ex.append(ex)
            class_vx.append(self.calculate_param_VX(spec_class, params, ex))

        return class_ex, class_vx

    def calc_classes_probability(self):
        classes_prob = []
        nr_of_spec = 0
        for spec_class in self.classes:
            classes_prob.append(0)
        for item in self.parameters_data[0]:
            nr_of_spec += 1
            for i, spec_class in enumerate(self.classes, start=0):
                if item[1] == spec_class:
                    classes_prob[i] += 1
        for j in range(len(classes_prob)):
            classes_prob[j] /= nr_of_spec

        return classes_prob

    def learn(self, learnig_data):
        self.learning_data = learning_data
        self.organize_the_data()        # przetwarzanie odpowiednio danych 
        self.classes_probablity = self.calc_classes_probability()   # prawdopodobieństwo wystapienia danej klasy
        for class_id in self.classes:
            result = self.calculate_class_EXVX(class_id)        # oblicz wartosci wariancji oraz wartosci sredniej dla kazdego parametru kazdej klasy
            self.ex_for_classes.append(result[0])
            self.vx_for_classes.append(result[1])

    def predict_spec(self, specimen):
        prob_of_classes = []
        for j in range(len(self.classes)):  # policz prawdopodobienstwa dla kazdej klasy
            prob_of_class = self.classes_probablity[j]
            for i, parameter in enumerate(specimen[:len(specimen) - 1], start=0):
                prob_of_class *= self.gauss(self.vx_for_classes[j][i], self.ex_for_classes[j][i], float(parameter)) # dla każdego parametru policz wartosci funkcji gestosci
            prob_of_classes.append(prob_of_class)

        sum_of_probs = sum(prob_of_classes)
        for ii in range(len(prob_of_classes)):
            prob_of_classes[ii] /= sum_of_probs

        return prob_of_classes

    def predict(self, specimen):
        result = self.predict_spec(specimen)
        for i in range(len(result)):            # wybierz klase ktora ma najwieksze prawdopodobienstwo
            if max(result) == result[i]:
                return self.classes[i]


def select_data(filename, percent, do_random):
    data = []
    classes = []
    learning_data = []
    data_to_predict = []
    with open(filename) as f:
        for line in f:
            data.append(line.split())
    data_len = len(data[0])
    for item in data:
        if item[data_len - 1] not in classes:
            classes.append(item[data_len - 1])
    if percent <= 100 and percent >= 0:
        num = len(data) * percent / 100
        num = int(num)
    if do_random:   # jeżeli losowo to przemieszaj data
        np.random.shuffle(data)
        learning_data = data[:num]
        data_to_predict = data[num:]
        return learning_data, data_to_predict
    num = num / len(classes)
    for spec_class in classes:  # dla każdej klasy wybierz tyle samo elementów
        i = 0
        curr_num = num
        while spec_class != data[i][data_len - 1]:
            i += 1
        while curr_num > 0:
            learning_data.append(data[i])
            curr_num -= 1
            i += 1
    for item in data:
        if item not in learning_data:
            data_to_predict.append(item)

    return learning_data, data_to_predict


if __name__ == "__main__":
    pass
