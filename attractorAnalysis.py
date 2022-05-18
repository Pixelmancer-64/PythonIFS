import math
from time import time
from collections import Counter

a = -1.32
b = -1.65
c = 0.74
d = 1.81

y = 0
x = 0


def performance(callback):
    def wrapper(*args, **kargs):
        time0 = time()
        aux = callback(*args, **kargs)
        time1 = time()
        print(f'\n********\n{time1-time0} s\n********')
        return aux
    return wrapper


def SIF(callback):
    def wrapper(*args, **kargs):
        return callback(*args, **kargs)
    return wrapper()


def clifford(num):
    x = 0
    y = 0

    for i in range(num):
        yield x, y
        xPrev = x
        yPrev = y

        x = math.sin(a*yPrev) + c*math.cos(a*xPrev)
        y = math.sin(b*xPrev) + d*math.cos(b*yPrev)


@performance
def test():
    aux = []
    for x, y in clifford(9999999):
        aux.append(y)

    aux.sort()
    print(aux[0])
    print(aux[len(aux)-1])

@performance
def realTest():
    coords = []
    for x, y in clifford(999):
        coords.append((round(x), round(y)))

    aux = []
    histogram = Counter(coords)
    for i in histogram:
        aux.append(histogram[i])
    aux.sort()

    print(aux)
    print(len(aux))

    print("Maior: ", aux[len(aux)-1])
