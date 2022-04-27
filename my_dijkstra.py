import pygame
import csv
from scipy.spatial.distance import cityblock
import time
import math
from math import cos, dist, sin, floor

import subprocess

numOfDice = 25
widthHeight = 20
margin = 5
grid = []
screen = pygame.display.set_mode([630, 630])
done = False
ok = False
delay = 0

tang_vel = 0
speed_robot = 0

pygame.init()
pygame.display.set_caption("Publisher GUI")
clock = pygame.time.Clock()

# subprocess.Popen(['gnome-terminal', '-x', 'python3', '/home/nmvr/dev_ws/src/my_NmvrPackage/my_NmvrPackage/publisher.py'])

robot = [-1, -1, -1, 1]
goal = [-1, -1]
lastPose = [-1, -1, -1]

robot_ort = [20, 21, 22, 23, 24, 25, 26, 27]
angles =   [0, 45, 90, 135, 180, 225, 270, 315, 360]
directions = ["West", "South-west", "South", "South-east", "East", "North-east", "North", "North-west"]

# empty grid
for row in range(numOfDice):
    grid.append([])
    for column in range(numOfDice):
        grid[row].append(0)

# dice 1 around map
for r_c in range(numOfDice):
    grid[r_c][24] = 1
    grid[r_c][0] = 1
    grid[24][r_c] = 1
    grid[0][r_c] = 1


grid[11][10] = 24 # robot
grid[16][10] = 3 # goal

# grid[0][20] = 1

def get_avel():
    global ang_vel
    return ang_vel

def oki(status):
    global ok
    ok = status

def set_avel(vel):
    global ang_vel
    ang_vel = vel

def get_label_robot_ort(label):
    for i in robot_ort:
            if i == label:
                return i-20

def get_position(object, row_column):
    for row in range(numOfDice):
        for col in range(numOfDice):
            if grid[row][col] == object and row_column == "row":
                return row
            elif grid[row][col] == object and row_column == "col":
                return col

def get_robot_int():
    for i in range(numOfDice):
        for j in range(numOfDice):
            for k in robot_ort:
                if grid[i][j] == k:
                    return k

