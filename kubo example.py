from matplotlib import pyplot as plt
from matplotlib import colors
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import csv
import numpy as np
import subprocess
import os
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from math import cos, pow, atan2, sqrt, dist, sin, floor
import math
from scipy.spatial.distance import cityblock
import time

data, mapStat, myDir, globAnot, lastSet, ang_vel = [], False, os.getcwd() + "/", 0, False, 0
# --------------------[x, y, rot, speed]
mainRobot, mainGoal, lastPose = [-1, -1, -1, 1], [-1, -1], [-1, -1, -1]
angles, directions = [0, 45, 90, 135, 180, 225, 270, 315, 360], ["West", "North-west", "North", "North-east", "East",
                                                                 "South-east", "South", "South-west"]


# Globalne uchovavanie mapy
def setData(inD):
    global data
    data = inD


# Ukladanie mapy pre jej nasledne odoslanie subscriberovi
def saveData(map):
    try:
        f1 = myDir + "publisher.csv"
        np.savetxt(f1, map, delimiter=",", fmt='% s')
    except:
        print("Map can not be saved.")


def getLast():
    global lastSet
    return lastSet


def setLast(status):
    global lastSet
    lastSet = status


def set_avel(vel):
    global ang_vel
    ang_vel = vel


def get_avel():
    global ang_vel
    return ang_vel


# Pozicia objektov
def place(map, obj):
    i, j, k = 0, 0, False
    for i in range(0, len(map)):
        for j in range(0, len(map[i])):
            # najdenie pozicie objektu (robota alebo ciela)
            if map[i][j] == obj:
                k = True
                break
            # Najdenie pozicie a rotacie robota pri prvotnom nacitani mapy
            elif obj == 28 and map[i][j] >= 20 and map[i][j] <= 27:
                mainRobot[2] = map[i][j]
                lastPose[2] = angles[map[i][j] - 20]
                k = True
                break

            if k: break
        if k: break
    if k:
        return i, j
    else:
        return -1, -1


LARGEFONT = ("Verdana", 35)
MEDIUMFONT = ("Verdana", 19)
MINIFONT = ("Verdana", 15)


