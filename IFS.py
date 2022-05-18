from sys import argv
import numpy as np
import pandas as pd
import datashader as ds
from random import random, choice, randint, uniform
from datashader import transfer_functions as tf
from datashader.colors import inferno, viridis, Greys9, Hot
from datashader.utils import export_image
from numba import njit
from math import sin, cos, sqrt, fabs
from datetime import date
from attractorAnalysis import SIF, performance


@njit
def Clifford(x, y, a, b, c, d, *o):
    return sin(a * y) + c * cos(a * x), sin(b * x) + d * cos(b * y)


@njit
def Souls(x, y, a, b, c, d, *o):
    return y - sqrt(abs(b * x - 1 - c)) * cos(x) * random(), a - x * sin(y)


@njit
def Bedhead(x, y, a, b, *o):
    return sin(x*y/b)*y + cos(a*x-y), \
        x + sin(y)/b


@njit
def RandomIFS(x, y, a, b, c, d, e, f, t):
    a, b, c, d, e, f = t[randint(0, len(t)-1)]
    return a * x + b * y + c, d * x + e * y + f


@njit
def Svensson(x, y, a, b, c, d, *o):
    return d * sin(a * x) - sin(b * y), \
        c * cos(a * x) + cos(b * y)


@njit
def Tree(x, y, a, b, c, d, *o):
    # r, s, theta, phi, e, f, p
    t = np.array([
        [0.05, 0.6,   0,      0,       0, 0, ],
        [0.05, -0.5,  0,      0,       0, 1, ],
        [0.6,  0.5,   0.698,  0.698,   0, 0.6],
        [0.5,  0.450, 0.349,  0.3492,  0, 1.1],
        [0.5,  0.55,  -0.524, -0.524,  0, 1],
        [0.55, 0.4,   -0.698,  -0.698, 0, 0.7],
    ])

    t = t[randint(0, len(t)-1)]

    return t[0] * cos(t[2]) * x - t[1] * sin(t[3]) * y + t[4], \
        t[0] * sin(t[2]) * x + t[1] * cos(t[3]) * y + t[5]


@njit
def Fern(x, y, a, b, c, d, *o):
    r = random()
    if (r < 0.01):
        return 0, 0.2 * y - 0.12
    elif (r < 0.86):
        return 0.845 * x + 0.035 * y, -0.035 * x + 0.82 * y + 1.6
    elif (r < 0.93):
        return 0.2 * x + -0.31 * y, 0.255 * x + 0.245 * y + 0.29
    else:
        return -0.15 * x + 0.24 * y, 0.25 * x + 0.2 * y + 0.68


@njit
def De_Jong(x, y, a, b, c, d, *o):
    return sin(a * y) - cos(b * x), sin(c * x) - cos(d * y)

@njit
def Fractal_Dream(x, y, a, b, c, d, *o):
    return sin(y*b)+c*sin(x*b), sin(x*a)+d*sin(y*a)


@njit
def Hopalong1(x, y, a, b, c, *o):
    return y - sqrt(fabs(b * x - c)) * np.sign(x), a - x


@njit
def Hopalong2(x, y, a, b, c, *o):
    return y - 1.0 - sqrt(fabs(b * x - 1.0 - c)) * np.sign(x - 1.0), a - x - 1.0




@njit
def trajectory_coords(fn, n, x0, y0, a=0, b=0, c=0, d=0, e=0, f=0, t=0):
    x, y = np.zeros(n), np.zeros(n)
    x[0], y[0] = x0, y0
    for i in np.arange(n-1):
        x[i+1], y[i+1] = fn(x[i], y[i], a, b, c, d, e, f, t)
    return x, y


def trajectory(fn, n, x0, y0, a=0, b=0, c=0, d=0, e=0, f=0, t=0):
    x, y = trajectory_coords(fn, n, x0, y0, a, b, c, d, e, f, t)
    return pd.DataFrame(dict(x=x, y=y))


@SIF
@performance
def attractor():
    # Fern, Tree
    IFSs = [Svensson, Bedhead, Souls, Clifford, RandomIFS,
            De_Jong, Hopalong1, Hopalong2, Fractal_Dream]
    Cmaps = [inferno, viridis, Greys9, Hot]

    for i in range(int(argv[1])):
        theIFS = choice(IFSs)
        initialCords = choice([0, 1, .5, 0.01])
        print(theIFS.__name__, initialCords)
        theCmap = choice(Cmaps)
        n = 100000000
        a = uniform(-10, 10)
        b = uniform(-10, 10)
        c = uniform(-10, 10)
        d = uniform(-10, 10)
        e = uniform(-10, 10)
        f = uniform(-10, 10)

        t = np.array([
            [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1),
             uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)],
            [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1),
             uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)],
            [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1),
             uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)],
            [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1),
             uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)],
        ])

        df = trajectory(theIFS, n, initialCords, initialCords, a, b, c, d, e, f, t)
        cvs = ds.Canvas(plot_width=4000, plot_height=4000)
        agg = cvs.points(df, 'x', 'y')

        ds.transfer_functions.Image.border = 0

        img = tf.shade(agg, theCmap)

        export_image(img, f"{date.today()}-{theIFS.__name__},{a},{b},{c},{d},{e},{f}-{initialCords}",
                     export_path="./attractors")
