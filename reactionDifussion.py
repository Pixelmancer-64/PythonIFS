from math import floor
import uuid
from PIL import Image, ImageDraw
import numpy as np
from numba import njit
from attractorAnalysis import SIF, performance

run_id = uuid.uuid1()

image = Image.new('RGB', (100, 100))
draw_image = ImageDraw.Draw(image)
width, height = image.size

grid = np.array([[{'a': 1, 'b': 0} for y in range(height)]
                for x in range(width)])
grid[floor(height/2)][floor(width/2)]['b'] = 40


def laplace(x, y, k):
    aux = 0
    aux += grid[x][y][k] * -1
    aux += grid[x - 1][y][k] * .2
    aux += grid[x + 1][y][k] * .2
    aux += grid[x][y + 1][k] * .2
    aux += grid[x][y - 1][k] * .2
    aux += grid[x + 1][y - 1][k] * .05
    aux += grid[x - 1][y - 1][k] * .05
    aux += grid[x - 1][y + 1][k] * .05
    aux += grid[x + 1][y + 1][k] * .05

    return aux


@SIF
@performance
def draw():
    da = 1
    db = .5
    f = .055
    k = .062
    print(f'Processing run_id: {run_id}')

    for x in range(999):
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

                grid[i][j]['a'] = newA
                grid[i][j]['b'] = newB

                color = grid[i][j]['a'] - grid[i][j]['b']
                color = floor(color * 255)
                rectangle_shape = [
                    (j, i),
                    (j, i)]

                draw_image.rectangle(
                    rectangle_shape,
                    fill=(
                        color,
                        color,
                        color
                    )
                )

    image.save(f'./output/{run_id}.png')
