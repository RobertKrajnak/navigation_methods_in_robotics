import pygame
import csv
from scipy.spatial.distance import cityblock
import time
import math
from math import cos, dist, sin, floor
import subprocess

# premenne pre zadanie 1
numOfDice = 10
widthHeight = 57.5
margin = 5
grid = []
screen = pygame.display.set_mode([630, 630])
pygame.init()
pygame.display.set_caption("Publisher GUI")
clock = pygame.time.Clock()

# subprocess.Popen(['gnome-terminal', '-x', 'python3', '/home/nmvr/dev_ws/src/my_NmvrPackage/my_NmvrPackage/publisher.py'])

# premenne pre zadanie 2
robot_int_ort = [20, 21, 22, 23, 24, 25, 26, 27]
robot_angles = [0, 45, 90, 135, 180, 225, 270, 315]
robot_directions = ["West", "South-west", "South", "South-east", "East", "North-east", "North", "North-west"]
done = False
ok = False
delay = 0
tang_vel = 0
iterra = 0

# vytovrenie prazdnej mapy
for row in range(numOfDice):
    grid.append([])
    for column in range(numOfDice):
        grid[row].append(0)

# naplnenie jednotkami dookola
for r_c in range(numOfDice):
    grid[r_c][numOfDice-1] = 1
    grid[r_c][0] = 1
    grid[numOfDice-1][r_c] = 1
    grid[0][r_c] = 1

# definovanie pozicii robota a ciela
print("Zajdajte polohu robota v rozmedzi :", numOfDice, "x", numOfDice)
print("Zajdajte x-ovú súradnicu robota od 0 do ", numOfDice - 1, ":")
x_Robot = input()
print("Zajdajte y-ovú súradnicu robota od 0 do ", numOfDice - 1, ":")
y_Robot = input()
print("Zajdajte otocenie robota v rozmedzi 20-27: ")
robot_ort = input()

print("Zajdajte polohu ciela v rozmedzi :", numOfDice, "x", numOfDice)
print("Zajdajte x-ovú súradnicu ciela od 0 do ", numOfDice - 1, ":")
x_Goal = input()
print("Zajdajte y-ovú súradnicu ciela od 0 do ", numOfDice - 1, ":")
y_Goal = input()

grid[int(x_Robot)][int(y_Robot)] = int(robot_ort)
grid[int(x_Goal)][int(y_Goal)] = 3 # goal

# grid[11][10] = 24 # robot
# grid[16][10] = 3 # goal





# nastavenie uhla posleslednej pozicie
def set_lastpose_angle(angle):
    global ang
    ang = angle

# zavolanie uhla poslednej pozicie
def get_lastpose_angle():
    global ang
    return ang

# zavolanie rozdielu uhlov povodnej a poslednej pozicie
def get_angle_diff():
    global angle
    return angle

# nastavenie rozdielu uhlov povodnej a poslednej pozicie
def set_angle_diff(diff):
    global angle
    angle = diff

# nastavenie statusu na dokoncenz - v ciely
def oki(status):
    global ok
    ok = status

# nastavenie prvej iteracie pre pozicie
def set_first_iter(iter):
    global iterat
    iterat = iter

set_first_iter(0)

# zavolanie - zistenie iteracie
def get_first_iter():
    global iterat
    return iterat

# vrati robot ort label napr.: 0,1,2...
def get_label_robot_ort(label):
    for i in robot_int_ort:
            if i == label:
                return i-20

# vrati poziciu row/coll objektu goal/robot
def get_position(object, row_column):
    for row in range(numOfDice):
        for col in range(numOfDice):
            if grid[row][col] == object and row_column == 'row':
                return row
            elif grid[row][col] == object and row_column == 'col':
                return col

# vrati konkretny int robota teda napr.: 20,21,22..
def get_robot_int():
    for i in range(numOfDice):
        for j in range(numOfDice):
            for k in robot_int_ort:
                if grid[i][j] == k:
                    return k