class NMVR(tk.Frame):

    # Vykreslovanie mapy a objektov na nej
    def showMap(self, ax, canvas, fig):
        i, j = place(data, mainRobot[2])
        i2, j2 = place(data, 3)
        # ax.cla()

        # Robot aj ciel
        if i != -1 and j != -1 and i2 != -1 and j2 != -1:
            # if lastY != i or lastX != j:
            cmap = colors.ListedColormap(
                ['White', 'Black', 'Green', 'Green', 'Green', 'White', 'White', 'White', 'White', 'White', 'White',
                 'White', 'White', 'White', 'White', 'White', 'White', 'White', 'White', 'White', 'Orange', 'Orange',
                 'Orange', 'Orange', 'Orange', 'Orange', 'Orange', 'Orange'])
            # cmap = colors.ListedColormap(['White', 'Black', 'Orange', 'Green'])
            ax.pcolor(data[::-1], cmap=cmap, edgecolors='k', linewidths=2)
            plt.gca().set_position([0, 0, 1, 1])

        # Len robot
        elif i != -1 and j != -1:
            # if lastY != i or lastX != j:
            # cmap = colors.ListedColormap(['White', 'Black', 'Orange'])

            cmap = colors.ListedColormap(
                ['White', 'Black', 'White', 'White', 'White', 'White', 'White', 'White', 'White', 'White', 'White',
                 'White', 'White', 'White', 'White', 'White', 'White', 'White', 'White', 'White', 'Orange', 'Orange',
                 'Orange', 'Orange', 'Orange', 'Orange', 'Orange', 'Orange'])

            ax.pcolor(data[::-1], cmap=cmap, edgecolors='k', linewidths=2)
            plt.gca().set_position([0, 0, 1, 1])

        elif i2 != -1 and j2 != -1:
            # if lastY != i or lastX != j:
            cmap = colors.ListedColormap(['White', 'Black', 'Green'])
            ax.pcolor(data[::-1], cmap=cmap, edgecolors='k', linewidths=2)
            plt.gca().set_position([0, 0, 1, 1])

        elif i == -1 and j == -1:
            cmap = colors.ListedColormap(['White', 'Black'])
            ax.pcolor(data[::-1], cmap=cmap, edgecolors='k', linewidths=2)
            plt.gca().set_position([0, 0, 1, 1])

        canvas.draw()

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        global globAnot

        initMap = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        saveData(initMap)
        setData(initMap)

        label = Label(self, text="Publisher", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        label.place(relx=.5, rely=0.05, anchor=CENTER)

        status = Label(self, text="Load map first", font=MEDIUMFONT)
        status.place(relx=.5, rely=0.1, anchor=CENTER)

        # Robo info
        robXlabel = Label(self, text="Robot: [-, -]", font=MEDIUMFONT)
        robXlabel.place(relx=.57, rely=0.35, anchor=W)

        # robYlabel = Label(self, text="Robot Y: ", font=MEDIUMFONT)
        # robYlabel.place(relx=.57, rely=0.35, anchor=W)

        robRotlabel = Label(self, text="Robot direction: ", font=MEDIUMFONT)
        robRotlabel.place(relx=.57, rely=0.4, anchor=W)

        # Goal info
        goalXlabel = Label(self, text="Goal: [-, -]", font=MEDIUMFONT)
        goalXlabel.place(relx=.05, rely=0.3, anchor=W)

        # goalYlabel = Label(self, text="Goal Y: ", font=MEDIUMFONT)
        # goalYlabel.place(relx=.25, rely=0.3, anchor=W)

        # Steering angle
        steerLabel = Label(self, text="Steering angle: ", font=MEDIUMFONT)
        steerLabel.place(relx=.57, rely=0.45, anchor=W)

        # Current speed
        speedLabel = Label(self, text="Current speed: ", font=MEDIUMFONT)
        speedLabel.place(relx=.57, rely=0.5, anchor=W)

        # Odometry stats
        odometrylab = Label(self, text="Odometry: ", font=LARGEFONT)
        odometrylab.place(relx=.57, rely=0.6, anchor=W)

        odomLastPose = Label(self, text="Last pose: ", font=MEDIUMFONT)
        odomLastPose.place(relx=.57, rely=0.65, anchor=W)

        odomNewPose = Label(self, text="New pose: ", font=MEDIUMFONT)
        odomNewPose.place(relx=.57, rely=0.7, anchor=W)

        odomAngles = Label(self, text="Last theta: | Angle:", font=MEDIUMFONT)
        odomAngles.place(relx=.57, rely=0.75, anchor=W)

        odomNewTheta = Label(self, text="New theta:", font=MEDIUMFONT)
        odomNewTheta.place(relx=.57, rely=0.8, anchor=W)

        myX, myY, loadName, saveName = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

        # =================================
        # Prepinanie dlazdic klikanim na mapu
        # =================================
        def on_mouse_click(event):
            if event.inaxes == ax:
                row = len(data) - int(round(event.ydata)) - 1
                col = int(round(event.xdata))
                # value = "[{}, {}]".format(col, row)
                changeCell(col + 1, row + 1)
                # print(value)

        # =================================
        # Manualny pohyb
        # =================================
        def on_key(event):
            kl = event.key

            # if kl == 'w':
            #     move(0, -1)
            # elif kl == 'q':
            #     move(-1, -1)
            # elif kl == 'e':
            #     move(1, -1)
            # elif kl == 'a':
            #     move(-1, 0)
            # elif kl == 'd':
            #     move(1, 0)
            # elif kl == 'z':
            #     move(-1, 1)
            # elif kl == 'x':
            #     move(0, 1)
            # elif kl == 'c':
            #     move(1, 1)

            if kl == 'r':
                i, j = place(data, mainRobot[2])
                row = len(data) - int(round(event.ydata))
                col = int(round(event.xdata)) + 1
                global lastSet
                if i == -1 and j == -1:
                    setLast(False)
                    addRobot(col, row, 20)
                    setLast(True)
                elif (j + 1) == col and (i + 1) == row:
                    setLast(True)
                    removeRobot(mainRobot[2])
                    setLast(False)
                else:
                    status.config(text="Hover robot and press 'r' for delete it")
            elif kl == 'g':
                i, j = place(data, 3)
                row = len(data) - int(round(event.ydata))
                col = int(round(event.xdata)) + 1
                if i == -1 and j == -1:
                    addRobot(col, row, 3)
                elif (j + 1) == col and (i + 1) == row:
                    removeRobot(3)
                else:
                    status.config(text="Hover goal and press 'g' for delete it")

        # Vytvorenie inicializacneho grafu s napisom na mape
        # Tu vieme, ze sa tu nachadzaju len polia s bielou a ciernou farbou
        fig, ax = plt.subplots(figsize=(5, 5))

        cmap = colors.ListedColormap(['White', 'Black'])
        ax.pcolor(data[::-1], cmap=cmap, edgecolors='k', linewidths=2)
        plt.gca().set_position([0, 0, 1, 1])

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().place(relx=0.3, rely=0.65, anchor=CENTER)
        canvas.draw()

        canvas.mpl_connect('button_press_event', on_mouse_click)
        canvas.mpl_connect('key_press_event', on_key)

        # =================================
        # Pridanie robota
        # =================================
        def addRobot(x, y, obj):
            try:
                i, j = place(data, obj)
                if i == -1 and j == -1:
                    if data[int(y) - 1][int(x) - 1] != 1:
                        data[int(y) - 1][int(x) - 1] = obj
                        if obj >= 20 and obj <= 27:

                            # else:
                            #     lastPose[0] = mainRobot[0]
                            #     lastPose[1] = mainRobot[1]
                            #     lastPose[2] = angles[mainRobot[2] - 20]

                            if getLast() == False:
                                lastPose[0] = int(x) - 1
                                lastPose[1] = int(y) - 1
                                lastPose[2] = angles[obj - 20]
                                setLast(True)

                            mainRobot[0] = int(x) - 1
                            mainRobot[1] = int(y) - 1
                            mainRobot[2] = obj

                            # robXlabel.config(text = "Robot X: " + str(mainRobot[0]+1))
                            # robYlabel.config(text = "Robot Y: " + str(mainRobot[1]+1))
                            robXlabel.config(
                                text="Robot: [" + str(mainRobot[0] + 1) + ", " + str(str(mainRobot[1] + 1)) + "]")

                            # robRotlabel.config(text = "Robot direction: " + str(mainRobot[2]))
                            robRotlabel.config(text="Robot direction: " + str(directions[mainRobot[2] - 20]))
                        elif obj == 3:
                            mainGoal[0] = int(x) - 1
                            mainGoal[1] = int(y) - 1
                            # goalXlabel.config(text = "Goal X: " + str(mainGoal[0]+1))
                            # goalYlabel.config(text = "Goal Y: " + str(mainGoal[1]+1))
                            goalXlabel.config(
                                text="Goal: [" + str(mainGoal[0] + 1) + ", " + str(str(mainGoal[1] + 1)) + "]")

                        # saveMap(data)
                        # self.showMap()
                        status.config(text="Object added into map")
                        saveData(data)
                        self.showMap(ax, canvas, fig)
                    else:
                        status.config(text="Object can be added only to free space")

                else:
                    status.config(text="There is already this kind of object in map")
            except:
                status.config(text="Can not add an object")

        # =================================
        # Zmazanie robota
        # =================================
        def removeRobot(obj):
            i, j = place(data, obj)
            if i != -1 and j != -1:
                data[i][j] = 0
                if obj == mainRobot[2]:
                    mainRobot[0] = -1
                    mainRobot[1] = -1
                    mainRobot[2] = -1

                    # robXlabel.config(text = "Robot X: -")
                    # robYlabel.config(text = "Robot Y: -")
                    robXlabel.config(text="Robot: [-, -]")
                    robRotlabel.config(text="Robot direction: -")
                elif obj == 3:
                    mainGoal[0] = -1
                    mainGoal[1] = -1
                    # goalXlabel.config(text = "Goal X: ")
                    # goalYlabel.config(text = "Goal Y: ")
                    goalXlabel.config(text="Goal: [-, -]")

                # saveMap(data)
                # self.showMap()
                # print(data)
                saveData(data)
                status.config(text="Object deleted")
                self.showMap(ax, canvas, fig)
            else:
                status.config(text="No object to delete")
                # print(data)

        # =================================
        # Prepinanie dlazdic
        # =================================
        def changeCell(x, y):
            try:
                if data[int(y) - 1][int(x) - 1] == 0:
                    data[int(y) - 1][int(x) - 1] = 1
                    myText = "Cell changed"
                    self.showMap(ax, canvas, fig)
                elif data[int(y) - 1][int(x) - 1] == 1:
                    data[int(y) - 1][int(x) - 1] = 0
                    myText = "Cell changed"
                    self.showMap(ax, canvas, fig)
                else:
                    myText = "Can not change cell with robot"
            except:
                myText = "Can not change cell"
            # saveMap(data)
            saveData(data)
            # self.showMap()
            status.config(text=myText)

        # =================================
        # Pohyb
        # =================================
        def move(x, y):
            # Zistenie aktualnej polohy robota
            # currY, currX = place(data, 2)
            currY = mainRobot[1]
            currX = mainRobot[0]

            # Overenie, ci sa na mape nejaky robot nachadza
            if currX != -1 and currY != -1:
                # Hore
                if y == -1 and x == 0:
                    if data[currY - 1][currX] != 1 and currY != 0:
                        removeRobot(mainRobot[2])
                        addRobot(currX + 1, currY, 22)
                        status.config(text="Moved UP")
                    else:
                        print("Can not move UP")
                        status.config(text="Can not move UP")
                # Diagonal hore a doprava
                elif y == -1 and x == 1:
                    if currX != int(len(data[0]) - 1):
                        if data[currY - 1][currX] != 1 and data[currY - 1][currX + 1] != 1 and data[currY][currX + 1] != 1 and currY != 0:
                            removeRobot(mainRobot[2])
                            addRobot(currX + 2, currY, 23)
                            status.config(text="Moved R-UP")
                        else:
                            print("Can not move R-UP")
                            status.config(text="Can not move R-UP")
                    else:
                        print("Can not move R-UP")
                        status.config(text="Can not move R-UP")
                # Diagonal hore a dolava
                elif y == -1 and x == -1:
                    if currX != 0:
                        if data[currY - 1][currX] != 1 and data[currY - 1][currX - 1] != 1 and data[currY][
                            currX - 1] != 1 and currY != 0:
                            removeRobot(mainRobot[2])
                            addRobot(currX, currY, 21)
                            status.config(text="Moved L-UP")
                        else:
                            print("Can not move L-UP")
                            status.config(text="Can not move L-UP")
                    else:
                        print("Can not move L-UP")
                        status.config(text="Can not move L-UP")
                # Vlavo
                elif y == 0 and x == -1:
                    if currX != 0:
                        if data[currY][currX - 1] != 1:
                            removeRobot(mainRobot[2])
                            addRobot(currX, currY + 1, 20)
                            status.config(text="Moved LEFT")
                        else:
                            print("Can not move L")
                            status.config(text="Can not move LEFT")
                    else:
                        print("Can not move L")
                        status.config(text="Can not move LEFT")
                # Vpravo
                elif y == 0 and x == 1:
                    if currX != int(len(data) - 1):
                        if data[currY][currX + 1] != 1:
                            removeRobot(mainRobot[2])
                            addRobot(currX + 2, currY + 1, 24)
                            status.config(text="Moved RIGHT")
                        else:
                            print("Can not move R")
                            status.config(text="Can not move RIGHT")
                    else:
                        print("Can not move R")
                        status.config(text="Can not move RIGHT")
                # Diagonal dole a dolava
                elif y == 1 and x == -1:
                    if currY != int(len(data) - 1) and currX != 0:
                        if data[currY + 1][currX] != 1 and data[currY + 1][currX - 1] != 1 and data[currY][
                            currX - 1] != 1:
                            removeRobot(mainRobot[2])
                            addRobot(currX, currY + 2, 27)
                            status.config(text="Moved L-DOWN")
                        else:
                            print("Can not move L-DOWN")
                            status.config(text="Can not move L-DOWN")
                    else:
                        print("Can not move L-DOWN")
                        status.config(text="Can not move L-DOWN")
                # Diagonal dole a doprava
                elif y == 1 and x == 1:
                    if currY != int(len(data) - 1) and currX != int(len(data) - 1):
                        if data[currY + 1][currX] != 1 and data[currY + 1][currX + 1] != 1 and data[currY][
                            currX + 1] != 1:
                            removeRobot(mainRobot[2])
                            addRobot(currX + 2, currY + 2, 25)
                            status.config(text="Moved R-DOWN")
                        else:
                            print("Can not move R-DOWN")
                            status.config(text="Can not move R-DOWN")
                    else:
                        print("Can not move R-DOWN")
                        status.config(text="Can not move R-DOWN")
                # Dole
                elif y == 1 and x == 0:
                    if currY != int(len(data) - 1):
                        if data[currY + 1][currX] != 1:
                            removeRobot(mainRobot[2])
                            addRobot(currX + 1, currY + 2, 26)
                            status.config(text="Moved DOWN")
                        else:
                            print("Can not move DOWN")
                            status.config(text="Can not move DOWN")
                    else:
                        print("Can not move DOWN")
                        status.config(text="Can not move DOWN")
                self.showMap(ax, canvas, fig)
            else:
                print("No robot to move")
                status.config(text="No robot to move")

        # =================================
        # Nacitanie mapy
        # =================================
        def loadMap(name):
            try:
                rows = []
                df = pd.read_csv(r'%s' % name, header=None)
                csvreader = df.values.tolist()

                for row in csvreader:
                    rows.append(row)
                for i in range(0, len(rows)):
                    for j in range(0, len(rows[0])):
                        if rows[i][j] == 'ď»ż1':
                            rows[i][j] = int(1)
                        elif rows[i][j] == 'ď»ż0':
                            rows[i][j] = int(0)
                        else:
                            rows[i][j] = int(rows[i][j])
                setData(rows[:][:])

                saveData(data)
                status.config(text="Map loaded succesfully")

                i, j = place(data, 28)
                if i != -1 and j != -1:
                    global lastSet
                    mainRobot[0] = j
                    mainRobot[1] = i
                    lastPose[0] = i
                    lastPose[1] = j
                    setLast(True)
                    # robXlabel.config(text = "Robot X: " + str(mainRobot[0]+1))
                    # robYlabel.config(text = "Robot Y: " + str(mainRobot[1]+1))
                    robXlabel.config(text="Robot: [" + str(mainRobot[0] + 1) + ", " + str(str(mainRobot[1] + 1)) + "]")
                    robRotlabel.config(text="Robot direction: " + str(directions[mainRobot[2] - 20]))

                i, j = place(data, 3)
                if i != -1 and j != -1:
                    mainGoal[0] = j
                    mainGoal[1] = i
                    # goalXlabel.config(text = "Goal X: " + str(mainGoal[0]+1))
                    # goalYlabel.config(text = "Goal Y: " + str(mainGoal[1]+1))
                    goalXlabel.config(text="Goal: [" + str(mainGoal[0] + 1) + ", " + str(str(mainGoal[1] + 1)) + "]")

                self.showMap(ax, canvas, fig)
            except Exception as e:
                print(e)
                status.config(text="No file found")

        # =================================
        # Nacitanie mapy
        # =================================
        def select_file():
            filetypes = (
                ('csv files', '*.csv'),
                ('All files', '*.*'))

            filename = fd.askopenfilename(title='Open a file', initialdir='/home/nmvr/Desktop/', filetypes=filetypes)
            showinfo(title='Selected File', message=filename)
            loadMap(filename)

        # =================================
        # Cityblock vzdialenost
        # =================================
        def cityBlock():
            # euc = round(sqrt(pow((mainGoal[0] - mainRobot[0]), 2) + pow((mainGoal[1] - mainRobot[1]), 2)), 2)
            city = cityblock([mainGoal[0], mainGoal[1]], [mainRobot[0], mainRobot[1]])
            if city <= 2:
                return 1.75
            elif city <= 4:
                return 1.5
            elif city <= 6:
                return 1
            else:
                return .5

        # =================================
        # Uhol otocenia
        # =================================
        def steerAng():
            steerX, steerY = 0, 0

            if mainGoal[0] < mainRobot[0] and mainGoal[1] < mainRobot[1]:
                steerX = -1
                steerY = -1
                steerLabel.config(text="Steering angle: 45°")
                tang_vel = 45
            elif mainGoal[0] > mainRobot[0] and mainGoal[1] < mainRobot[1]:
                steerX = 1
                steerY = -1
                steerLabel.config(text="Steering angle: 135°")
                tang_vel = 135
            elif mainGoal[0] < mainRobot[0] and mainGoal[1] > mainRobot[1]:
                steerX = -1
                steerY = 1
                steerLabel.config(text="Steering angle: 315°")
                tang_vel = 315
            elif mainGoal[0] > mainRobot[0] and mainGoal[1] > mainRobot[1]:
                steerX = 1
                steerY = 1
                steerLabel.config(text="Steering angle: 225°")
                tang_vel = 225
            elif mainGoal[0] < mainRobot[0] and mainGoal[1] == mainRobot[1]:
                steerX = -1
                steerY = 0
                steerLabel.config(text="Steering angle: 0°")
                tang_vel = 0
            elif mainGoal[0] > mainRobot[0] and mainGoal[1] == mainRobot[1]:
                steerX = 1
                steerY = 0
                steerLabel.config(text="Steering angle: 180°")
                tang_vel = 180
            elif mainGoal[0] == mainRobot[0] and mainGoal[1] < mainRobot[1]:
                steerX = 0
                steerY = -1
                steerLabel.config(text="Steering angle: 90°")
                tang_vel = 90
            elif mainGoal[0] == mainRobot[0] and mainGoal[1] > mainRobot[1]:
                steerX = 0
                steerY = 1
                steerLabel.config(text="Steering angle: 270°")
                tang_vel = 270
            # steerLabel.config(text = "Steering angle: " + str(steerAngle))

            tang_vel = tang_vel - angles[mainRobot[2] - 20]
            if tang_vel >= 360:
                tang_vel -= 360

            set_avel(tang_vel)
            return steerX, steerY

        # =================================
        # Calculate odometry
        # =================================
        def odomCal(l_vel):
            d_r, d_l = 0, 0

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

            odomLastPose.config(text="Last pose: [" + str(lastPose[0] + 1) + ", " + str(lastPose[1] + 1) + "]")
            odomNewPose.config(text="New pose: [" + str(newX) + ", " + str(newY) + "]")
            odomAngles.config(text="Last theta: " + str(lastPose[2]) + "° | angle: " + str(get_avel()) + "°")
            odomNewTheta.config(text="New theta: " + str(newTeta) + "°")

            # Aktualizovanie poslednej polohy
            lastPose[0] = newX - 1
            lastPose[1] = newY - 1
            lastPose[2] = newTeta

        # =================================
        # Go to goal
        # =================================
        def go2goal():
            while mainGoal[0] != mainRobot[0] or mainGoal[1] != mainRobot[1]:
                goX, goY = steerAng()
                Preg = cityBlock() * mainRobot[3]

                move(goX, goY)
                speedLabel.config(text="Current speed: " + str(2 - Preg))
                odomCal(Preg)
                time.sleep(Preg)

            speedLabel.config(text="Current speed: 0")

        exit_button = Button(self, text="Exit", command=root.destroy)
        exit_button.place(relx=.85, rely=.95, height=40, width=100, anchor=CENTER)

        loadB = Button(self, text="Load map", font=MEDIUMFONT, command=select_file)
        loadB.place(relx=.5, rely=.15, height=40, width=150, anchor=CENTER)
        loadB.config(bg="green", fg="black")

        goTogoalB = Button(self, text="Go 2 Goal", font=MEDIUMFONT, command=go2goal)
        goTogoalB.place(relx=.57, rely=.3, height=40, width=200, anchor=W)
        goTogoalB.config(bg="cyan", fg="black")


root = tk.Tk()


def quit_me():
    print("Close publisher app")
    root.quit()
    root.destroy()


def main():
    view = NMVR(root)
    view.pack(side="top", fill="both", expand=True)
    root.geometry("1100x800")
    root.resizable(0, 0)
    root.protocol("MW_DELETE_WINDOW", quit_me)
    root.title("Publisher")
    root.mainloop()


if __name__ == '__main__':
    main()
