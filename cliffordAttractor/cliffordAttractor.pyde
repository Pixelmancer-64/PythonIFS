from collections import Counter
from numba import jit 

a,b,c,d = [-1.3, -1.3, -1.8, -1.9]

def setup():
    fullScreen()
    #size(500,500)
    background(255)
    
def clifford(num):
    x = 0
    y = 0

    for i in range(num):
        yield x, y
        xPrev = x
        yPrev = y

        x = sin(a*yPrev) + c*cos(a*xPrev)
        y = sin(b*xPrev) + d*cos(b*yPrev)

def draw():
    noLoop()
    n = 99999
    xl = []
    yl = []
    
    for x, y in clifford(9999):
        xl.append(x)
        yl.append(y)
        
    xl.sort()
    yl.sort()
    
    for x, y in clifford(n):
        xb = map(x, xl[0], xl[len(xl)-1], 0, width)
        yb = map(y, yl[0], yl[len(yl)-1], 0, height)
        point(xb, yb)
    
