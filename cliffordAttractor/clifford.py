a = -1.32
b = -1.65
c = 0.74
d = 1.81

x = 0
y = 0

def setup():
    size(500,500)
    background(255)
    stroke(0)
    
def clifford():
    return sin(a*y) + c * cos(a*x), sin(b*x) + d * cos(b * y)

def draw():
    global x
    global y
     
    for i in range(999):
         xb = map(x, -1.2981013006324171, 1.7399991891975277, 0, width)
         yb = map(y, -2.809999553604871, 2.8099834609084327, 0, height)
         point(xb, yb)
         x, y = clifford()