from matplotlib import pyplot as plt
from matplotlib import colors
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from tkinter import *
import tkinter as tk
import numpy as np
import os
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from math import cos, pow, atan2, sqrt, dist, sin, floor
import math
from pandas.io import api
from scipy.spatial.distance import cityblock, euclidean
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

data, mapStat, myDir, globAnot, lastSet, ang_vel = [], False, os.getcwd() + "/", 0, False, 0
# --------------------[x, y, rot, speed, view]
mainRobot, mainGoal, lastPose = [-1, -1, -1, 1, 4], [-1, -1], [-1, -1, -1]
angles, directions = [0, 45, 90, 135, 180, 225, 270, 315, 360], ["West", "North-west", "North", "North-east", "East",
                                                                 "South-east", "South", "South-west"]

running, byClick, Alist, globDone, AsLast, globIndx, OldList, mainStart, pathList = False, False, [], False, [], 0, [], [
    -1, -1], []
startPath = []


# Alist - nieco ako closed list finalnej cesty
# pathList - zredukovanie cesty na najkratsiu
# OldList - suradnice starej strasy a ich ceny

def set_startPath(val):
    global startPath
    startPath = val


def get_startPath():
    global startPath
    return startPath


def set_pathList(val, type):
    global pathList
    if type == 0:
        pathList.pop()
    elif type == 1:
        print("From function: ", val)
        pathList.remove(val)


def get_pathList():
    global pathList
    return pathList


def copyList():
    global Alist, pathList
    pathList = Alist.copy()
    pathList.reverse()


def set_globIndx(indx):
    global globIndx
    globIndx = indx


def get_globIndx():
    global globIndx
    return globIndx


def set_AsLast(val):
    global AsLast
    AsLast = val


def get_AsLast():
    global AsLast
    return AsLast


def set_globDone(val):
    global globDone
    globDone = val


def get_globDone():
    global globDone
    return globDone


def get_Alist():
    global Alist
    return Alist


def set_Alist(val, type):
    global Alist, pathList
    if type == 0:
        Alist.append(val)
    elif type == 1:
        Alist.pop()
        Alist.append(val)
    elif type == -1:
        Alist.clear()
    elif type == -2:
        Alist.clear()
        Alist = val.copy()
        Alist.reverse()
    elif type == -3:
        Alist.clear()
        Alist = val.copy()
    elif type == -4:
        Alist.pop(0)


def get_oldList():
    global OldList
    return OldList


def set_oldList(typeF):
    global OldList

    if typeF == 0:
        if len(get_Alist()) > 0:
            OldList.append(get_Alist())
            set_Alist(None, -1)
    elif typeF == -1:
        OldList.clear()


def set_click(val):
    global byClick
    byClick = val


def get_click():
    global byClick
    return byClick


def set_running(val):
    global running
    running = val


def get_running():
    global running
    return running


# Globalne uchovavanie mapy
def setData(inD):
    global data
    data = inD


def getData():
    global data
    return data


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


ARR = ("Verdana", 50)
LARGEFONT = ("Verdana", 35)
MEDIUMFONT = ("Verdana", 19)
MINIFONT = ("Verdana", 15)


class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher = self.create_publisher(String, 'topic', 1)

        timer_period = .5
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = '%s' % str(data)
        self.publisher.publish(msg)
        # self.get_logger().info('"%s"' % msg.data)
        self.get_logger().info('Sending map')


