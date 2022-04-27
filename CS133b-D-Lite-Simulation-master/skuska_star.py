import numpy as np
import math

x_Goal = 1
y_Goal = 8
x_Robot = 8
y_Robot = 8
posMin = [y_Goal, x_Goal]

openListRhs = []  # rhs
posOpenListRhs = []  # pozicia rhs
gValue = []

numOfDice = 10
grid = np.zeros((numOfDice, numOfDice))

grid[y_Robot][x_Robot] = 2
grid[y_Goal][x_Goal] = 3
grid[8][3] = 1  # prekazka
grid[7][2] = 1  # prekazka
grid[7][3] = 1  # prekazka

rhs = np.ones((numOfDice, numOfDice)) * np.inf
g = np.ones((numOfDice, numOfDice)) * np.inf
rhs[y_Goal][x_Goal] = 0

# inicializacne nahratie pozicie cieloveho bodu do rhslist a posrhslist
if rhs[y_Goal][x_Goal] != g[y_Goal][x_Goal]:
    openListRhs.append(rhs[y_Goal][x_Goal])
    posOpenListRhs.append((y_Goal, x_Goal))

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


def getFinalPos(robotPathMinPosIndex):
    robotPosRow = robotPathMinPosIndex[0]
    robotPosCol = robotPathMinPosIndex[1]

    print("hore: ", g[robotPosRow - 1][robotPosCol])  # hore 0
    print("dole: ", g[robotPosRow + 1][robotPosCol])  # dole 1
    print("vlavo: ", g[robotPosRow][robotPosCol - 1])  # vlavo 2
    print("vpravo: ", g[robotPosRow][robotPosCol + 1])  # vpravo 3

    print("hore-vlavo: ", g[robotPosRow - 1][robotPosCol - 1])  # hore-vlavo 4
    print("dole-vlavo: ", g[robotPosRow + 1][robotPosCol - 1])  # dole-vlavo 5
    print("dole-vpravo: ", g[robotPosRow + 1][robotPosCol + 1])  # dole-vpravo 6
    print("hore-vpravo: ", g[robotPosRow - 1][robotPosCol + 1])  # hore-vpravo 7

    robotPathG.append(g[robotPosRow - 1][robotPosCol])
    robotPathGPos.append((robotPosRow - 1, robotPosCol))

    robotPathG.append(g[robotPosRow + 1][robotPosCol])
    robotPathGPos.append((robotPosRow + 1, robotPosCol))

    robotPathG.append(g[robotPosRow][robotPosCol - 1])
    robotPathGPos.append((robotPosRow, robotPosCol - 1))

    robotPathG.append(g[robotPosRow][robotPosCol + 1])
    robotPathGPos.append((robotPosRow, robotPosCol + 1))

    robotPathG.append(g[robotPosRow - 1][robotPosCol - 1])
    robotPathGPos.append((robotPosRow - 1, robotPosCol - 1))

    robotPathG.append(g[robotPosRow + 1][robotPosCol - 1])
    robotPathGPos.append((robotPosRow + 1, robotPosCol - 1))

    robotPathG.append(g[robotPosRow + 1][robotPosCol + 1])
    robotPathGPos.append((robotPosRow + 1, robotPosCol + 1))

    robotPathG.append(g[robotPosRow - 1][robotPosCol + 1])
    robotPathGPos.append((robotPosRow - 1, robotPosCol + 1))

    return robotPathG, robotPathGPos


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


def ComputeShortestPath():
    while rhs[y_Robot][x_Robot] == np.inf or g[y_Robot][x_Robot] == np.inf:

        print("g[robotY][robotX]: ", g[y_Robot][x_Robot])
        print("rhs[robotY][robotX]: ", rhs[y_Robot][x_Robot])

        posMin = posOpenListRhs[openListRhs.index(min(openListRhs))]

        UpdateVertex(posMin)
        print("posMin: ", posMin)
        print("rhs posMin: ", rhs[posMin[0]][posMin[1]])
        print("g posMin: ", g[posMin[0]][posMin[1]])

        popIndex = openListRhs.index(min(openListRhs))

        print("I remove index: ", popIndex)

        openListRhs.pop(popIndex)
        posOpenListRhs.pop(popIndex)

        if g[posMin[0]][posMin[1]] > rhs[posMin[0]][posMin[1]]:
            g[posMin[0]][posMin[1]] = rhs[posMin[0]][posMin[1]]

            UpdateVertex(posMin)
            print("Mazem min zaznam z openListRhs a z posOpenListRhs")

        print("gValue : \n", g)
        print('rhs: \n', rhs)
        print("grid: \n", grid)
        print('openListRhs: ', openListRhs)
        print('posOpenListRhs: ', posOpenListRhs)

        print("---------------------------------------")


ComputeShortestPath()

robotPathG = []
robotPathGPos = []
finalPath = []
robotPathMin = np.inf

robotPosRow = get_position(2, "row")
robotPosCol = get_position(2, "col")

robotPathG, robotPathGPos = getFinalPos((robotPosRow, robotPosCol))

while robotPathMin != 0:
    # robotPosRow = get_position(2, "row")
    # robotPosCol = get_position(2, "col")

    print("robotPathG: ", robotPathG)
    print("robotPathGPos: ", robotPathGPos)

    robotPathMin = min(robotPathG)
    robotPathMinPosIndex = robotPathGPos[robotPathG.index(min(robotPathG))]

    print("robotPathMin: ", robotPathMin)
    print("robotPathMinPosIndex: ", robotPathMinPosIndex)

    finalPath.append(robotPathMinPosIndex)

    print("finalPath: ", finalPath)

    robotPathG = []
    robotPathGPos = []

    robotPathG, robotPathGPos = getFinalPos(robotPathMinPosIndex)

print("gValue : \n", g)
