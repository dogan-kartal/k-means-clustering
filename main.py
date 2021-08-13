import math
import sys
from random import shuffle, uniform, choice
from matplotlib import pyplot



def ReadData(fileName):

    f = open(fileName, 'r')
    lines = f.read().splitlines()
    f.close()

    items = []

    for i in range(1, len(lines)):
        line = lines[i].split(',')
        itemFeatures = []

        for j in range(len(line) - 1):
            v = float(line[j])
            itemFeatures.append(v)

        items.append(itemFeatures)

    shuffle(items)

    return items



def FindColMinMax(items):
    n = len(items[0])
    minima = [sys.maxsize for i in range(n)]
    maxima = [-sys.maxsize - 1 for i in range(n)]

    for item in items:
        for f in range(len(item)):
            if (item[f] < minima[f]):
                minima[f] = item[f]

            if (item[f] > maxima[f]):
                maxima[f] = item[f]

    return minima, maxima


def EuclideanDistance(x, y):
    sum = 0
    for i in range(len(x)):
        sum += math.pow(x[i] - y[i], 2)

    return math.sqrt(sum)


def InitializeMeans(items, k, cMin, cMax):


    f = len(items[0]) 
    means = [[0 for i in range(f)] for j in range(k)]

    for mean in means:
        for i in range(len(mean)):

            mean[i] = uniform(cMin[i] + 1, cMax[i] - 1)

    return means

def FindClusters(means, items):
    clusters = [[] for i in range(len(means))]

    for item in items:

        index = Classify(means, item)


        clusters[index].append(item)

    return clusters


def UpdateMean(n, mean, item):
    for i in range(len(mean)):
        m = mean[i]
        m = (m * (n - 1) + item[i]) / float(n)
        mean[i] = round(m, 3)

    return mean


def Classify(means, eleman):


    minimum = sys.maxsize
    index = -1

    for i in range(len(means)):
        
        dis = EuclideanDistance(eleman, means[i])

        if (dis < minimum):
            minimum = dis
            index = i

    return index

def CalculateMeans(k, items, maxIterations=100000):

    cMin, cMax = FindColMinMax(items)


    means = InitializeMeans(items, k, cMin, cMax)



    clusterSizes = [0 for i in range(len(means))]


    belongsTo = [0 for i in range(len(items))]


    for e in range(maxIterations):

        noChange = True
        for i in range(len(items)):
            item = items[i]


            index = Classify(means, item)

            clusterSizes[index] += 1
            means[index] = UpdateMean(clusterSizes[index], means[index], item)


            if (index != belongsTo[i]):
                noChange = False

            belongsTo[i] = index


        if (noChange):
            break

    return means

def DrawClusters(clusters):
    n = len(clusters)

    X = [[] for i in range(n)]

    for i in range(n):
        cluster = clusters[i]
        for item in cluster:
            X[i].append(item)

    colors = ['r','b','g','c','m','y']

    for x in X:


        c = choice(colors)
        colors.remove(c)

        Xa = []
        Xb = []

        for item in x:
            Xa.append(item[0])
            Xb.append(item[1])

        pyplot.plot(Xa,Xb,'o',color=c)

    pyplot.show()



items = ReadData('data.txt')

k = 3

means = CalculateMeans(k, items)
clusters = FindClusters(means, items)

DrawClusters(clusters)