# nastavenie orientacie robota na ciel, vratenie orientacii pre posun, nastavenie uhla
def orientation_setting():
    try:
        axis_x, axis_y = 0, 0

        # vpravo-dole = 135, robot int = 23
        if get_position(3, "row") > get_position(get_robot_int(), "row") and get_position(3, "col") > get_position(get_robot_int(), "col"):
            axis_x, axis_y = 1, -1
            print("| Required steering angle: 135° and now orientation is: ", robot_directions[get_robot_int() - 20])
            target_angle = 135
            target_angle = target_angle - robot_angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 23

        # vlavo-dole = 45, robot int = 21
        elif get_position(3, "row") > get_position(get_robot_int(), "row") and get_position(3, "col") < get_position(get_robot_int(), "col"):
            axis_x, axis_y = -1, -1
            print("| Required steering angle: 45° and now orientation is: ", robot_directions[get_robot_int() - 20])
            target_angle = 45
            target_angle = target_angle - robot_angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 21

        # vlavo-hore = 315, robot int = 27
        elif get_position(3, "row") < get_position(get_robot_int(), "row") and get_position(3, "col") < get_position(get_robot_int(), "col"):
            axis_x, axis_y = -1, 1
            print("| Required steering angle: 315° and now orientation is: ", robot_directions[get_robot_int() - 20])
            target_angle = 315
            target_angle = target_angle - robot_angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 27

        # vpravo-hore = 225, robot int = 25
        elif get_position(3, "row") < get_position(get_robot_int(), "row") and get_position(3, "col") > get_position(get_robot_int(), "col"):
            axis_x, axis_y = 1, 1
            print("| Required steering angle: 225° and now orientation is: ", robot_directions[get_robot_int() - 20])
            target_angle = 225
            target_angle = target_angle - robot_angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 25

        # vlavo = 0, robot int = 20
        elif get_position(3, "row") == get_position(get_robot_int(), "row") and get_position(3, "col") < get_position(get_robot_int(), "col"):
            axis_x, axis_y = -1, 0
            print("| Required steering angle: 0° and now orientation is: ", robot_directions[get_robot_int() - 20])
            target_angle = 0
            target_angle = target_angle - robot_angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 20

        # vpravo = 180, robot int = 24
        elif get_position(3, "row") == get_position(get_robot_int(), "row") and get_position(3, "col") > get_position(get_robot_int(), "col"):
            axis_x, axis_y = 1, 0
            print("| Required steering angle: 180° and now orientation is: ", robot_directions[get_robot_int() - 20])
            target_angle = 180
            target_angle = target_angle - robot_angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 24

        # dole = 90, robot int = 22
        elif get_position(3, "row") > get_position(get_robot_int(), "row") and get_position(3, "col") == get_position(get_robot_int(), "col"):
            axis_x, axis_y = 0, -1
            print("| Required steering angle: 90° and now orientation is: ", robot_directions[get_robot_int() - 20])
            target_angle = 90
            target_angle = target_angle - robot_angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 22

        # hore = 270, robot int = 26
        elif get_position(3, "row") < get_position(get_robot_int(), "row") and get_position(3, "col") == get_position(get_robot_int(), "col"):
            axis_x, axis_y = 0, 1
            print("| Required steering angle: 270° and now orientation is: ", robot_directions[get_robot_int() - 20])
            target_angle = 270
            target_angle = target_angle - robot_angles[get_label_robot_ort(get_robot_int())]
            grid[get_position(get_robot_int(), "row")][get_position(get_robot_int(), "col")] = 26

        if target_angle >= 360:
            target_angle -= 360

        set_angle_diff(target_angle)
        return axis_x, axis_y
    except:
        oki(True)

