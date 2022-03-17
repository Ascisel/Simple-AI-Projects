import math

# klasa reprezentująca obiekt węzła w drzwie decyzyjnym


class Node:
    def __init__(self, parent, infSet):
        self.nodeSet = infSet       # zbiór danych dla danego węzła
        self.parent = parent
        self.lChild = None
        self.rChild = None
        self.condition = None       # warunek w węźle
        self.leaf = False           # oznaczenie czy węzeł jest liściem
        self.leafClass = None       # klasa jaką przechowuje liść

    def set_condition(self, division):  # metoda set służaca do ustalenia atrybutu conddition
        self.condition = division


# klasa reprezentująca obiekt drzewa decyzyjnego


class DecisionTree:
    def __init__(self, dataset):
        self.root = None                # korzeń
        self.classes = []               # lista klas w danych w danym drzewie
        self.deep = 0                   # głębokość drzewa
        self.madeTree(dataset)          # podczas wywołania konstruktora na podstawie podanego zbioru tworzona jest struktura drzewa

    def madeTree(self, infSet):         # tworzenie drzewa od korzenia
        self.root = Node(None, infSet)
        self.classes = self.findClasses(infSet)
        self.deep += 1
        self.madeTreeRecursive(self.root)

    def madeTreeRecursive(self, node):      # rekurencyjne tworzenie drzewa
        for specClass in self.classes:          # kończ jeżeli wszystkie próbki w węźle jednej klasy
            if self.specCounter(node.nodeSet, specClass) == len(node.nodeSet):
                node.leaf = True
                node.leafClass = specClass
                return
        nodeDivisions = self.set_divisions(node.nodeSet)
        if nodeDivisions == []:             # kończ jeżeli dla węzła nie ma dostępnych podziałów, wybierz częstszą klasę w węźle
            node.leaf = True
            node.leafClass = self.mostFreqClass(node.nodeSet)
            return
        bestDivision = self.findBestDivision(nodeDivisions, node.nodeSet)   # znajdź najlepszy podział
        dividedSets = self.divideSet(bestDivision, node.nodeSet)    # podziel według najlepszego podziału
        node.set_condition(bestDivision)                            # ustal warunek w węźle
        node.lChild = Node(node, dividedSets[0])                    # dla podzielonego zbioru według podziały wywołaj funkcję dla prawego i lewego dziecka
        node.rChild = Node(node, dividedSets[1])
        self.deep += 1
        self.madeTreeRecursive(node.lChild)
        self.deep += 1
        self.madeTreeRecursive(node.rChild)

    def findClasses(self, infSet):      # ustal jakie klasy są przedstawiane przez dane testowe
        classes = []
        for line in infSet:
            if line[0] not in classes:
                classes.append(line[0])

        return classes

    def specCounter(self, nodeSet, specClass):      # policz ile próbek konkretnej klasy jest w zbiorze
        count = 0
        for i in nodeSet:
            if i[0] == specClass:
                count += 1

        return count

    def mostFreqClass(self, infSet):        # wybierz najczęstszą klase ze zbioru
        mostFreqClass = None
        bestResult = 0
        for specClass in self.classes:
            nOfSpecForClass = self.specCounter(infSet, specClass)
            if nOfSpecForClass > bestResult:
                bestResult = nOfSpecForClass
                mostFreqClass = specClass

        return mostFreqClass

    def findBestDivision(self, divisions, infSet):      # na podstawie entropii wybierz najlepszy podział dla tego zbioru
        bestDivision = None
        bestRate = -math.inf
        bestAttribute = self.findBestAttributeToDivideSet(infSet)
        for division in divisions:
            if division[0] == bestAttribute:
                rate = self.infGain(division, infSet)
                if rate > bestRate:
                    bestRate = rate
                    bestDivision = division

        return bestDivision

    # przyjęta metoda wyboru atrybutu do podziału

    def findBestAttributeToDivideSet(self, infSet):     # obliczając wartości średnie oraz wariancje dla każdego atrybutu wybierz ten którego iloraz wariancji i wartości średniej jest największy
        bestVX = 0
        bestAttribute = None
        for i in range(1, len(infSet[0])):
            ex = 0
            vx = 0
            for line in infSet:
                ex += line[i]
            ex /= len(infSet)
            for line2 in infSet:
                vx += (line2[i] - ex)**2
            vx /= (len(infSet) - 1)
            if ex != 0 and vx/ex > bestVX:
                bestVX = vx/ex
                bestAttribute = i

        return bestAttribute

    # obliczanie entropii 

    def calcSetEntropy(self, infSet):
        entropy = 0
        for specClass in self.classes:
            nOfSpecForClass = self.specCounter(infSet, specClass)
            if nOfSpecForClass != 0:
                class_freq = nOfSpecForClass/len(infSet)
                entropy += (class_freq) * math.log(class_freq)

        return -entropy

    def calcDividedSetEntropy(self, division, infSet):
        inf = 0
        for dividedSet in self.divideSet(division, infSet):
            inf += (len(dividedSet)/len(infSet)) * self.calcSetEntropy(dividedSet)

        return inf

    def infGain(self, division, infSet):
        return self.calcSetEntropy(infSet) - self.calcDividedSetEntropy(division, infSet)

    # podział podanego zbioru według podanego warunku

    def divideSet(self, division, infSet):
        dividedSets = [[], []]
        for specimen in infSet:
            if specimen[division[0]] < division[1]:
                dividedSets[0].append(specimen)
            else:
                dividedSets[1].append(specimen)

        return dividedSets

    # znajdź możliwe podziały w danym secie dla wartości ciągłych

    def set_divisions(self, infSet):
        divisions = []
        for i in range(1, len(infSet[0])):
            sortedParameterData = []
            for j in range(len(infSet)):
                sortedParameterData.append(infSet[j][i])
            sortedParameterData.sort()
            for ii in range(len(sortedParameterData) - 1):
                if sortedParameterData[ii] != sortedParameterData[ii + 1]:
                    division = (sortedParameterData[ii] + sortedParameterData[ii + 1]) / 2
                    divisions.append((i, division))

        return divisions

    # na podstawie zbudowanego drzewa określ do jakiej klasy należy podana w argumencie wywołania próbka

    def predict(self, specimen):
        node = self.root
        while node.leaf is not True:
            if specimen[node.condition[0]] < node.condition[1]:
                node = node.lChild
            else:
                node = node.rChild

        return node.leafClass


if __name__ == "__main__":
    pass
