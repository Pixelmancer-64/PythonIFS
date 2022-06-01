from math import floor
import random
import uuid
from PIL import Image, ImageDraw
run_id = uuid.uuid1()

image = Image.new('RGB', (400, 400))
draw_image = ImageDraw.Draw(image)
width, height = image.size

grid = [[{'a': 1, 'b': 0} for y in range(height)] for x in range(width)]
nextGrid = [[{'a': 1, 'b': 0} for y in range(height)] for x in range(width)]

def draw(times):
    global grid
    global nextGrid
    da = 1
    db = .5
    f = .055
    k = .062
    print(f'Processing run_id: {run_id}')

    for x in range(times):
        print(x)
        for i in range(height - 1):
            for j in range(width - 1):
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

                nextGrid[i][j]['a'] = newA
                nextGrid[i][j]['b'] = newB

                color = floor(nextGrid[i][j]['a'] - nextGrid[i][j]['b'])

                rectangle_shape = [
                    (j, i),
                    (j + 1, i + 1)]
                draw_image.rectangle(
                    rectangle_shape,
                    fill=(
                        color * 255,
                        color * 255,
                        color * 255
                    )
                )
        aux = grid
        grid = nextGrid
        nextGrid = aux

    image.save(f'./output/{run_id}.png')


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


grid[200][200] = {'a': 0, 'b': 1}
draw(1000)
