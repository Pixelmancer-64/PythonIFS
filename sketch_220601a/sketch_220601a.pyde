sizeX = 100
sizeY = 100

grid = [[{'a': 1, 'b': 0} for y in range(sizeY)] for x in range(sizeX)]

def setup():
    start()
    size(sizeX,sizeY)

def draw():
    global grid
    da = 1
    db = 0.5
    f = 0.055
    k = 0.062

    print(frameCount)
    for i in range(sizeY - 1):
        for j in range(sizeX - 1):
            a = grid[i][j]['a']
            b = grid[i][j]['b']
            newA = a + (da * laplace(i, j, 'a')) - \
                (a * b * b) + (f * (1 - a))
            newB = b + (db * laplace(i, j, 'b')) + \
                (a * b * b) - ((k + f) * b)
            
            if newA < 0:
                newA = 0
            elif newA > 1:
                newA = 1
            
            if newB < 0:
                newB = 0
            elif newB > 1:
                newB = 1
                
            grid[i][j]['a'] = newA
            grid[i][j]['b'] = newB

            color = floor(grid[i][j]['a'] - grid[i][j]['b'])
            stroke(color * 255)
            rect(j, i, 1, 1)
            
def start():
    grid[floor(sizeY/2)][floor(sizeX/2)]['b'] = 40


def laplace(x, y, k):
    sum = 0
    sum += grid[x][y][k] * -1
    sum += grid[x - 1][y][k] * .2
    sum += grid[x + 1][y][k] * .2
    sum += grid[x][y + 1][k] * .2
    sum += grid[x][y - 1][k] * .2
    sum += grid[x + 1][y - 1][k] * .05
    sum += grid[x - 1][y - 1][k] * .05
    sum += grid[x - 1][y + 1][k] * .05
    sum += grid[x + 1][y + 1][k] * .05

    return sum