class NMVR(tk.Frame):

    # Vykreslovanie mapy a objektov na nej
    def showMap(self, ax, canvas, fig):
        mycmap = colors.ListedColormap(['white', 'black', 'green', 'blue', 'gray', 'orange'])
        norm = colors.BoundaryNorm([0, .9, 2.9, 3.9, 4.9, 19.9, 28], mycmap.N)
        ax.pcolor(data[::-1], cmap=mycmap, norm=norm, edgecolors='k', linewidths=2)
        plt.gca().set_position([0, 0, 1, 1])
        canvas.draw()

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        global globAnot
        rclpy.init(args=None)
        minimal_publisher = MinimalPublisher()

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

        # Start info
        startXlabel = Label(self, text="Start: [-, -]", font=MEDIUMFONT)
        startXlabel.place(relx=.25, rely=0.3, anchor=W)

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

        # Odometry stats
        sipka = Label(self, text="", font=ARR)
        sipka.place(relx=.65, rely=0.9, anchor=CENTER)

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
        # Vkladanie robota a ciela
        # ================================= 
        def on_key(event):
            kl = event.key

            if kl == 'r':
                i, j = place(data, mainRobot[2])
                row = len(data) - int(round(event.ydata))
                col = int(round(event.xdata)) + 1
                global lastSet
                if i == -1 and j == -1:
                    setLast(False)
                    set_click(True)
                    addRobot(col, row, 20)
                    setLast(True)
                elif (j + 1) == col and (i + 1) == row:
                    setLast(True)
                    set_click(True)
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
        # Sipka
        # ================================= 
        def arrDir(dir):
            if dir == 20:
                sipka.config(text="←")
            elif dir == 21:
                sipka.config(text="↖")
            elif dir == 22:
                sipka.config(text="↑")
            elif dir == 23:
                sipka.config(text="↗")
            elif dir == 24:
                sipka.config(text="→")
            elif dir == 25:
                sipka.config(text="↘")
            elif dir == 26:
                sipka.config(text="↓")
            elif dir == 27:
                sipka.config(text="↙")
            else:
                sipka.config(text="")

        # =================================
        # Pridanie robota
        # ================================= 
        def addRobot(x, y, obj):
            try:
                i, j = place(data, obj)
                if obj == 4:
                    i = -1
                    j = -1

                if i == -1 and j == -1:
                    if data[int(y) - 1][int(x) - 1] != 1:
                        data[int(y) - 1][int(x) - 1] = obj
                        if obj >= 20 and obj <= 27:

                            if get_click():
                                mainStart[0] = int(x) - 1
                                mainStart[1] = int(y) - 1
                                startXlabel.config(
                                    text="Start: [" + str(mainStart[0] + 1) + ", " + str(mainStart[1] + 1) + "]")
                                set_click(False)

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
                            arrDir(mainRobot[2])
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
                        if obj != 4 and obj != '4':
                            self.showMap(ax, canvas, fig)
                            rclpy.spin_once(minimal_publisher)
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
                if get_running():
                    data[i][j] = 4
                else:
                    data[i][j] = 0

                if obj == mainRobot[2]:
                    mainRobot[0] = -1
                    mainRobot[1] = -1
                    mainRobot[2] = -1

                    # robXlabel.config(text = "Robot X: -")
                    # robYlabel.config(text = "Robot Y: -")
                    robXlabel.config(text="Robot: [-, -]")
                    robRotlabel.config(text="Robot direction: -")
                    arrDir(0)

                    if get_click():
                        rclpy.spin_once(minimal_publisher)
                        mainStart[0] = -1
                        mainStart[1] = -1
                        startXlabel.config(text="Start: [-, -]")
                        self.showMap(ax, canvas, fig)
                        set_click(False)

                elif obj == 3:
                    mainGoal[0] = -1
                    mainGoal[1] = -1
                    goalXlabel.config(text="Goal: [-, -]")
                    rclpy.spin_once(minimal_publisher)
                    self.showMap(ax, canvas, fig)

                status.config(text="Object deleted")

            else:
                status.config(text="No object to delete")
                # print(data)

        # =================================
        # Prepinanie dlazdic
        # ================================= 
        def changeCell(x, y):
            try:
                if data[int(y) - 1][int(x) - 1] == 0 or data[int(y) - 1][int(x) - 1] == 4:
                    data[int(y) - 1][int(x) - 1] = 1
                    myText = "Cell changed"
                    self.showMap(ax, canvas, fig)
                    rclpy.spin_once(minimal_publisher)
                # elif data[int(y)-1][int(x)-1] == 4:
                #     data[int(y)-1][int(x)-1] = 1
                #     myText = "Path blocked"
                #     self.showMap(ax, canvas, fig)
                #     set_globDone(True)
                #     set_running(False)
                #     rclpy.spin_once(minimal_publisher)
                elif data[int(y) - 1][int(x) - 1] == 1:
                    data[int(y) - 1][int(x) - 1] = 0
                    myText = "Cell changed"
                    self.showMap(ax, canvas, fig)
                    rclpy.spin_once(minimal_publisher)
                else:
                    myText = "Can not change cell with robot"

                # print(int(y)-1, int(x)-1, data[int(y)-1][int(x)-1])
            except:
                myText = "Can not change cell"

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
                        if data[currY - 1][currX + 1] != 1 and (
                                data[currY - 1][currX] != 1 or data[currY][currX + 1] != 1) and currY != 0:
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
                        if data[currY - 1][currX - 1] != 1 and (
                                data[currY - 1][currX] != 1 or data[currY][currX - 1] != 1) and currY != 0:
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
                        if data[currY + 1][currX - 1] != 1 and (
                                data[currY + 1][currX] != 1 or data[currY][currX - 1] != 1):
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
                        if data[currY + 1][currX + 1] != 1 and (
                                data[currY + 1][currX] != 1 or data[currY][currX + 1] != 1):
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
                status.config(text="Map loaded succesfully")

                i, j = place(data, 28)
                if i != -1 and j != -1:
                    global lastSet
                    mainRobot[0] = j
                    mainRobot[1] = i
                    lastPose[0] = i
                    lastPose[1] = j
                    setLast(True)
                    arrDir(mainRobot[2])
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
                set_Alist(None, -1)
                rclpy.spin_once(minimal_publisher)
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
            Preg = 0
            if city <= 2:
                Preg = .75
            elif city <= 4:
                Preg = .5
            elif city <= 6:
                Preg = .25
            else:
                Preg = .1

            speedLabel.config(text="Current speed: " + str(mainRobot[3] - Preg * mainRobot[3]))
            return Preg

        # =================================
        # Uhol otocenia
        # ================================= 
        def steerAng(pathX, pathY):
            steerX, steerY = 0, 0

            if pathX < mainRobot[0] and pathY < mainRobot[1]:
                steerX = -1
                steerY = -1
                steerLabel.config(text="Steering angle: 45°")
                tang_vel = 45
            elif pathX > mainRobot[0] and pathY < mainRobot[1]:
                steerX = 1
                steerY = -1
                steerLabel.config(text="Steering angle: 135°")
                tang_vel = 135
            elif pathX < mainRobot[0] and pathY > mainRobot[1]:
                steerX = -1
                steerY = 1
                steerLabel.config(text="Steering angle: 315°")
                tang_vel = 315
            elif pathX > mainRobot[0] and pathY > mainRobot[1]:
                steerX = 1
                steerY = 1
                steerLabel.config(text="Steering angle: 225°")
                tang_vel = 225
            elif pathX < mainRobot[0] and pathY == mainRobot[1]:
                steerX = -1
                steerY = 0
                steerLabel.config(text="Steering angle: 0°")
                tang_vel = 0
            elif pathX > mainRobot[0] and pathY == mainRobot[1]:
                steerX = 1
                steerY = 0
                steerLabel.config(text="Steering angle: 180°")
                tang_vel = 180
            elif pathX == mainRobot[0] and pathY < mainRobot[1]:
                steerX = 0
                steerY = -1
                steerLabel.config(text="Steering angle: 90°")
                tang_vel = 90
            elif pathX == mainRobot[0] and pathY > mainRobot[1]:
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
        def odomCal():
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
        # Hladanie cesty
        # ================================= 
        def checkAround(midSur):

            Flist, SurList, FlistVisit, SuristVisit, minList, minSur = [], [], [], [], 0, []

            # Lavo 
            if 20 <= data[midSur[1]][midSur[0] - 1] <= 27:
                Flist.append(midSur[2])
                SurList.append([midSur[0] - 1, midSur[1]])
                set_globDone(True)
            elif data[midSur[1]][midSur[0] - 1] == 0 or data[midSur[1]][midSur[0] - 1] == 5:
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] - 1, midSur[1]]))
                SurList.append([midSur[0] - 1, midSur[1]])
            elif data[midSur[1]][midSur[0] - 1] == 4:
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] - 1, midSur[1]]))
                SuristVisit.append([midSur[0] - 1, midSur[1]])

            # Lavo - hore
            if 20 <= data[midSur[1] - 1][midSur[0] - 1] <= 27 and (
                    data[midSur[1]][midSur[0] - 1] == 0 or data[midSur[1]][midSur[0] - 1] == 5) and (
                    data[midSur[1] - 1][midSur[0]] == 0 or data[midSur[1] - 1][midSur[0]] == 5):
                Flist.append(midSur[2])
                SurList.append([midSur[0] - 1, midSur[1] - 1])
                set_globDone(True)
            elif (data[midSur[1] - 1][midSur[0] - 1] == 0 or data[midSur[1] - 1][midSur[0] - 1] == 5) and (
                    data[midSur[1]][midSur[0] - 1] == 0 or data[midSur[1]][midSur[0] - 1] == 5) and (
                    data[midSur[1] - 1][midSur[0]] == 0 or data[midSur[1] - 1][midSur[0]] == 5):
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] - 1, midSur[1] - 1]))
                SurList.append([midSur[0] - 1, midSur[1] - 1])
            elif (data[midSur[1] - 1][midSur[0] - 1] == 0 or data[midSur[1] - 1][midSur[0] - 1] == 5) and \
                    data[midSur[1]][midSur[0] - 1] == 4 and data[midSur[1] - 1][midSur[0]] == 4:
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] - 1, midSur[1] - 1]))
                SurList.append([midSur[0] - 1, midSur[1] - 1])
            elif data[midSur[1] - 1][midSur[0] - 1] == 4 and data[midSur[1]][midSur[0] - 1] == 4 and \
                    data[midSur[1] - 1][midSur[0]] == 4:
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] - 1, midSur[1] - 1]))
                SuristVisit.append([midSur[0] - 1, midSur[1] - 1])
            elif (data[midSur[1] - 1][midSur[0] - 1] == 0 or data[midSur[1] - 1][midSur[0] - 1] == 4 or
                  data[midSur[1] - 1][midSur[0] - 1] == 5) and (
                    data[midSur[1]][midSur[0] - 1] == 0 or data[midSur[1]][midSur[0] - 1] == 4 or data[midSur[1]][
                midSur[0] - 1] == 5) and (
                    data[midSur[1] - 1][midSur[0]] == 0 or data[midSur[1] - 1][midSur[0]] == 4 or data[midSur[1] - 1][
                midSur[0]] == 5):
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] - 1, midSur[1] - 1]))
                SuristVisit.append([midSur[0] - 1, midSur[1] - 1])

            # Hore
            if 20 <= data[midSur[1] - 1][midSur[0]] <= 27:
                Flist.append(midSur[2])
                SurList.append([midSur[0], midSur[1] - 1])
                set_globDone(True)
            elif (data[midSur[1] - 1][midSur[0]] == 0 or data[midSur[1] - 1][midSur[0]] == 5):
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0], midSur[1] - 1]))
                SurList.append([midSur[0], midSur[1] - 1])
            elif data[midSur[1] - 1][midSur[0]] == 4:
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0], midSur[1] - 1]))
                SuristVisit.append([midSur[0], midSur[1] - 1])

            # Vpravo - hore
            if 20 <= data[midSur[1] - 1][midSur[0] + 1] <= 27 and (
                    data[midSur[1] - 1][midSur[0]] == 0 or data[midSur[1] - 1][midSur[0]] == 5) and (
                    data[midSur[1]][midSur[0] + 1] == 0 or data[midSur[1]][midSur[0] + 1] == 5):
                Flist.append(midSur[2])
                SurList.append([midSur[0] + 1, midSur[1] - 1])
                set_globDone(True)
            elif (data[midSur[1] - 1][midSur[0] + 1] == 0 or data[midSur[1] - 1][midSur[0] + 1] == 5) and (
                    data[midSur[1] - 1][midSur[0]] == 0 or data[midSur[1] - 1][midSur[0]] == 5) and (
                    data[midSur[1]][midSur[0] + 1] == 0 or data[midSur[1]][midSur[0] + 1] == 5):
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] + 1, midSur[1] - 1]))
                SurList.append([midSur[0] + 1, midSur[1] - 1])
            elif (data[midSur[1] - 1][midSur[0] + 1] == 0 or data[midSur[1] - 1][midSur[0] + 1] == 5) and \
                    data[midSur[1] - 1][midSur[0]] == 4 and data[midSur[1]][midSur[0] + 1] == 4:
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] + 1, midSur[1] - 1]))
                SurList.append([midSur[0] + 1, midSur[1] - 1])
            elif data[midSur[1] - 1][midSur[0] + 1] == 4 and data[midSur[1] - 1][midSur[0]] == 4 and data[midSur[1]][
                midSur[0] + 1] == 4:
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] + 1, midSur[1] - 1]))
                SuristVisit.append([midSur[0] + 1, midSur[1] - 1])
            elif (data[midSur[1] - 1][midSur[0] + 1] == 0 or data[midSur[1] - 1][midSur[0] + 1] == 4 or
                  data[midSur[1] - 1][midSur[0] + 1] == 5) and (
                    data[midSur[1] - 1][midSur[0]] == 0 or data[midSur[1] - 1][midSur[0]] == 4 or data[midSur[1] - 1][
                midSur[0]] == 5) and (
                    data[midSur[1]][midSur[0] + 1] == 0 or data[midSur[1]][midSur[0] + 1] == 4 or data[midSur[1]][
                midSur[0] + 1] == 5):
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] + 1, midSur[1] - 1]))
                SuristVisit.append([midSur[0] + 1, midSur[1] - 1])

            # Vpravo
            if 20 <= data[midSur[1]][midSur[0] + 1] <= 27:
                Flist.append(midSur[2])
                SurList.append([midSur[0] + 1, midSur[1]])
                set_globDone(True)
            elif (data[midSur[1]][midSur[0] + 1] == 0 or data[midSur[1]][midSur[0] + 1] == 5):
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] + 1, midSur[1]]))
                SurList.append([midSur[0] + 1, midSur[1]])
            elif data[midSur[1]][midSur[0] + 1] == 4:
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] + 1, midSur[1]]))
                SuristVisit.append([midSur[0] + 1, midSur[1]])

            # Vpravo - dole
            if 20 <= data[midSur[1] + 1][midSur[0] + 1] <= 27 and (
                    data[midSur[1]][midSur[0] + 1] == 0 or data[midSur[1]][midSur[0] + 1] == 5) and (
                    data[midSur[1] + 1][midSur[0]] == 0 or data[midSur[1] + 1][midSur[0]] == 5):
                Flist.append(midSur[2])
                SurList.append([midSur[0] + 1, midSur[1] + 1])
                set_globDone(True)
            elif (data[midSur[1] + 1][midSur[0] + 1] == 0 or data[midSur[1] + 1][midSur[0] + 1] == 5) and (
                    data[midSur[1]][midSur[0] + 1] == 0 or data[midSur[1]][midSur[0] + 1] == 5) and (
                    data[midSur[1] + 1][midSur[0]] == 0 or data[midSur[1] + 1][midSur[0]] == 5):
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] + 1, midSur[1] + 1]))
                SurList.append([midSur[0] + 1, midSur[1] + 1])
            elif (data[midSur[1] + 1][midSur[0] + 1] == 0 or data[midSur[1] + 1][midSur[0] + 1] == 5) and \
                    data[midSur[1]][midSur[0] + 1] == 4 and data[midSur[1] + 1][midSur[0]] == 4:
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] + 1, midSur[1] + 1]))
                SurList.append([midSur[0] + 1, midSur[1] + 1])
            elif data[midSur[1] + 1][midSur[0] + 1] == 4 and data[midSur[1]][midSur[0] + 1] == 4 and \
                    data[midSur[1] + 1][midSur[0]] == 4:
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] + 1, midSur[1] + 1]))
                SuristVisit.append([midSur[0] + 1, midSur[1] + 1])
            elif (data[midSur[1] + 1][midSur[0] + 1] == 0 or data[midSur[1] + 1][midSur[0] + 1] == 4 or
                  data[midSur[1] + 1][midSur[0] + 1] == 5) and (
                    data[midSur[1]][midSur[0] + 1] == 0 or data[midSur[1]][midSur[0] + 1] == 4 or data[midSur[1]][
                midSur[0] + 1] == 5) and (
                    data[midSur[1] + 1][midSur[0]] == 0 or data[midSur[1] + 1][midSur[0]] == 4 or data[midSur[1] + 1][
                midSur[0]] == 5):
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] + 1, midSur[1] + 1]))
                SuristVisit.append([midSur[0] + 1, midSur[1] + 1])

            # Dole
            if 20 <= data[midSur[1] + 1][midSur[0]] <= 27:
                Flist.append(midSur[2])
                SurList.append([midSur[0], midSur[1] + 1])
                set_globDone(True)
            elif (data[midSur[1] + 1][midSur[0]] == 0 or data[midSur[1] + 1][midSur[0]] == 5):
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0], midSur[1] + 1]))
                SurList.append([midSur[0], midSur[1] + 1])
            elif data[midSur[1] + 1][midSur[0]] == 4:
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0], midSur[1] + 1]))
                SuristVisit.append([midSur[0], midSur[1] + 1])

            # Lavo dole
            if 20 <= data[midSur[1] + 1][midSur[0] - 1] <= 27 and (
                    data[midSur[1] + 1][midSur[0]] == 0 or data[midSur[1] + 1][midSur[0]] == 5) and (
                    data[midSur[1]][midSur[0] - 1] == 0 or data[midSur[1]][midSur[0] - 1] == 5):
                Flist.append(midSur[2])
                SurList.append([midSur[0] - 1, midSur[1] + 1])
                set_globDone(True)
            elif (data[midSur[1] + 1][midSur[0] - 1] == 0 or data[midSur[1] + 1][midSur[0] - 1] == 5) and (
                    data[midSur[1] + 1][midSur[0]] == 0 or data[midSur[1] + 1][midSur[0]] == 5) and (
                    data[midSur[1]][midSur[0] - 1] == 0 or data[midSur[1]][midSur[0] - 1] == 5):
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] - 1, midSur[1] + 1]))
                SurList.append([midSur[0] - 1, midSur[1] + 1])
            elif (data[midSur[1] + 1][midSur[0] - 1] == 0 or data[midSur[1] + 1][midSur[0] - 1] == 5) and \
                    data[midSur[1] + 1][midSur[0]] == 4 and data[midSur[1]][midSur[0] - 1] == 4:
                Flist.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] - 1, midSur[1] + 1]))
                SurList.append([midSur[0] - 1, midSur[1] + 1])
            elif data[midSur[1] + 1][midSur[0] - 1] == 4 and data[midSur[1] + 1][midSur[0]] == 4 and data[midSur[1]][
                midSur[0] - 1] == 4:
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] - 1, midSur[1] + 1]))
                SuristVisit.append([midSur[0] - 1, midSur[1] + 1])
            elif (data[midSur[1] + 1][midSur[0] - 1] == 0 or data[midSur[1] + 1][midSur[0] - 1] == 4 or
                  data[midSur[1] + 1][midSur[0] - 1] == 5) and (
                    data[midSur[1] + 1][midSur[0]] == 0 or data[midSur[1] + 1][midSur[0]] == 4 or data[midSur[1] + 1][
                midSur[0]] == 5) and (
                    data[midSur[1]][midSur[0] - 1] == 0 or data[midSur[1]][midSur[0] - 1] == 4 or data[midSur[1]][
                midSur[0] - 1] == 5):
                FlistVisit.append(midSur[2] + euclidean([mainRobot[0], mainRobot[1]], [midSur[0] - 1, midSur[1] + 1]))
                SuristVisit.append([midSur[0] - 1, midSur[1] + 1])

            # Rozhodnutie ktora cesta je najkratsia 
            # V pripade nejakej pasce pokus o navrat spat
            # FlistVisit a SuristVisit su suradnice uz navstivenych suradnic (closed)
            # Flist a minList su suradnice este nenavstivenych suradnic ktore sa overuju (opened)

            if len(Flist) == 0 and 1 < len(FlistVisit) <= 3:
                lastMove = [get_Alist()[-3][0], get_Alist()[-3][1]]
                try:
                    FlistVisit.pop(SuristVisit.index(lastMove))
                    SuristVisit.remove(lastMove)
                    print("Removed")
                except:
                    print("Cant remove ")

                minList = max(FlistVisit)
                minSur = SuristVisit[FlistVisit.index(minList)]
            elif len(Flist) == 0:
                minList = max(FlistVisit)
                minSur = SuristVisit[FlistVisit.index(minList)]
            else:
                minList = min(Flist)
                minSur = SurList[Flist.index(minList)]

            # print("Non visited list: ", Flist, " and I picked: ", minList)
            print("Visited list: ", SuristVisit)
            print("Len of visited list: ", len(FlistVisit))

            set_Alist([minSur[0], minSur[1], minList], 1)

            if get_globDone():
                print("In da goal")

            addRobot(minSur[0] + 1, minSur[1] + 1, 4)
            # data[minSur[0]][minSur[1]] = int(4)
            # self.showMap(ax, canvas, fig)

        def pickPack():
            copyList()
            templist = []

            templist.append(get_pathList()[0])
            set_pathList(get_pathList()[0], 1)

            while templist[-1][0] != mainGoal[0] or templist[-1][1] != mainGoal[1]:
                # print("Temp List [-1]: ", templist[-1], " startPath: ", get_startPath())

                myList = []
                for x in pathList:
                    if [x[0], x[1]] == [templist[-1][0] + 1, templist[-1][1]] or [x[0], x[1]] == [templist[-1][0] - 1,
                                                                                                  templist[-1][1]] or [
                        x[0], x[1]] == [templist[-1][0], templist[-1][1] + 1] or [x[0], x[1]] == [templist[-1][0],
                                                                                                  templist[-1][1] - 1]:
                        myList.append(x)
                    # Vlavo hore
                    elif [x[0], x[1]] == [templist[-1][0] - 1, templist[-1][1] - 1] and (
                            data[x[0]][x[1] + 1] != 1 or data[x[0] + 1][x[1]] != 1):
                        myList.append(x)
                    # Vpravo hore
                    elif [x[0], x[1]] == [templist[-1][0] + 1, templist[-1][1] - 1] and (
                            data[x[0]][x[1] + 1] != 1 or data[x[0] - 1][x[1]] != 1):
                        myList.append(x)
                    # Vlavo dole
                    elif [x[0], x[1]] == [templist[-1][0] - 1, templist[-1][1] + 1] and (
                            data[x[0]][x[1] + 1] != 1 or data[x[0] + 1][x[1]] != 1):
                        myList.append(x)
                    # Vpravo dole
                    elif [x[0], x[1]] == [templist[-1][0] + 1, templist[-1][1] + 1] and (
                            data[x[0]][x[1] + 1] != 1 or data[x[0] - 1][x[1]] != 1):
                        myList.append(x)

                min, minsur = math.inf, []
                for x in myList:
                    if x[2] < min:
                        min = x[2]
                        minsur = x
                print("\n---\nTempList: ", templist, "\n\npathList: ", get_pathList(), "\n\nminsur: ", minsur,
                      "\n\nmainGoal: ", mainGoal, "\n---\n")
                # pathList.remove(minsur)
                if len(minsur) > 0:
                    set_pathList(minsur, 1)
                    templist.append(minsur)

            for i in range(0, len(data)):
                for j in range(0, len(data[0])):
                    if data[i][j] == 4 or data[i][j] == '4':
                        data[i][j] = int(0)

            for x in templist:
                addRobot(x[0] + 1, x[1] + 1, 4)

            print(templist)
            set_Alist(templist, -3)
            set_Alist(templist, -4)
            print(get_Alist())
            addRobot(mainRobot[0] + 1, mainRobot[1] + 1, 20)
            self.showMap(ax, canvas, fig)
            rclpy.spin_once(minimal_publisher)
            set_running(True)
            go2goal()

            # =================================

        # Pohyb po ceste
        # =================================
        def checkPath(indx, sup):
            try:
                # if mainRobot[4] + indx > indx + sup:
                print("\nalist len: ", len(get_Alist()), " checking: ", indx + sup, "\n")

                if (indx + sup) >= len(get_Alist()):
                    followPath()
                    if mainRobot[0] == mainGoal[0] and mainRobot[1] == mainGoal[1]:
                        print("\n\nDi end\n\n")
                        set_globDone(True)
                        set_running(False)
                        status.config(text="In the goal :)")
                        speedLabel.config(text="Current speed: 0")

                    # print("\n\nhehe\n\n")
                elif mainRobot[4] + indx > indx + sup:
                    if data[get_Alist()[indx + sup][1]][get_Alist()[indx + sup][0]] != 1:
                        self.after(100, checkPath(indx, sup + 1))
                    else:
                        set_globDone(True)
                        set_running(False)
                        for i in range(0, len(data)):
                            for j in range(0, len(data[0])):
                                if data[i][j] == 4 or data[i][j] == '4':
                                    data[i][j] = int(5)

                        set_oldList(0)
                        set_globIndx(0)
                        set_globDone(False)

                        addRobot(mainGoal[0] + 1, mainGoal[1] + 1, 3)
                        self.showMap(ax, canvas, fig)
                        rclpy.spin_once(minimal_publisher)
                        status.config(text="Recalculating path")
                        Dstar()
                else:
                    followPath()
                    # if mainGoal[0] == mainRobot[0]-1 and mainGoal[1] == mainRobot[1]-1:
                    #     set_globDone(True)
                    #     set_running(False)
                    #     status.config(text="In the goal :)")
                    #     speedLabel.config(text = "Current speed: 0")
                    # else:
                    #     followPath()
            except Exception as e:
                # for i in range(0, mainRobot[4]-1):
                #     followPath()
                #     time.sleep(mainRobot[3] * cityBlock())
                set_globDone(True)
                set_running(False)
                status.config(text="Something went wrong, stopped D*Lite and movement")
                print(e)
                speedLabel.config(text="Current speed: 0")

        def followPath():
            pathLen = len(get_Alist())
            indx = get_globIndx()
            if indx <= pathLen:
                moveX, moveY = steerAng(get_Alist()[indx][0], get_Alist()[indx][1])
                print(get_Alist()[indx])
                print(indx, pathLen)
                move(moveX, moveY)
                try:
                    odomCal()
                except:
                    print("Hoopsie doopsie")

                set_globIndx(get_globIndx() + 1)
            else:
                set_running(False)

        def go2goal():
            if get_running():
                checkPath(get_globIndx(), 0)
                self.after(int(cityBlock() * mainRobot[3] * 1000), go2goal)

        # =================================
        # Pokus o D*Lite
        # =================================        
        def Dstar():
            # while not get_globDone():

            if not get_globDone():
                if len(get_Alist()) == 0:
                    set_Alist([mainGoal[0], mainGoal[1], 0], 0)
                    set_Alist([mainGoal[0], mainGoal[1], 0], 0)
                    addRobot(mainGoal[0] + 1, mainGoal[1] + 1, 4)
                else:
                    set_Alist(get_Alist()[-1], 0)

                checkAround(get_Alist()[-1])
                self.after(1, Dstar)
            else:
                set_startPath(get_Alist()[0])
                pickPack()
                # set_running(True)
                self.showMap(ax, canvas, fig)

                # if get_running():
                #     checkPath(get_globIndx(), 0)
                #     self.after(int(cityBlock() * mainRobot[3] * 100), Dstar)
                # else:
                #     self.after(1, Dstar)

            # elif get_running():
            #     checkPath(get_globIndx(), 0)
            #     self.after(int(cityBlock() * mainRobot[3] * 100), Dstar)
            # else:
            #     set_running(False)

        # =================================
        # Test
        # ================================= 
        def shouldImove():
            if get_running():
                set_running(False)
                status.config(text="I stopped on button click")
            else:
                set_running(True)
                go2goal()

        def clearMap():
            set_running(False)
            set_globDone(False)
            set_Alist(None, -1)
            set_oldList(-1)
            copyList()
            set_globIndx(0)
            for i in range(0, len(data)):
                for j in range(0, len(data[0])):
                    if data[i][j] == 4 or data[i][j] == '4' or data[i][j] == 5 or data[i][j] == '5':
                        data[i][j] = int(0)
            removeRobot(mainRobot[2])
            removeRobot(3)
            print(get_Alist())
            print(pathList)
            self.showMap(ax, canvas, fig)
            rclpy.spin_once(minimal_publisher)

        exit_button = Button(self, text="Exit", command=root.destroy)
        exit_button.place(relx=.85, rely=.95, height=40, width=100, anchor=CENTER)

        loadB = Button(self, text="Load map", font=MEDIUMFONT, command=select_file)
        loadB.place(relx=.5, rely=.15, height=40, width=150, anchor=CENTER)
        loadB.config(bg="green", fg="black")

        # goTogoalB = Button(self, text="Go 2 Goal", font=MEDIUMFONT, command = go2goal)
        goTogoalB = Button(self, text="Go 2 Goal", font=MEDIUMFONT, command=shouldImove)
        goTogoalB.place(relx=.57, rely=.3, height=40, width=200, anchor=W)
        goTogoalB.config(bg="cyan", fg="black")

        dStar = Button(self, text="D* Lite", font=MEDIUMFONT, command=Dstar)
        dStar.place(relx=.77, rely=.3, height=40, width=200, anchor=W)
        dStar.config(bg="magenta", fg="black")

        clearb = Button(self, text="Clear", font=MEDIUMFONT, command=clearMap)
        clearb.place(relx=.77, rely=.35, height=40, width=200, anchor=W)
        clearb.config(bg="white", fg="black")


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