# p regulator pre urcovanie rychlosti v zavislosti od vzdialenosti od ciela
def p_reg_setting():
    try:
        # ziskanie vzdialensoti od ciela
        distance_goal = cityblock([get_position(3, "row"), get_position(3, "col")], [get_position(get_robot_int(), "row"), get_position(get_robot_int(), "col")])

        # nastavenie rychlosti podla vzdialensoti
        if distance_goal <= 1:
            return 1.75
        elif distance_goal <= 3:
            return 1.5
        elif distance_goal <= 5:
            return 1
        else:
            return 0.3
    except:
        print("I cant find navigation road")

# pridanie novej pozicie pre robota v zavislosti od uhla otocenia - robot int
def robot_add(x, y, obj):
    try:
        # ako to nie je ciel
        if grid[y][x] != 3:
            grid[y][x] = obj
            if obj >= 20 and obj <= 27:
                set_lastpose_angle(robot_angles[obj - 20])

                print("| Robot actual posotion is: [", x + 1, ", ", y + 1, "]")
                print("| Robot direction is: ", robot_directions[obj - 20])
        else:
            # ak to je ciel
            grid[int(y)][int(x)] = obj
            c = get_position(get_robot_int(), "row")
            r = get_position(get_robot_int(), "col")

            print("| Robot actual posotion is: [", r + 1, ", ", c + 1, "]")
            print("| Robot direction is: ", robot_directions[obj - 20])
            oki(True)
    except:
        oki(True)

# riadenie pohybu v zavislosti od polohy a orientacie robota
def move_setting(x, y):
    try:
        # Zistenie aktualnej polohy robota
        currX = get_position(get_robot_int(), "col")
        currY = get_position(get_robot_int(), "row")

        # - prva podmienka stale ci sa pred nim nenachadza prekazka
        # - vymaze robota z aktualnej pozicie
        # - prida robota na nasledujucu poziciu

        # pohyb vlavo
        if x == -1 and y == 0:
            if grid[currY][currX - 1] != 1:
                print("| Next grid value grid: ", grid[currY][currX - 1])

                if grid[currY][currX] == 20: # remove robot
                    grid[currY][currX] = 0

                robot_add(currX - 1, currY, 20)
                print("| Robot move left! ")
            else:
                print("| ROBOT CANT MOVE LEFT! ")

        # pohyb vpravo
        if x == 1 and y == 0:
            if grid[currY][currX + 1] != 1:
                print("| Next grid value grid: ", grid[currY][currX + 1])

                if grid[currY][currX] == 24: # remove robot
                    grid[currY][currX] = 0

                print("| Robot move right")
                robot_add(currX + 1, currY, 24)
            else:
                print("| ROBOT CANT MOVE RIGHT! ")

        # pohyb dole
        if x == 0 and y == -1:
            if grid[currY + 1][currX] != 1:
                print("| Next grid value grid: ", grid[currY + 1][currX])

                if grid[currY][currX] == 22: # remove robot
                    grid[currY][currX] = 0

                robot_add(currX, currY + 1, 22)
                print("| Robot move down")
            else:
                print("| ROBOT CANT MOVE DOWN! ")

        # pohyb hore
        if x == 0 and y == 1:
            if grid[currY - 1][currX] != 1:
                print("| Next grid value grid: ", grid[currY - 1][currX])

                if grid[currY][currX] == 26: # remove robot
                    grid[currY][currX] = 0

                robot_add(currX, currY - 1, 26)
                print("| Robot move up")
            else:
                print("| ROBOT CANT MOVE UP! ")

        # pohyb hore vpravo
        if x == 1 and y == 1:
            if grid[currY - 1][currX + 1] != 1:
                print("| Next grid value grid: ", grid[currY - 1][currX + 1])

                if grid[currY][currX] == 25: # remove robot
                    grid[currY][currX] = 0

                robot_add(currX + 1, currY - 1, 25)
                print("| Robot move up and right")
            else:
                print("| ROBOT CANT MOVE UP AND RIGHT! ")

        # pohyb hore vlavo
        if x == - 1 and y == 1:
            if grid[currY - 1][currX - 1] != 1:
                print("| Next grid value grid: ", grid[currY - 1][currX - 1])

                if grid[currY][currX] == 27: # remove robot
                    grid[currY][currX] = 0

                robot_add(currX - 1, currY - 1, 27)
                print("| Robot move up and left")
            else:
                print("| ROBOT CANT MOVE UP AND LEFT! ")

        # pohyb dole vlavo
        if x == - 1 and y == - 1:
            if grid[currY + 1][currX - 1] != 1:
                print("| Next grid value grid: ", grid[currY + 1][currX - 1])

                if grid[currY][currX] == 21: # remove robot
                    grid[currY][currX] = 0

                robot_add(currX - 1, currY + 1, 21)
                print("| Robot move down and left")
            else:
                print("| ROBOT CANT MOVE DOWN AND LEFT! ")

        # pohyb dole vpravo
        if x == 1 and y == - 1:
            if grid[currX + 1][currY + 1] != 1:
                print("| Next grid value grid: ", grid[currY + 1][currX + 1])

                if grid[currY][currX] == 23: # remove robot
                    grid[currY][currX] = 0

                robot_add(currX + 1, currY + 1, 23)
                print("| Robot move down and right")
            else:
                print("| ROBOT CANT MOVE DOWN AND RIGHT! ")

    except:
        print("ERROR---Something wrong, a cant move---")