def steerAng():
    try:
        steerX, steerY = 0, 0

        if get_position(3, "row") > get_position(get_robot_int(), "row") and get_position(3, "col") > get_position(get_robot_int(), "col"):
            steerX = 1
            steerY = -1
            print("Required steering angle: 135° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 135
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 23

        elif get_position(3, "row") > get_position(get_robot_int(), "row") and get_position(3, "col") < get_position(get_robot_int(), "col"):
            steerX = -1
            steerY = -1
            print("Required steering angle: 45° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 45
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 21

        elif get_position(3, "row") < get_position(get_robot_int(), "row") and get_position(3, "col") < get_position(get_robot_int(), "col"):
            steerX = -1
            steerY = 1
            print("Required steering angle: 315° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 315
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 27

        elif get_position(3, "row") < get_position(get_robot_int(), "row") and get_position(3, "col") > get_position(get_robot_int(), "col"):
            steerX = 1
            steerY = 1
            print("Required steering angle: 225° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 225
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 25

        elif get_position(3, "row") == get_position(get_robot_int(), "row") and get_position(3, "col") < get_position(get_robot_int(), "col"):
            steerX = -1
            steerY = 0
            print("Required steering angle: 0° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 0
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 20

        elif get_position(3, "row") == get_position(get_robot_int(), "row") and get_position(3, "col") > get_position(get_robot_int(), "col"):
            steerX = 1
            steerY = 0
            print("Required steering angle: 180° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 180
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 24

        elif get_position(3, "row") > get_position(get_robot_int(), "row") and get_position(3, "col") == get_position(get_robot_int(), "col"):
            steerX = 0
            steerY = -1
            print("Required steering angle: 90° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 90
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 22

        elif get_position(3, "row") < get_position(get_robot_int(), "row") and get_position(3, "col") == get_position(get_robot_int(), "col"):
            steerX = 0
            steerY = 1
            print("Required steering angle: 270° and now orientation is: ",directions[get_robot_int() - 20])
            tang_vel = 270
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 26

        if tang_vel >= 360:
            tang_vel -= 360

        set_avel(tang_vel)

        return steerX, steerY
    except:
        print("I dont find ang")

def cityBlock():
    city_goal = cityblock([get_position(3, "row"), get_position(3, "col")], [get_position(get_robot_int(), "row"), get_position(get_robot_int(), "col")])

    if city_goal <= 1:
        return 1.75
    elif city_goal <= 3:
        return 1.5
    elif city_goal <= 5:
        return 1
    else:
        return 0.3


def addRobot(x, y, obj):
    try:
        if grid[int(y)][int(x)] != 3:
            grid[int(y)][int(x)] = obj
            if obj >= 20 and obj <= 27:
                lastPose[0] = int(x) - 1
                lastPose[1] = int(y) - 1
                lastPose[2] = angles[obj - 20]

                print("Robot actual posotion is: [" + str(x + 1) + ", " + str(str(y + 1)) + "]")
                print("Robot direction is: " + str(directions[obj - 20]))
        else:
            grid[int(y)][int(x)] = obj
            row_gridpos_robot = get_position(get_robot_int(), "row")
            col_gridpos_robot = get_position(get_robot_int(), "col")

            print("Robot actual posotion is: [" + str(col_gridpos_robot + 1) + ", " + str(row_gridpos_robot + 1) + "]")
            print("Robot direction is: " + str(directions[robot[2] - 20]))
            oki(True)
    except:
        oki(True)
        print("Can not add an object")


def move(x, y):
    # Zistenie aktualnej polohy robota
    col_gridpos_robot = get_position(get_robot_int(), "col")
    row_gridpos_robot = get_position(get_robot_int(), "row")

    # vlavo
    if x == -1 and y == 0:
        if grid[row_gridpos_robot][col_gridpos_robot - 1] != 1:
            print("next grid value grid: ", grid[row_gridpos_robot][col_gridpos_robot - 1])

            if grid[row_gridpos_robot][col_gridpos_robot] == 20: # remove robot
                grid[row_gridpos_robot][col_gridpos_robot] = 0

            addRobot(col_gridpos_robot - 1, row_gridpos_robot, 20)
            print("Moved left")
        else:
            print("Can not move left")

    # vpravo
    if x == 1 and y == 0:
        if grid[row_gridpos_robot][col_gridpos_robot + 1] != 1:
            print("next grid value : ", grid[row_gridpos_robot][col_gridpos_robot + 1])

            if grid[row_gridpos_robot][col_gridpos_robot] == 24: # remove robot
                grid[row_gridpos_robot][col_gridpos_robot] = 0

            print("Moved right")
            addRobot(col_gridpos_robot + 1, row_gridpos_robot, 24)
        else:
            print("Can not move right")

    # dole
    if x == 0 and y == -1:
        if grid[row_gridpos_robot + 1][col_gridpos_robot] != 1:
            print("next grid value : ", grid[row_gridpos_robot + 1][col_gridpos_robot])

            if grid[row_gridpos_robot][col_gridpos_robot] == 22: # remove robot
                grid[row_gridpos_robot][col_gridpos_robot] = 0

            addRobot(col_gridpos_robot, row_gridpos_robot + 1, 22)
            print("Moved down")
        else:
            print("Can not move down")

    # hore
    if x == 0 and y == 1:
        if grid[row_gridpos_robot - 1][col_gridpos_robot] != 1:
            print("next grid value : ", grid[row_gridpos_robot - 1][col_gridpos_robot])

            if grid[row_gridpos_robot][col_gridpos_robot] == 26: # remove robot
                grid[row_gridpos_robot][col_gridpos_robot] = 0

            addRobot(col_gridpos_robot, row_gridpos_robot - 1, 26)
            print("Moved up")
        else:
            print("Can not move up")

    # hore vpravo
    if x == 1 and y == 1:
        if grid[row_gridpos_robot - 1][col_gridpos_robot + 1] != 1:
            print("next grid value : ", grid[row_gridpos_robot - 1][col_gridpos_robot + 1])

            if grid[row_gridpos_robot][col_gridpos_robot] == 25: # remove robot
                grid[row_gridpos_robot][col_gridpos_robot] = 0

            addRobot(col_gridpos_robot + 1, row_gridpos_robot - 1, 25)
            print("Moved up and right")
        else:
            print("Can not move up and right")

    # hore vlavo
    if x == - 1 and y == 1:
        if grid[row_gridpos_robot - 1][col_gridpos_robot - 1] != 1:
            print("next grid value : ", grid[row_gridpos_robot - 1][col_gridpos_robot - 1])

            if grid[row_gridpos_robot][col_gridpos_robot] == 27: # remove robot
                grid[row_gridpos_robot][col_gridpos_robot] = 0

            addRobot(col_gridpos_robot - 1, row_gridpos_robot - 1, 27)
            print("Moved up and left")
        else:
            print("Can not move up and left")

    # dole vlavo
    if x == - 1 and y == - 1:
        if grid[row_gridpos_robot + 1][col_gridpos_robot - 1] != 1:
            print("next grid value : ", grid[row_gridpos_robot + 1][col_gridpos_robot - 1])

            if grid[row_gridpos_robot][col_gridpos_robot] == 21: # remove robot
                grid[row_gridpos_robot][col_gridpos_robot] = 0

            addRobot(col_gridpos_robot - 1, row_gridpos_robot + 1, 21)
            print("Moved down and left")
        else:
            print("Can not move down and left")

    # dole vpravo
    if x == 1 and y == - 1:
        if grid[col_gridpos_robot + 1][row_gridpos_robot + 1] != 1:
            print("next grid value : ", grid[row_gridpos_robot + 1][col_gridpos_robot + 1])

            if grid[row_gridpos_robot][col_gridpos_robot] == 23: # remove robot
                grid[row_gridpos_robot][col_gridpos_robot] = 0

            addRobot(col_gridpos_robot + 1, row_gridpos_robot + 1, 23)
            print("Moved down and right")
        else:
            print("Can not move down and right")

def odomCal():
    d_r, d_l = 0, 0

    # ro = get_position(get_robot_int(), "col")
    # co = get_position(get_robot_int(), "row")
    # tan = angles[get_label_robot_ort(get_robot_int())]
    #
    # lastPose0 = lastPose[0]
    # lastPose1 = lastPose[1]
    # lastPose2 = lastPose[2]
    #
    # print("co: ", co)
    # print("ro: ", ro)
    # print("tan", tan)
    # print("lastPose[0]", lastPose0)
    # print("lastPose[1]", lastPose1)
    # print("lastPose[2]", lastPose2)
    #
    # print("ok")

    # kolesa
    if lastPose[2] == 0:
        d_r = [lastPose[0], lastPose[1] + .5]
        d_l = [lastPose[0], lastPose[1] - .5]
    elif lastPose[2] == 45:
        d_r = [lastPose[0] + .35, lastPose[1] + .35]
        d_l = [lastPose[0] - .35, lastPose[1] - .35]
    elif lastPose[2] == 90:
        d_r = [lastPose[0] + .5, lastPose[1]]
        d_l = [lastPose[0] - .5, lastPose[1]]
    elif lastPose[2] == 135:
        d_r = [lastPose[0] + .35, lastPose[1] - .35]
        d_l = [lastPose[0] - .35, lastPose[1] + .35]
    elif lastPose[2] == 180:
        d_r = [lastPose[0], lastPose[1] - .5]
        d_l = [lastPose[0], lastPose[1] + .5]
    elif lastPose[2] == 225:
        d_r = [lastPose[0] - .35, lastPose[1] - .35]
        d_l = [lastPose[0] + .35, lastPose[1] + .35]
    elif lastPose[2] == 270:
        d_r = [lastPose[0] - .5, lastPose[1]]
        d_l = [lastPose[0] + .5, lastPose[1]]
    elif lastPose[2] == 315:
        d_r = [lastPose[0] - .35, lastPose[1] + .35]
        d_l = [lastPose[0] + .35, lastPose[1] - .35]

    # Vzdialenost koliest od stredu
    d_l = dist([lastPose[0], lastPose[1]], d_l)
    d_r = dist([lastPose[0], lastPose[1]], d_r)
    dc = round((d_r + d_l) / 2, 1)

    # Nove natocenie
    newTeta = lastPose[2] + get_avel()

    # Nove polohy
    newX = floor(lastPose[0] + (dc * cos(math.radians(newTeta))))
    newY = floor(lastPose[1] + (dc * sin(math.radians(newTeta))))

    # Uprava polohy aby sedela voci mape
    if newTeta == 0:
        newX += 0
        newY += 1
    elif newTeta == 45:
        newX += 0
        newY += 0
    elif newTeta == 90:
        newX += 1
        newY += 0
    elif newTeta == 135:
        newX += 3
        newY += 0
    elif newTeta == 180:
        newX += 3
        newY += 1
    elif newTeta == 225:
        newX += 3
        newY += 3
    elif newTeta == 270:
        newX += 1
        newY += 3
    else:
        newX += 0
        newY += 3

    print("------------------------------------------------------]")
    print("Last pose: [" + str(lastPose[0] + 2) + ", " + str(lastPose[1] + 2) + "]")
    print("New pose: [" + str(newX + 1) + ", " + str(newY + 1) + "]")
    print("Last theta: " + str(lastPose[2]) + "° | angle: " + str(get_avel()) + "°")
    print("New theta: " + str(newTeta) + "°")
    print("------------------------------------------------------]")

    # Aktualizovanie poslednej polohy
    lastPose[0] = newX - 1
    lastPose[1] = newY - 1
    lastPose[2] = newTeta

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (widthHeight + margin)
            row = pos[1] // (widthHeight + margin)

            # pre kliknutie na dlazdicu - vyt. a odst. muru
            for i in robot_ort:
                if grid[row][column] == i and grid[row][column] == 3:
                    break
                elif grid[row][column] == 0:
                    grid[row][column] = 1
                    break
                elif grid[row][column] == 1:
                    grid[row][column] = 0
                    break

            print("Click ", pos, "Grid coordinates: ", row, column, "Value:", grid[row][column])

            # for value_row in range(len(grid)):
            #     print(grid[value_row])

            print("Saving data to csv...")
            with open("new_file.csv", "w+", newline="") as my_csv:
                csvWriter = csv.writer(my_csv)
                csvWriter.writerows(grid)

    for row in range(numOfDice):
        for column in range(numOfDice):
            color = (255, 255, 255)
            if grid[row][column] == 1: # mur
                color = (30, 30, 30)
            for i in robot_ort: # robot
                if grid[row][column] == i:
                    color = (255, 0, 0)
            if grid[row][column] == 3: # goal
                color = (255, 255, 0)
            if grid[row][column] == 0: # free
                color = (255, 255, 255)
            pygame.draw.rect(screen, color, [(margin + widthHeight) * column + margin,
                                             (margin + widthHeight) * row + margin,
                                             widthHeight, widthHeight])

    if ok == False:
        goX, goY = steerAng()
        Preg = cityBlock()
        move(goX, goY)
        # odomCal()
        time.sleep(Preg)

        print("Current speed: " + str(2-Preg))
        print("x: ", goX, "y: ", goY)
        print("tang_vel: ", ang_vel)
        print('-----------------------------------')

    if ok == True:
        delay += 1
        time.sleep(Preg)
        if delay > 1:
            print('-----------------------------------')
            print("I HAVE FINAL POSITION!")
            print("Current speed: 0")

    # for value_row in range(len(grid)):
    #     print(grid[value_row])

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
