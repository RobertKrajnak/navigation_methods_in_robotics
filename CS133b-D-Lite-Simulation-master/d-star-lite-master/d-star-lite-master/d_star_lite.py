import numpy as np
import math

goalX = 1
goalY = 8
robotX = 8
robotY = 4
pos = [goalY, goalX]

openListRhs = []  # rhs
posOpenListRhs = []  # pozicia rhs
gValue = []

numOfDice = 10
grid = np.zeros((numOfDice, numOfDice))

grid[robotY][robotX] = 2
grid[goalY][goalX] = 3
grid[8][3] = 1  # prekazka
grid[7][2] = 1  # prekazka
grid[7][3] = 1  # prekazka

rhs = np.ones((numOfDice, numOfDice)) * np.inf
g = np.ones((numOfDice, numOfDice)) * np.inf
rhs[goalY][goalX] = 0

if rhs[goalY][goalX] != g[goalY][goalX]:
    openListRhs.append(rhs[goalY][goalX])
    posOpenListRhs.append((goalY, goalX))

# naplnenie jednotkami dookola
for r_c in range(numOfDice):
    grid[r_c][9] = 1
    grid[r_c][0] = 1
    grid[9][r_c] = 1
    grid[0][r_c] = 1


# vrati poziciu row/coll objektu goal/robot
def get_position(object, row_column):
    for row in range(numOfDice):
        for col in range(numOfDice):
            if grid[row][col] == object and row_column == 'row':
                return row
            elif grid[row][col] == object and row_column == 'col':
                return col


def UpdateVertex(pos):
    posX = pos[0]
    posY = pos[1]

    # doprava
    if grid[posX][posY + 1] != 1 and rhs[posX][posY + 1] == np.inf:
        rhs[posX][posY + 1] = np.round(math.sqrt(
            (posX - posX) ** 2 + (posY - posY + 1) ** 2) + rhs[posX][posY], 1)
        openListRhs.append(rhs[posX][posY + 1])
        posOpenListRhs.append((posX, posY + 1))
        print("I add euclidian distance right")

    # dolava
    if grid[posX][posY - 1] != 1 and rhs[posX][posY - 1] == np.inf:
        rhs[posX][posY - 1] = np.round(math.sqrt(
            (posX - posX) ** 2 + (posY - posY - 1) ** 2) + rhs[posX][posY], 1)
        openListRhs.append(rhs[posX][posY - 1])
        posOpenListRhs.append((posX, posY - 1))
        print("I add euclidian distance left")

    # hore
    if grid[posX - 1][posY] != 1 and rhs[posX - 1][posY] == np.inf:
        rhs[posX - 1][posY] = np.round(math.sqrt(
            (posX - posX - 1) ** 2 + (posY - posY) ** 2) + rhs[posX][posY], 1)
        openListRhs.append(rhs[posX - 1][posY])
        posOpenListRhs.append((posX - 1, posY))
        print("I add euclidian distance up")

    # dole
    if grid[posX + 1][posY] != 1 and rhs[posX + 1][posY] == np.inf:
        rhs[posX + 1][posY] = np.round(math.sqrt(
            (posX - posX + 1) ** 2 + (posY - posY) ** 2) + rhs[posX][posY], 1)
        openListRhs.append(rhs[posX + 1][posY])
        posOpenListRhs.append((posX + 1, posY))
        print("I add euclidian distance down")

    # doprava-hore
    if grid[posX - 1][posY + 1] != 1 and rhs[posX - 1][posY + 1] == np.inf:
        rhs[posX - 1][posY + 1] = np.round(
            math.sqrt((posX - posX - 1) ** 2 + (posY - posY + 1) ** 2) + rhs[posX][posY], 1)
        openListRhs.append(rhs[posX - 1][posY + 1])
        posOpenListRhs.append((posX - 1, posY + 1))
        print("I add euclidian distance right and up")

    # dolava-hore
    if grid[posX - 1][posY - 1] != 1 and rhs[posX - 1][posY - 1] == np.inf:
        rhs[posX - 1][posY - 1] = np.round(
            math.sqrt((posX - posX - 1) ** 2 + (posY - posY - 1) ** 2) + rhs[posX][posY], 1)
        openListRhs.append(rhs[posX - 1][posY - 1])
        posOpenListRhs.append((posX - 1, posY - 1))
        print("I add euclidian distance left and up")

    # dolava-dole
    if grid[posX + 1][posY - 1] != 1 and rhs[posX + 1][posY - 1] == np.inf:
        rhs[posX + 1][posY - 1] = np.round(
            math.sqrt((posX - posX + 1) ** 2 + (posY - posY - 1) ** 2) + rhs[posX][posY], 1)
        openListRhs.append(rhs[posX + 1][posY - 1])
        posOpenListRhs.append((posX + 1, posY - 1))
        print("I add euclidian distance left and down")

    # doprava-dole
    if grid[posX + 1][posY + 1] != 1 and rhs[posX + 1][posY + 1] == np.inf:
        rhs[posX + 1][posY + 1] = np.round(
            math.sqrt((posX - posX + 1) ** 2 + (posY - posY + 1) ** 2) + rhs[posX][posY], 1)
        openListRhs.append(rhs[posX + 1][posY + 1])
        posOpenListRhs.append((posX + 1, posY + 1))
        print("I add euclidian distance right and down")

    # print(openList)


# while pos != [robotY, robotX]:
i = 0
while i < 13:

    pos = posOpenListRhs[openListRhs.index(min(openListRhs))]

    UpdateVertex(pos)

    print("rhs[pos[1]][pos[0]]: ", rhs[pos[0]][pos[1]])
    print("g[pos[0]][pos[1]]: ", g[pos[0]][pos[1]])



    if g[pos[0]][pos[1]] != rhs[pos[0]][pos[1]]:
        g[pos[0]][pos[1]] = rhs[pos[0]][pos[1]]
        openListRhs.pop(openListRhs.index(min(openListRhs)))
        posOpenListRhs.pop(openListRhs.index(min(openListRhs)))
        print("Mazem min zaznam z openListRhs a z posOpenListRhs")

    elif g[pos[0]][pos[1]] == rhs[pos[0]][pos[1]]:
        openListRhs.pop(openListRhs.index(min(openListRhs)))
        posOpenListRhs.pop(openListRhs.index(min(openListRhs)))
        print("Mazem elks")

    print("gValue :", g)
    print('rhs: ', rhs)
    print('grid: ', grid)

    print('openListRhs: ', openListRhs)
    print('posOpenListRhs: ', posOpenListRhs)

    i += 1



