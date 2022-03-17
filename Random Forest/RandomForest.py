from DecisionTree import DecisionTree
import numpy as np


class RandomForest:
    def __init__(self):
        self.classes = []
        self.forest = []

    # losowy wybór atrybutów ( bez zwracania )

    def selectAttributes(self, nOfAttributesToChoose, dataSet):
        selectedAttributes = []
        indexesOfAttributes = [index for index in range(1, len(dataSet[0]))]
        for i in range(nOfAttributesToChoose):
            np.random.shuffle(indexesOfAttributes)
            selectedAttributes.append(indexesOfAttributes.pop())

        return selectedAttributes

    # losowy wybór próbek ( ze zwracaniem )

    def selectSpecs(self, nOfElementsToChoose, dataSet):
        selectedSpecs = []
        for i in range(nOfElementsToChoose):
            randomIndex = np.random.randint(len(dataSet))
            selectedSpecs.append(dataSet[randomIndex])

        return selectedSpecs

    # odpowiednia obróbka próbek potrzebnych do stworzenia losowego drzewa

    def selectData(self, attributes, dataset):
        selectedData = []
        attributes.sort()
        for line in dataset:
            templine = [0 for i in range(len(line))]
            templine[0] = line[0]
            for attribute in attributes:
                templine[attribute] = line[attribute]
            selectedData.append(templine)

        return selectedData

    # przy pomocy powyższych metod stwórz losowy zbiór na którego podstawie stworzysz numberOfTrees drzew o parametrach podanych a argumentach wywołania

    def trainRandomForest(self, numberOfTrees, numberOfAttributes, dataSet):
        for i in range(numberOfTrees):
            selectedSpecs = self.selectSpecs(numberOfTrees*10, dataSet.copy())
            selectedAttributes = self.selectAttributes(numberOfAttributes, dataSet.copy())
            selectedData = self.selectData(selectedAttributes, selectedSpecs)
            self.forest.append(DecisionTree(selectedData))

    # znajdź najczęstsza klasę w zbiorze

    def findMostFreqClass(self, resultList):
        resultSet = set(resultList)
        best_result = 0
        best_class = None
        for item in resultSet:
            count = 0
            for result in resultList:
                if item == result:
                    count += 1
            if count > best_result:
                best_result = count
                best_class = item

        return best_class

    # na podstawie stworzonego lasu spróbuj zaklasyfikować próbkę do danej klasy

    def predictRandomForest(self, inputVector):
        results = []
        for tree in self.forest:
            results.append(tree.predict(inputVector))
        return self.findMostFreqClass(results)

# funkcje użyte przy testowaniu walidacji


def podziel_zbior(zbior, k):
    podzielony_zbior = []
    wielkosc_zbioru = len(zbior)
    wielkosc_podzialu = int(wielkosc_zbioru/k)
    if wielkosc_zbioru % k != 0:
        wielkosc_podzialu += 1
    for i in range(k):
        podzial1 = wielkosc_podzialu * i
        podzial2 = wielkosc_podzialu * (i+1)
        podzielony_zbior.append(zbior[podzial1:podzial2])

    return podzielony_zbior


def odejmij_zbior(odjemnik, odjemna):
    zbior = odjemna.copy()
    for item in odjemnik:
        zbior.remove(item)

    return zbior


if __name__ == "__main__":
    pass