def odometry_setting():
    # zistenie aktualny-predchadzajucich pozicii a orientacii
    robot_lastpose_col = get_position(get_robot_int(), "col") - 1
    robot_lastpose_row = get_position(get_robot_int(), "row") - 1
    last_theta = get_lastpose_angle() - get_angle_diff()

    right_wheel, left_wheel = 0, 0

    # nastavenie kolies v zavislosti od uhla
    if last_theta == robot_angles[0]:
        left_wheel = [robot_lastpose_col, robot_lastpose_row - .5]
        right_wheel = [robot_lastpose_col, robot_lastpose_row + .5]
    elif last_theta == robot_angles[1]:
        left_wheel = [robot_lastpose_col + .35, robot_lastpose_row - .35]
        right_wheel = [robot_lastpose_col - .35, robot_lastpose_row + .35]
    elif last_theta == robot_angles[2]:
        left_wheel = [robot_lastpose_col + .5, robot_lastpose_row]
        right_wheel = [robot_lastpose_col - .5, robot_lastpose_row]
    elif last_theta == robot_angles[3]:
        left_wheel = [robot_lastpose_col + .35, robot_lastpose_row + .35]
        right_wheel = [robot_lastpose_col - .35, robot_lastpose_row - .35]
    elif last_theta == robot_angles[4]:
        left_wheel = [robot_lastpose_col, robot_lastpose_row + .5]
        right_wheel = [robot_lastpose_col, robot_lastpose_row - .5]
    elif last_theta == robot_angles[5]:
        left_wheel = [robot_lastpose_col - .35, robot_lastpose_row + .35]
        right_wheel = [robot_lastpose_col + .35, robot_lastpose_row - .35]
    elif last_theta == robot_angles[6]:
        left_wheel = [robot_lastpose_col - .5, robot_lastpose_row]
        right_wheel = [robot_lastpose_col + .5, robot_lastpose_row]
    elif last_theta == robot_angles[7]:
        right_wheel = [robot_lastpose_col + .35, robot_lastpose_row + .35]
        left_wheel = [robot_lastpose_col - .35, robot_lastpose_row - .35]

    # vypocet vzdialenosti koliest od stredu podla uhla
    left_wheel = dist([robot_lastpose_col, robot_lastpose_row], left_wheel)
    right_wheel = dist([robot_lastpose_col, robot_lastpose_row], right_wheel)
    dc = round((right_wheel + left_wheel) / 2, 1)
    # vypocet noveho aktualneho natocenia robota
    new_theta = get_lastpose_angle()
    # vypocet novej polohy robota v zavislosti od natocenia
    new_row_pos = floor(robot_lastpose_col + (dc * cos(math.radians(new_theta))))
    new_coll_pos = floor(robot_lastpose_row + (dc * sin(math.radians(new_theta))))

    # vyrovnanie rozdielu polohy
    if new_theta == robot_angles[0]:
        new_row_pos += 3
        new_coll_pos += 2
    elif new_theta == robot_angles[1]:
        new_row_pos += 3
        new_coll_pos += 1
    elif new_theta == robot_angles[2]:
        new_row_pos += 2
        new_coll_pos += 1
    elif new_theta == robot_angles[3]:
        new_row_pos += 2
        new_coll_pos += 1
    elif new_theta == robot_angles[4]:
        new_row_pos += 2
        new_coll_pos += 2
    elif new_theta == robot_angles[5]:
        new_row_pos += 2
        new_coll_pos += 4
    elif new_theta == robot_angles[6]:
        new_row_pos += 2
        new_coll_pos += 4
    elif new_theta == robot_angles[7]:
        new_row_pos += 3
        new_coll_pos += 4

    # v prvej iteracii je aktualna a posledna poza rovnaka
    if get_first_iter() < 1:
        new_row_pos = robot_lastpose_col + 2
        new_coll_pos = robot_lastpose_row + 2

    print(" ---------ODO CALLCULATE---------")
    print("| Last robot theta ", last_theta, "°")
    print("| New robot theta: ", new_theta, "°")
    print("| Robot angle: ", get_angle_diff(), "°")
    print("| New robot pose: [", robot_lastpose_col + 2, ",", robot_lastpose_row + 2, "]")
    print("| Last robot pose: [", new_row_pos, ",", new_coll_pos, "]")
    print(" --------------------------------")


    # preposianie poslednej polohy a nastavenie iteracie
    set_lastpose_angle(new_theta)
    set_first_iter(2)

