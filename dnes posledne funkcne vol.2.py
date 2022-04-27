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


grid[15][15] = 24 # robot
grid[5][3] = 3 # goal


def get_avel():
    global ang_vel
    return ang_vel


def oki(status):
    global ok
    ok = status

def set_first_iter(iter):
    global iterat
    iterat = iter

set_first_iter(0)

def get_first_iter():
    global iterat
    return iterat

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
            if grid[row][col] == object and row_column == 'row':
                return row
            elif grid[row][col] == object and row_column == 'col':
                return col

def get_robot_int():
    for i in range(numOfDice):
        for j in range(numOfDice):
            for k in robot_ort:
                if grid[i][j] == k:
                    return k

def steerAng():
    try:
        axis_x, axis_y = 0, 0

        if get_position(3, "row") > get_position(get_robot_int(), "row") and get_position(3, "col") > get_position(get_robot_int(), "col"):
            axis_x, axis_y = 1, -1
            print("Required steering angle: 135° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 135
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 23

        elif get_position(3, "row") > get_position(get_robot_int(), "row") and get_position(3, "col") < get_position(get_robot_int(), "col"):
            axis_x, axis_y = -1, -1
            print("Required steering angle: 45° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 45
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 21

        elif get_position(3, "row") < get_position(get_robot_int(), "row") and get_position(3, "col") < get_position(get_robot_int(), "col"):
            axis_x, axis_y = -1, 1
            print("Required steering angle: 315° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 315
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 27

        elif get_position(3, "row") < get_position(get_robot_int(), "row") and get_position(3, "col") > get_position(get_robot_int(), "col"):
            axis_x, axis_y = 1, 1
            print("Required steering angle: 225° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 225
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 25

        elif get_position(3, "row") == get_position(get_robot_int(), "row") and get_position(3, "col") < get_position(get_robot_int(), "col"):
            axis_x, axis_y = -1, 0
            print("Required steering angle: 0° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 0
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 20

        elif get_position(3, "row") == get_position(get_robot_int(), "row") and get_position(3, "col") > get_position(get_robot_int(), "col"):
            axis_x, axis_y = 1, 0
            print("Required steering angle: 180° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 180
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 24

        elif get_position(3, "row") > get_position(get_robot_int(), "row") and get_position(3, "col") == get_position(get_robot_int(), "col"):
            axis_x, axis_y = 0, -1
            print("Required steering angle: 90° and now orientation is: ", directions[get_robot_int() - 20])
            tang_vel = 90
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 22

        elif get_position(3, "row") < get_position(get_robot_int(), "row") and get_position(3, "col") == get_position(get_robot_int(), "col"):
            axis_x, axis_y = 0, 1
            print("Required steering angle: 270° and now orientation is: ",directions[get_robot_int() - 20])
            tang_vel = 270
            tang_vel = tang_vel - angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 26

        if tang_vel >= 360:
            tang_vel -= 360

        set_avel(tang_vel)

        return axis_x, axis_y
    except:
        oki(True)


def cityBlock():
    try:
        city_goal = cityblock([get_position(3, "row"), get_position(3, "col")], [get_position(get_robot_int(), "row"), get_position(get_robot_int(), "col")])

        if city_goal <= 1:
            return 1.75
        elif city_goal <= 3:
            return 1.5
        elif city_goal <= 5:
            return 1
        else:
            return 0.3
    except:
        print("I cant find navigation road")


def addRobot(x, y, obj):
    try:
        if grid[y][x] != 3:
            grid[y][x] = obj
            if obj >= 20 and obj <= 27:
                lastPose[0] = x - 1
                lastPose[1] = y - 1
                lastPose[2] = angles[obj - 20]

                print("Robot actual posotion is: [", x + 1, ", " , y + 1,"]")
                print("Robot direction is: " , directions[obj - 20])
        else:
            grid[int(y)][int(x)] = obj
            c = get_position(get_robot_int(), "row")
            r = get_position(get_robot_int(), "col")

            print("Robot actual posotion is: [" , r + 1, ", ", c + 1, "]")
            print("Robot direction is: ", directions[obj - 20])
            oki(True)
    except:
        oki(True)

def move(x, y):
    try:
        # Zistenie aktualnej polohy robota
        currX = get_position(get_robot_int(), "col")
        currY = get_position(get_robot_int(), "row")

        # vlavo
        if x == -1 and y == 0:
            if grid[currY][currX - 1] != 1:
                print("next grid value grid: ", grid[currY][currX - 1])

                if grid[currY][currX] == 20: # remove robot
                    grid[currY][currX] = 0

                addRobot(currX - 1, currY, 20)
                print("Moved left")
            else:
                print("Can not move left")

        # vpravo
        if x == 1 and y == 0:
            if grid[currY][currX + 1] != 1:
                print("next grid value : ", grid[currY][currX + 1])

                if grid[currY][currX] == 24: # remove robot
                    grid[currY][currX] = 0

                print("Moved right")
                addRobot(currX + 1, currY, 24)
            else:
                print("Can not move right")

        # dole
        if x == 0 and y == -1:
            if grid[currY + 1][currX] != 1:
                print("next grid value : ", grid[currY + 1][currX])

                if grid[currY][currX] == 22: # remove robot
                    grid[currY][currX] = 0

                addRobot(currX, currY + 1, 22)
                print("Moved down")
            else:
                print("Can not move down")

        # hore
        if x == 0 and y == 1:
            if grid[currY - 1][currX] != 1:
                print("next grid value : ", grid[currY - 1][currX])

                if grid[currY][currX] == 26: # remove robot
                    grid[currY][currX] = 0

                addRobot(currX, currY - 1, 26)
                print("Moved up")
            else:
                print("Can not move up")

        # hore vpravo
        if x == 1 and y == 1:
            if grid[currY - 1][currX + 1] != 1:
                print("next grid value : ", grid[currY - 1][currX + 1])

                if grid[currY][currX] == 25: # remove robot
                    grid[currY][currX] = 0

                addRobot(currX + 1, currY - 1, 25)
                print("Moved up and right")
            else:
                print("Can not move up and right")

        # hore vlavo
        if x == - 1 and y == 1:
            if grid[currY - 1][currX - 1] != 1:
                print("next grid value : ", grid[currY - 1][currX - 1])

                if grid[currY][currX] == 27: # remove robot
                    grid[currY][currX] = 0

                addRobot(currX - 1, currY - 1, 27)
                print("Moved up and left")
            else:
                print("Can not move up and left")

        # dole vlavo
        if x == - 1 and y == - 1:
            if grid[currY + 1][currX - 1] != 1:
                print("next grid value : ", grid[currY + 1][currX - 1])

                if grid[currY][currX] == 21: # remove robot
                    grid[currY][currX] = 0

                addRobot(currX - 1, currY + 1, 21)
                print("Moved down and left")
            else:
                print("Can not move down and left")

        # dole vpravo
        if x == 1 and y == - 1:
            if grid[currX + 1][currY + 1] != 1:
                print("next grid value : ", grid[currY + 1][currX + 1])

                if grid[currY][currX] == 23: # remove robot
                    grid[currY][currX] = 0

                addRobot(currX + 1, currY + 1, 23)
                print("Moved down and right")
            else:
                print("Can not move down and right")
    except:
        print("Something wrong, a cant move")

def odomCal():
    d_r, d_l = 0, 0
    robot_lastpose_col = get_position(get_robot_int(), "col") - 1
    robot_lastpose_row = get_position(get_robot_int(), "row") - 1

    # kolesa
    if lastPose[2] == 0:
        d_l = [robot_lastpose_col, robot_lastpose_row - .5]
        d_r = [robot_lastpose_col, robot_lastpose_row + .5]
    elif lastPose[2] == 45:
        d_l = [robot_lastpose_col + .35, robot_lastpose_row - .35]
        d_r = [robot_lastpose_col - .35, robot_lastpose_row + .35]
    elif lastPose[2] == 90:
        d_l = [robot_lastpose_col + .5, robot_lastpose_row]
        d_r = [robot_lastpose_col - .5, robot_lastpose_row]
    elif lastPose[2] == 135:
        d_l = [robot_lastpose_col + .35, robot_lastpose_row + .35]
        d_r = [robot_lastpose_col - .35, robot_lastpose_row - .35]
    elif lastPose[2] == 180:
        d_l = [robot_lastpose_col, robot_lastpose_row + .5]
        d_r = [robot_lastpose_col, robot_lastpose_row - .5]
    elif lastPose[2] == 225:
        d_l = [robot_lastpose_col - .35, robot_lastpose_row + .35]
        d_r = [robot_lastpose_col + .35, robot_lastpose_row - .35]
    elif lastPose[2] == 270:
        d_l = [robot_lastpose_col - .5, robot_lastpose_row]
        d_r = [robot_lastpose_col + .5, robot_lastpose_row]
    elif lastPose[2] == 315:
        d_l = [robot_lastpose_col - .35, robot_lastpose_row - .35]
        d_r = [robot_lastpose_col + .35, robot_lastpose_row + .35]

    # Vzdialenost koliest od stredu
    d_l = dist([robot_lastpose_col, robot_lastpose_row], d_l)
    d_r = dist([robot_lastpose_col, robot_lastpose_row], d_r)
    dc = round((d_r + d_l) / 2, 1)

    # premenna = angles[get_label_robot_ort(get_robot_int())]

    # Nove natocenie
    get_av = get_avel()
    newTeta = angles[get_label_robot_ort(get_robot_int())] - get_av

    # Nove polohy
    newX = floor(robot_lastpose_col + (dc * cos(math.radians(newTeta))))
    newY = floor(robot_lastpose_row + (dc * sin(math.radians(newTeta))))

    # Uprava polohy aby sedela voci mape
    if newTeta == 0:
        newX += 3
        newY += 2
    elif newTeta == 45:
        newX += 3
        newY += 1
    elif newTeta == 90:
        newX += 2
        newY += 1
    elif newTeta == 135:
        newX += 2
        newY += 1
    elif newTeta == 180:
        newX += 2
        newY += 2
    elif newTeta == 225:
        newX += 2
        newY += 4
    elif newTeta == 270:
        newX += 2
        newY += 4
    elif newTeta == 315:
        newX += 3
        newY += 4

    if get_first_iter() < 1: # v prvej iteracii je aktualna a posledna poza rovnaka
        newX = robot_lastpose_col + 2
        newY = robot_lastpose_row + 2

    print("------------------------------------------------------]")
    print("New pose: [" + str(robot_lastpose_col + 2) + ", " + str(robot_lastpose_row + 2) + "]")
    print("Last pose: [" + str(newX) + ", " + str(newY) + "]")

    print("New theta " + str(lastPose[2]) + "° | angle: " + str(get_avel()) + "°")
    print("Last theta: " + str(newTeta) + "°")
    print("------------------------------------------------------]")

    # Aktualizovanie poslednej polohy
    # robot_lastpose_col = newX - 1
    # robot_lastpose_row = newY - 1
    lastPose[2] = newTeta
    set_first_iter(2)

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
        odomCal()
        time.sleep(Preg)

        print("Current speed: " + str(2-Preg))
        print("x: ", goX, "y: ", goY)
        print("tang_vel: ", ang_vel)
        print('-----------------------------------')

    if ok == True:
        if delay > 0:
            time.sleep(Preg)
        delay += 1
        if delay > 1:
            print('-----------------------------------')
            print("I HAVE FINAL POSITION!")
            print("Current speed: 0")

    # for value_row in range(len(grid)):
    #     print(grid[value_row])

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
