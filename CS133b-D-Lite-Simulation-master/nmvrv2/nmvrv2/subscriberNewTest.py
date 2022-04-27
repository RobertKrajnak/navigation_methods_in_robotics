from matplotlib import pyplot as plt
from matplotlib import colors
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import csv
import numpy as np
import pathlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import os
import urllib.request
import pandas as pd
import scipy.ndimage as ndi
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

data, imgStat, lastY, lastX, myDir, globFig, angle = [], 0, -2, -2, os.getcwd() + "/", [None, None, None, None], 0

def setGlobFig(ax, canvas, fig, robo):
    global globFig
    globFig[0] = ax
    globFig[1] = canvas
    globFig[2] = fig
    globFig[3] = robo

def getGlobFig():
    global globFig
    return globFig

def setXY(x, y):
    lastX = x
    lastY = y

def getXY():
    return lastX, lastY

def setAngle(a):
    global angle
    angle = a

def getAngle():
    return angle

def getImgStat():
    return imgStat

def setImgStat(stat):
    global imgStat
    imgStat = stat

def setData(inD):
    global data
    data = inD

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
                k = True
                # print(map[i][j])
                setAngle(map[i][j])
                break

            if k: break
        if k: break
    if k:
        return i, j
    else:
        return -1, -1

def saveImg():
    try:
        # url = "https://www.pngkey.com/png/full/964-9645727_preview-tank-top-down-sprite.png"
        # myurl = "https://m.media-amazon.com/images/I/31grDt8hrBS._SL500_.jpg"
        myurl = "http://1xtgzvl.257.cz/cache/d317f9c9/avefdb1ad8fbf8d8b72a2.png"
        urllib.request.urlretrieve(myurl, myDir + "robo.png")
                
        im = Image.open(myDir + "robo.png")
        imres = im.resize((500, 500), Image.ANTIALIAS)
        imres.save(myDir + "robo.png")
        setImgStat(1)
        print(getImgStat())
    except:
        print("Can not download img, continue without robo image.")
        setImgStat(0)

def rotateRobo(robImg):
    rotatedRobo = robImg
    if getAngle() == 20:
        rotatedRobo = ndi.rotate(robImg, 180)
    elif getAngle() == 21:
        rotatedRobo = ndi.rotate(robImg, 135)
    elif getAngle() == 22:
        rotatedRobo = ndi.rotate(robImg, 90)
    elif getAngle() == 23:
        rotatedRobo = ndi.rotate(robImg, 45)
    elif getAngle() == 25:
        rotatedRobo = ndi.rotate(robImg, -45)
    elif getAngle() == 26:
        rotatedRobo = ndi.rotate(robImg, -90)
    elif getAngle() == 27:
        rotatedRobo = ndi.rotate(robImg, -135)
    return rotatedRobo

LARGEFONT = ("Verdana", 35)
MEDIUMFONT = ("Verdana", 20)

class NMVR(tk.Frame):

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        saveImg()
        # loadMap()

        initMap =   [
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,1,0,1,0,1,0,0,1,0,0,1,0,1,1,1,0,0,0,1,],
                    [1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,0,0,1,],
                    [1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,0,0,1,],
                    [1,0,0,1,0,1,0,1,0,1,1,1,0,1,0,0,1,0,0,0,0,1,],
                    [1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,0,0,1,],
                    [1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,0,0,1,],
                    [1,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,1,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,1,0,1,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,1,0,1,1,0,1,0,1,0,0,1,0,0,0,0,0,0,0,1,],
                    [1,0,0,1,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,1,],
                    [1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,1,],
                    [1,0,0,1,0,1,0,0,1,0,0,1,1,0,0,1,0,1,0,1,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,]]           
        setData(initMap)

        fig, ax = plt.subplots(figsize=(8,8))

        i, j = place(data, 28)
        setXY(j, i)

        mycmap = colors.ListedColormap(['white', 'black', 'green', 'blue', 'gray','orange'])
        norm = colors.BoundaryNorm([0, .9, 2.9, 3.9, 4.9, 19.9, 28], mycmap.N)
        ax.pcolor(data[::-1], cmap=mycmap, norm=norm, edgecolors='k', linewidths=2)
        plt.gca().set_position([0, 0, 1, 1])
        robo = fig.add_axes([(j/len(data)) + 0.001, ((len(data) - i - 1) / len(data)) + 0.002, .04, .04], ANCHOR='C')
        canvas = FigureCanvasTkAgg(fig, master=root)

        if i != -1 and j != -1:
            robo.imshow(rotateRobo(plt.imread(myDir + 'robo.png')))
            robo.axis('off')

        canvas.draw()
        canvas.get_tk_widget().pack()
        # self.after(511, self.refresh_plot(ax, canvas, fig, robo)) 
        setGlobFig(ax, canvas, fig, robo)

    def refresh_plot(self):
        ax, canvas, fig, myrobo = getGlobFig()
        # loadMap()
        i, j = place(data, 28)

        mycmap = colors.ListedColormap(['white', 'black', 'green', 'blue', 'gray','orange'])
        norm = colors.BoundaryNorm([0, .9, 2.9, 3.9, 4.9, 19.9, 28], mycmap.N)
        ax.pcolor(data[::-1], cmap=mycmap, norm=norm, edgecolors='k', linewidths=2)
        plt.gca().set_position([0, 0, 1, 1])

        fig.delaxes(myrobo)
        myrobo = fig.add_axes([(j/len(data)) + 0.001, ((len(data) - i - 1) / len(data)) + 0.002, .04, .04], ANCHOR='C')
        robImg = rotateRobo(plt.imread(myDir + 'robo.png'))
        myrobo.imshow(robImg)
        myrobo.axis('off')

        canvas.draw()
        # self.after(511, self.refresh_plot(ax, canvas, fig, myrobo))
        setGlobFig(ax, canvas, fig, myrobo)

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(String, 'topic', self.listener_callback, 1)
        self.subscription

    def listener_callback(self, msg):
        setData(eval(msg.data))
        # self.get_logger().info('I see map')
        self.get_logger().info('I hear: "%s"' % msg.data)

root = tk.Tk()
root.title("Subscriber")

def quit_me():
    print("Close subscriber app")
    root.quit()
    root.destroy()

def main():
    rclpy.init(args=None)
    minimal_subscriber = MinimalSubscriber()
    

    view = NMVR(root)
    view.pack(side="top", fill="both", expand=True)
    root.geometry("800x800")
    root.protocol("MW_DELETE_WINDOW", quit_me)

    # rclpy.spin_once(minimal_subscriber)
    while True:
        view.refresh_plot()
        root.update()
        rclpy.spin_once(minimal_subscriber)
        view.refresh_plot()
        root.update()

if __name__=='__main__':
    main()