def save_csv():
    print("| Saving data to csv...")
    print(" --------------------------------")
    with open("new_file.csv", "w+", newline="") as my_csv:
        csvWriter = csv.writer(my_csv)
        csvWriter.writerows(grid)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (widthHeight + margin)
            row = pos[1] // (widthHeight + margin)

            # pre kliknutie na dlazdicu - vyt. a odst. muru
            for i in robot_int_ort:
                if grid[row][column] == i and grid[row][column] == 3:
                    break
                elif grid[row][column] == 0:
                    grid[row][column] = 1
                    break
                elif grid[row][column] == 1:
                    grid[row][column] = 0
                    break

            print("| Click ", pos, "Grid coordinates: ", row, column, "Value:", grid[row][column])

            # for value_row in range(len(grid)):
            #     print(grid[value_row])

            save_csv()

    print(" -------------No. Iter is:", iterra, "-------------")
    # ak este nie je v ciely
    if ok == False:
        goX, goY = orientation_setting()
        p_regulator = p_reg_setting()
        move_setting(goX, goY)

        print("| Current robot speed: " + str(2 - p_regulator))
        print("| Orientation setting for move: [", goX, ", ", goY, "]")

        odometry_setting()
        time.sleep(p_regulator)
        

    # ak robot je v ciely
    if ok == True:
        if delay > 0:
            time.sleep(p_regulator)
        delay += 1
        if delay > 1:
            print("---I HAVE FINAL POSITION!----------")
            print("| Current speed: 0")


    for row in range(numOfDice):
        for column in range(numOfDice):
            color = (255, 255, 255)
            if grid[row][column] == 1: # mur
                color = (30, 30, 30)
            for i in robot_int_ort: # robot
                if grid[row][column] == i:
                    color = (255, 0, 0)
            if grid[row][column] == 3: # goal
                color = (255, 255, 0)
            if grid[row][column] == 0: # free
                color = (255, 255, 255)
            pygame.draw.rect(screen, color, [(margin + widthHeight) * column + margin,
                                             (margin + widthHeight) * row + margin,
                                             widthHeight, widthHeight])

    save_csv()

    
    # for value_row in range(len(grid)):
    #     print(grid[value_row])

    print("\n")
    iterra += 1
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
