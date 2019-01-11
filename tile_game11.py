# -*- coding: utf-8 -*-
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QPushButton,
                             QFrame, QLabel, QFrame, QGroupBox, QGridLayout,
                             QTableWidget, QTableWidgetItem)
import random
import numpy as np

import threading
import time

FILEPATH = os.path.dirname(__file__)
# print("FILEPATH: ", FILEPATH)
pic_path = os.path.join(FILEPATH, "pic")


class FormCreate(QWidget):
    def __init__(self):
        super(FormCreate, self).__init__()
        # self.floorstatus = np.zeros(64).reshape(8, 8) #0表示正常地板，1表示有洞地板，2表示堆有瓦砾的地板，3表示障碍物
        self.floorstatus = [[0] * 8 for i in range(8)]
        print("floorstatus:", self.floorstatus)
        self.initholenumber = 0
        self.inittilenumber = 0
        self.initobstaclenumber = 0
        self.robotx = 0
        self.roboty = 0
        self.hold = False
        self.direction = 1  # 表示机器人头所指向的方向，1表示向北，2表示向东，3表示向南，4表示向西
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.operate)  # 计时结束调用operate()方法
        self.timer.start(100)
        self.initUI()

    def showEvent(self, showEvent):
        # self.timer_control()
        self.timer.start()
        # print('run show')

    def operate(self):

        if self.initholenumber != 0 or self.inittilenumber != 0:
            # print("self.initholenumber,", self.initholenumber, self.inittilenumber)
            self.automatic_execute()
        else:
            
            print("-------------------")
            if self.timer.isActive():
                self.timer.stop()

    # def timer_control(self):
    # 	while self.initholenumber != 0 or self.inittilenumber != 0:
    #         print('run automatic')
    #         self.automatic_execute()
    #         break

    def initUI(self):
        self.font = QFont()
        self.font.setPixelSize(13)

        self.leftframe = QFrame(self)
        self.leftframe.setGeometry(0, 0, 360, 400)
        self.rightframe = QFrame(self)
        self.rightframe.setGeometry(360, 0, 190, 400)

        self.leftui()
        self.rightui()

        self.setGeometry(300, 300, 550, 400)
        self.setWindowTitle('瓦片世界')
        self.show()

    def leftui(self):
        self.label_west = QLabel("西", self)
        self.label_west.move(20, 180)
        self.label_west.setFont(self.font)

        self.label_east = QLabel("东", self)
        self.label_east.move(320, 180)
        self.label_east.setFont(self.font)

        self.label_west = QLabel("北", self)
        self.label_west.move(165, 30)
        self.label_west.setFont(self.font)

        self.label_west = QLabel("南", self)
        self.label_west.move(165, 350)
        self.label_west.setFont(self.font)

        self.tablebox = QFrame(self.leftframe)
        self.tablebox.setGeometry(50, 60, 260, 260)
        self.initable()  # 初始化表格
        self.addItem()  # 初始化地板

        while self.initholenumber < 3:
            self.holeinit()  # 初始化三个洞穴

        while self.inittilenumber < 3:
            self.tileinit()  # 初始化三个瓦砾

        while self.initobstaclenumber < 6:
            self.obstacleinit()  # 初始化六个障碍物

        self.robotinit()  # 初始化机器人的方向，位置，状态

    def initable(self):
        self.table = QTableWidget(self.tablebox)
        self.table.setGeometry(5, 5, 250, 250)
        self.table.setRowCount(8)
        self.table.setColumnCount(8)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        # 设置列宽
        i = 0
        while i < self.table.columnCount():
            self.table.setColumnWidth(i, 31)
            i += 1
        # 设置行高
        j = 0
        while j < self.table.rowCount():
            self.table.setRowHeight(j, 31)
            j += 1
        vh = self.table.verticalHeader()
        vh.hide()
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

    def holeinit(self):
        i = random.randint(0, 7)  # 包含0和7
        j = random.randint(0, 7)
        if (i == 0) and (j == 0):
            if (self.floorstatus[i + 1][j] == 0) and (
                    self.floorstatus[i][j + 1] == 0) and (self.floorstatus[
                        i + 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 1

        elif (i == 7) and (j == 0):
            if (self.floorstatus[i - 1][j] == 0) and (
                    self.floorstatus[i][j + 1] == 0) and (self.floorstatus[
                        i - 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 1

        elif (i == 0) and (j == 7):
            if (self.floorstatus[i + 1][j] == 0) and (
                    self.floorstatus[i][j - 1] == 0) and (self.floorstatus[
                        i + 1][j - 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 1

        elif (i == 7) and (j == 7):
            if (self.floorstatus[i - 1][j] == 0) and (
                    self.floorstatus[i][j - 1] == 0) and (self.floorstatus[
                        i - 1][j - 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 1

        elif (i == 0) and (j > 0) and (j < 7):
            if (self.floorstatus[i][j - 1] == 0) and (
                    self.floorstatus[i][j + 1] == 0
            ) and (self.floorstatus[i + 1][j - 1] == 0) and (
                    self.floorstatus[i + 1][j] == 0) and (self.floorstatus[
                        i + 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 1

        elif (j == 0) and (i > 0) and (i < 7):
            if (self.floorstatus[i - 1][j] == 0) and (
                    self.floorstatus[i + 1][j] == 0
            ) and (self.floorstatus[i - 1][j + 1] == 0) and (
                    self.floorstatus[i][j + 1] == 0) and (self.floorstatus[
                        i + 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 1

        elif (i == 7) and (j > 0) and (j < 7):
            if (self.floorstatus[i][j - 1] == 0) and (self.floorstatus[i - 1][
                    j + 1] == 0) and (self.floorstatus[i - 1][j] == 0) and (
                        self.floorstatus[i - 1][j - 1] == 0) and (
                            self.floorstatus[i][j + 1] == 0) and (
                                self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 1

        elif (j == 7) and (i > 0) and (i < 7):
            if (self.floorstatus[i - 1][j - 1] == 0
                ) and (self.floorstatus[i][j - 1] == 0) and (
                    self.floorstatus[i + 1][j - 1] == 0) and (
                        self.floorstatus[i + 1][j] == 0) and (self.floorstatus[
                            i - 1][j] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 1

        else:
            if (self.floorstatus[i - 1][j - 1] == 0) and (
                    self.floorstatus[i - 1][j] == 0
            ) and (self.floorstatus[i - 1][j + 1] == 0) and (
                    self.floorstatus[i][j - 1] == 0) and (
                        self.floorstatus[i][j + 1] == 0) and (
                            self.floorstatus[i + 1][j - 1] == 0) and (
                                self.floorstatus[i + 1][j] == 0) and (
                                    self.floorstatus[i + 1][j + 1] == 0) and (
                                        self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 1

        if self.floorstatus[i][j] == 1:
            photoname = "hole.bmp"
            self.modify(i, j, photoname)
            self.initholenumber = self.initholenumber + 1

    def tileinit(self):
        # print("init tile: ", self.floorstatus)
        i = random.randint(0, 7)
        j = random.randint(0, 7)
        if (i == 0) and (j == 0):
            if (self.floorstatus[i + 1][j] == 0) and (
                    self.floorstatus[i][j + 1] == 0) and (self.floorstatus[
                        i + 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 2

        elif (i == 7) and (j == 0):
            if (self.floorstatus[i - 1][j] == 0) and (
                    self.floorstatus[i][j + 1] == 0) and (self.floorstatus[
                        i - 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 2

        elif (i == 0) and (j == 7):
            if (self.floorstatus[i + 1][j] == 0) and (
                    self.floorstatus[i][j - 1] == 0) and (self.floorstatus[
                        i + 1][j - 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 2

        elif (i == 7) and (j == 7):
            if (self.floorstatus[i - 1][j] == 0) and (
                    self.floorstatus[i][j - 1] == 0) and (self.floorstatus[
                        i - 1][j - 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 2

        elif (i == 0) and (j > 0) and (j < 7):
            if (self.floorstatus[i][j - 1] == 0) and (
                    self.floorstatus[i][j + 1] == 0
            ) and (self.floorstatus[i + 1][j - 1] == 0) and (
                    self.floorstatus[i + 1][j] == 0) and (self.floorstatus[
                        i + 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 2

        elif (j == 0) and (i > 0) and (i < 7):
            if (self.floorstatus[i - 1][j] == 0) and (
                    self.floorstatus[i + 1][j] == 0
            ) and (self.floorstatus[i - 1][j + 1] == 0) and (
                    self.floorstatus[i][j + 1] == 0) and (self.floorstatus[
                        i + 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 2

        elif (i == 7) and (j > 0) and (j < 7):
            if (self.floorstatus[i][j - 1] == 0) and (self.floorstatus[i - 1][
                    j + 1] == 0) and (self.floorstatus[i - 1][j] == 0) and (
                        self.floorstatus[i - 1][j - 1] == 0) and (
                            self.floorstatus[i][j + 1] == 0) and (
                                self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 2

        elif (j == 7) and (i > 0) and (i < 7):
            if (self.floorstatus[i - 1][j - 1] == 0
                ) and (self.floorstatus[i][j - 1] == 0) and (
                    self.floorstatus[i + 1][j - 1] == 0) and (
                        self.floorstatus[i + 1][j] == 0) and (self.floorstatus[
                            i - 1][j] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 2

        else:
            if (self.floorstatus[i - 1][j - 1] == 0) and (
                    self.floorstatus[i - 1][j] == 0
            ) and (self.floorstatus[i - 1][j + 1] == 0) and (
                    self.floorstatus[i][j - 1] == 0) and (
                        self.floorstatus[i][j + 1] == 0) and (
                            self.floorstatus[i + 1][j - 1] == 0) and (
                                self.floorstatus[i + 1][j] == 0) and (
                                    self.floorstatus[i + 1][j + 1] == 0) and (
                                        self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 2

        if self.floorstatus[i][j] == 2:
            photoname = "tile.bmp"
            self.modify(i, j, photoname)
            self.inittilenumber = self.inittilenumber + 1

    def obstacleinit(self):
        i = random.randint(0, 7)
        j = random.randint(0, 7)
        if (i == 0) and (j == 0):
            if (self.floorstatus[i + 1][j] == 0) and (
                    self.floorstatus[i][j + 1] == 0) and (self.floorstatus[
                        i + 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 3

        elif (i == 7) and (j == 0):
            if (self.floorstatus[i - 1][j] == 0) and (
                    self.floorstatus[i][j + 1] == 0) and (self.floorstatus[
                        i - 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 3

        elif (i == 0) and (j == 7):
            if (self.floorstatus[i + 1][j] == 0) and (
                    self.floorstatus[i][j - 1] == 0) and (self.floorstatus[
                        i + 1][j - 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 3

        elif (i == 7) and (j == 7):
            if (self.floorstatus[i - 1][j] == 0) and (
                    self.floorstatus[i][j - 1] == 0) and (self.floorstatus[
                        i - 1][j - 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 3

        elif (i == 0) and (j > 0) and (j < 7):
            if (self.floorstatus[i][j - 1] == 0) and (
                    self.floorstatus[i][j + 1] == 0
            ) and (self.floorstatus[i + 1][j - 1] == 0) and (
                    self.floorstatus[i + 1][j] == 0) and (self.floorstatus[
                        i + 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 3

        elif (j == 0) and (i > 0) and (i < 7):
            if (self.floorstatus[i - 1][j] == 0) and (
                    self.floorstatus[i + 1][j] == 0
            ) and (self.floorstatus[i - 1][j + 1] == 0) and (
                    self.floorstatus[i][j + 1] == 0) and (self.floorstatus[
                        i + 1][j + 1] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 3

        elif (i == 7) and (j > 0) and (j < 7):
            if (self.floorstatus[i][j - 1] == 0) and (self.floorstatus[i - 1][
                    j + 1] == 0) and (self.floorstatus[i - 1][j] == 0) and (
                        self.floorstatus[i - 1][j - 1] == 0) and (
                            self.floorstatus[i][j + 1] == 0) and (
                                self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 3

        elif (j == 7) and (i > 0) and (i < 7):
            if (self.floorstatus[i - 1][j - 1] == 0
                ) and (self.floorstatus[i][j - 1] == 0) and (
                    self.floorstatus[i + 1][j - 1] == 0) and (
                        self.floorstatus[i + 1][j] == 0) and (self.floorstatus[
                            i - 1][j] == 0) and (self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 3

        else:
            if (self.floorstatus[i - 1][j - 1] == 0) and (
                    self.floorstatus[i - 1][j] == 0
            ) and (self.floorstatus[i - 1][j + 1] == 0) and (
                    self.floorstatus[i][j - 1] == 0) and (
                        self.floorstatus[i][j + 1] == 0) and (
                            self.floorstatus[i + 1][j - 1] == 0) and (
                                self.floorstatus[i + 1][j] == 0) and (
                                    self.floorstatus[i + 1][j + 1] == 0) and (
                                        self.floorstatus[i][j] == 0):
                self.floorstatus[i][j] = 3

        if self.floorstatus[i][j] == 3:
            photoname = "obstacle.bmp"
            self.modify(i, j, photoname)
            self.initobstaclenumber = self.initobstaclenumber + 1

    def modify(self, i, j, photoname):
        self.floor = QLabel(self.tablebox)
        self.floor.resize(31, 31)
        floor_bmp_path = os.path.join(pic_path, photoname)
        img = QPixmap(floor_bmp_path)
        self.floor.setPixmap(img)
        self.table.setCellWidget(i, j, self.floor)

    def robotinit(self):
        while self.floorstatus[self.robotx][self.roboty] != 0:
            self.robotx = random.randint(0, 7)
            self.roboty = random.randint(0, 7)
        photoname = "rbnorth.bmp"
        print("robotinit----self.robotx, self.roboty: ", self.robotx,
              self.roboty)
        self.modify(self.robotx, self.roboty, photoname)
        self.direction = 1
        self.hold = False

    def addItem(self):
        i = 0
        j = 0
        for i in range(8):
            for j in range(8):
                self.left_Ifloor = QLabel(self.tablebox)
                self.left_Ifloor.resize(31, 31)
                photoname = "floor.bmp"
                Ifloor_bmp_path = os.path.join(pic_path, photoname)
                img = QPixmap(Ifloor_bmp_path)
                self.left_Ifloor.setPixmap(img)
                self.table.setCellWidget(i, j, self.left_Ifloor)
                self.floorstatus[i][j] = 0
                j = j + 1
        print("after init floorstatus:", self.floorstatus)

    def rightui(self):
        self.groupbox = QGroupBox("description", self.rightframe)
        self.groupbox.setGeometry(2, 5, 185, 395)

        self.Ifloor = QLabel(self.groupbox)
        self.Ifloor.resize(31, 31)
        self.Ifloor.move(30, 15)
        photoname = "floor.bmp"
        Ifloor_bmp_path = os.path.join(pic_path, photoname)
        img = QPixmap(Ifloor_bmp_path)
        self.Ifloor.setPixmap(img)
        self.label1 = QLabel('正常的地板', self.groupbox)
        self.label1.move(10, 55)
        self.label1.setFont(self.font)

        self.Ihole = QLabel(self.groupbox)
        self.Ihole.resize(31, 31)
        self.Ihole.move(120, 15)
        photoname = "hole.bmp"
        Ihole_bmp_path = os.path.join(pic_path, photoname)
        img = QPixmap(Ihole_bmp_path)
        self.Ihole.setPixmap(img)
        self.label2 = QLabel('有洞的地板', self.groupbox)
        self.label2.move(100, 55)
        self.label2.setFont(self.font)

        self.Iobstacle = QLabel(self.groupbox)
        self.Iobstacle.resize(31, 31)
        self.Iobstacle.move(30, 80)
        photoname = "obstacle.bmp"
        Iobstacle_bmp_path = os.path.join(pic_path, photoname)
        img = QPixmap(Iobstacle_bmp_path)
        self.Iobstacle.setPixmap(img)
        self.label3 = QLabel('障碍物', self.groupbox)
        self.label3.move(23, 120)
        self.label3.setFont(self.font)

        self.Ltile = QLabel(self.groupbox)
        self.Ltile.resize(31, 31)
        self.Ltile.move(120, 80)
        photoname = "tile.bmp"
        Ltile_bmp_path = os.path.join(pic_path, photoname)
        img = QPixmap(Ltile_bmp_path)
        self.Ltile.setPixmap(img)
        self.label4 = QLabel('瓦砾', self.groupbox)
        self.label4.move(120, 120)
        self.label4.setFont(self.font)

        self.Irnorth = QLabel(self.groupbox)
        self.Irnorth.resize(31, 31)
        self.Irnorth.move(30, 145)
        photoname = "rbnorth.bmp"
        Irnorth_bmp_path = os.path.join(pic_path, photoname)
        img = QPixmap(Irnorth_bmp_path)
        self.Irnorth.setPixmap(img)
        self.label5 = QLabel('机器人头朝北', self.groupbox)
        self.label5.move(3, 185)
        self.label5.setFont(self.font)

        self.Ireast = QLabel(self.groupbox)
        self.Ireast.resize(31, 31)
        self.Ireast.move(120, 145)
        photoname = "rbeast.bmp"
        Ireast_bmp_path = os.path.join(pic_path, photoname)
        img = QPixmap(Ireast_bmp_path)
        self.Ireast.setPixmap(img)
        self.label6 = QLabel('机器人头朝东', self.groupbox)
        self.label6.move(93, 185)
        self.label6.setFont(self.font)

        self.Irwest = QLabel(self.groupbox)
        self.Irwest.resize(31, 31)
        self.Irwest.move(30, 210)
        photoname = "rbwest.bmp"
        Irwest_bmp_path = os.path.join(pic_path, photoname)
        img = QPixmap(Irwest_bmp_path)
        self.Irwest.setPixmap(img)
        self.label7 = QLabel('机器人头朝西', self.groupbox)
        self.label7.move(3, 250)
        self.label7.setFont(self.font)

        self.Irsouth = QLabel(self.groupbox)
        self.Irsouth.resize(31, 31)
        self.Irsouth.move(120, 210)
        photoname = "rbsouth.bmp"
        Irsouth_bmp_path = os.path.join(pic_path, photoname)
        img = QPixmap(Irsouth_bmp_path)
        self.Irsouth.setPixmap(img)
        self.label7 = QLabel('机器人头朝南', self.groupbox)
        self.label7.move(93, 250)
        self.label7.setFont(self.font)

        self.button1 = QPushButton("turnlefttest", self.groupbox)
        self.button1.move(5, 280)
        self.button1.clicked.connect(self.turnleft)

        self.button2 = QPushButton("sucktest", self.groupbox)
        self.button2.move(100, 280)
        self.button2.clicked.connect(self.suck)

        self.button3 = QPushButton("turnrighttest", self.groupbox)
        self.button3.move(5, 320)
        self.button3.clicked.connect(self.turnright)

        self.button4 = QPushButton("releasetest", self.groupbox)
        self.button4.move(100, 320)
        self.button4.clicked.connect(self.release)

        self.button5 = QPushButton("movetest", self.groupbox)
        self.button5.move(5, 360)
        self.button5.clicked.connect(self.move)

        self.button6 = QPushButton("test", self.groupbox)
        self.button6.move(100, 360)
        # self.button1.clicked.connect(self.turnleft)

    def turnleft(self):
        self.direction = (self.direction + 2) % 4 + 1
        if self.direction == 1:
            photoname = "rbnorth.bmp"
            self.modify(self.robotx, self.roboty, photoname)
        elif self.direction == 2:
            photoname = "rbeast.bmp"
            self.modify(self.robotx, self.roboty, photoname)
        elif self.direction == 3:
            photoname = "rbsouth.bmp"
            self.modify(self.robotx, self.roboty, photoname)
        elif self.direction == 4:
            photoname = "rbwest.bmp"
            self.modify(self.robotx, self.roboty, photoname)
        else:
            pass

    def turnright(self):
        self.direction = self.direction % 4 + 1
        if self.direction == 1:
            photoname = "rbnorth.bmp"
        elif self.direction == 2:
            photoname = "rbeast.bmp"
        elif self.direction == 3:
            photoname = "rbsouth.bmp"
        elif self.direction == 4:
            photoname = "rbwest.bmp"
        else:
            pass
        self.modify(self.robotx, self.roboty, photoname)

    def change(self):
        if self.floorstatus[self.robotx][self.roboty] == 0:
            photoname = "floor.bmp"
            self.modify(self.robotx, self.roboty, photoname)
        elif self.floorstatus[self.robotx][self.roboty] == 1:
            photoname = "hole.bmp"
            self.modify(self.robotx, self.roboty, photoname)
        elif self.floorstatus[self.robotx][self.roboty] == 2:
            photoname = "tile.bmp"
            self.modify(self.robotx, self.roboty, photoname)
        else:
            pass

    def move(self):
        if (self.direction == 1) and (self.roboty > 0) and (
                self.floorstatus[self.robotx][self.roboty - 1] != 3):
            self.change()
            self.robotx -= 1
            photoname = "rbnorth.bmp"
            self.modify(self.robotx, self.roboty, photoname)

        elif (self.direction == 2) and (self.roboty < 7) and (
                self.floorstatus[self.robotx][self.roboty + 1] != 3):
            self.change()
            self.roboty += 1
            photoname = "rbeast.bmp"
            self.modify(self.robotx, self.roboty, photoname)

        elif (self.direction == 3) and (self.robotx < 7) and (
                self.floorstatus[self.robotx + 1][self.roboty] != 3):
            self.change()
            self.robotx += 1
            photoname = "rbsouth.bmp"
            self.modify(self.robotx, self.roboty, photoname)

        elif (self.direction == 4) and (self.roboty > 0) and (
                self.floorstatus[self.robotx][self.roboty - 1] != 3):
            self.change()
            self.roboty -= 1
            photoname = "rbwest.bmp"
            self.modify(self.robotx, self.roboty, photoname)

        else:
            print('pass')
            pass

    def suck(self):
        if (self.hold == False) and (
                self.floorstatus[self.robotx][self.roboty] == 2):
            print("im a tile")
            self.floorstatus[self.robotx][self.roboty] = 0
            self.hold = True
            self.inittilenumber -= 1

    def release(self):
        if (self.hold == True) and (
                self.floorstatus[self.robotx][self.roboty] == 1):
            print("im a hole")
            self.floorstatus[self.robotx][self.roboty] = 0
            self.hold = False
            self.initholenumber -= 1

    def automatic_execute(self):
        if (self.floorstatus[self.robotx][self.roboty] == 2):
            self.suck()
        elif (self.floorstatus[self.robotx][self.roboty] == 1):
            self.release()
        elif (self.robotx > 0) and (self.direction == 1) and (
                self.floorstatus[self.robotx - 1][self.roboty] == 2
                or self.floorstatus[self.robotx - 1][self.roboty] == 1):
            print("move")
            self.move()
        elif (self.roboty < 7) and (self.direction == 2) and (
                self.floorstatus[self.robotx][self.roboty + 1] == 2
                or self.floorstatus[self.robotx][self.roboty + 1] == 1):
            print("move")
            self.move()
        elif (self.robotx < 7) and (self.direction == 3) and (
                self.floorstatus[self.robotx + 1][self.roboty] == 2
                or self.floorstatus[self.robotx + 1][self.roboty] == 1):
            print("move")
            self.move()
        elif (self.roboty > 0) and (self.direction == 4) and (
                self.floorstatus[self.robotx][self.roboty - 1] == 2
                or self.floorstatus[self.robotx][self.roboty - 1] == 1):
            print("move")
            self.move()
        elif (self.roboty < 7) and (self.direction == 1) and (
                self.floorstatus[self.robotx][self.roboty + 1] == 2
                or self.floorstatus[self.robotx][self.roboty + 1] == 1):
            print("turnright")
            self.turnright()
        elif (self.roboty > 0) and (self.direction == 1) and (
                self.floorstatus[self.robotx][self.roboty - 1] == 2
                or self.floorstatus[self.robotx][self.roboty - 1] == 1):
            print("turnleft")
            self.turnleft()
        elif (self.robotx < 7) and (self.direction == 2) and (
                self.floorstatus[self.robotx + 1][self.roboty] == 2
                or self.floorstatus[self.robotx + 1][self.roboty] == 1):
            print("turnright")
            self.turnright()
        elif (self.robotx > 0) and (self.direction == 2) and (
                self.floorstatus[self.robotx - 1][self.roboty] == 2
                or self.floorstatus[self.robotx - 1][self.roboty] == 1):
            print("turnleft")
            self.turnleft()
        elif (self.roboty > 0) and (self.direction == 3) and (
                self.floorstatus[self.robotx][self.roboty - 1] == 2
                or self.floorstatus[self.robotx][self.roboty - 1] == 1):
            print("turnright")
            self.turnright()
        elif (self.roboty < 7) and (self.direction == 3) and (
                self.floorstatus[self.robotx][self.roboty + 1] == 2
                or self.floorstatus[self.robotx][self.roboty + 1] == 1):
            print("turnleft")
            self.turnleft()
        elif (self.robotx > 0) and (self.direction == 4) and (
                self.floorstatus[self.robotx - 1][self.roboty] == 2
                or self.floorstatus[self.robotx - 1][self.roboty] == 1):
            print("turnright")
            self.turnright()
        elif (self.robotx < 7) and (self.direction == 4) and (
                self.floorstatus[self.robotx + 1][self.roboty] == 2
                or self.floorstatus[self.robotx + 1][self.roboty] == 1):
            print("turnleft")
            self.turnleft()
        elif (self.robotx < 7) and (self.direction == 1) and (
                self.floorstatus[self.robotx + 1][self.roboty] == 2
                or self.floorstatus[self.robotx + 1][self.roboty] == 1):
            print("turnright")
            self.turnright()
        elif (self.roboty > 0) and (self.direction == 2) and (
                self.floorstatus[self.robotx][self.roboty - 1] == 2
                or self.floorstatus[self.robotx][self.roboty - 1] == 1):
            self.turnright()
            print("turnright")
        elif (self.robotx > 0) and (self.direction == 3) and (
                self.floorstatus[self.robotx - 1][self.roboty] == 2
                or self.floorstatus[self.robotx - 1][self.roboty] == 1):
            self.turnright()
            print("turnright")
        elif (self.roboty < 7) and (self.direction == 4) and (
                self.floorstatus[self.robotx][self.roboty + 1] == 2
                or self.floorstatus[self.robotx][self.roboty + 1] == 1):
            self.turnright()
            print("turnright")
        elif (self.roboty <
              7) and (self.robotx > 0) and (self.direction == 1) and (
                  self.floorstatus[self.robotx - 1][self.roboty + 1] == 2
                  or self.floorstatus[self.robotx - 1][self.roboty + 1] == 1):
            self.move()
            print("move")
        elif (self.roboty <
              7) and (self.robotx < 7) and (self.direction == 2) and (
                  self.floorstatus[self.robotx + 1][self.roboty + 1] == 2
                  or self.floorstatus[self.robotx + 1][self.roboty + 1] == 1):
            self.move()
            print("move")
        elif (self.roboty >
              0) and (self.robotx < 7) and (self.direction == 3) and (
                  self.floorstatus[self.robotx + 1][self.roboty - 1] == 2
                  or self.floorstatus[self.robotx + 1][self.roboty - 1] == 1):
            self.move()
            print("move")
        elif (self.roboty >
              0) and (self.robotx > 0) and (self.direction == 4) and (
                  self.floorstatus[self.robotx - 1][self.roboty - 1] == 2
                  or self.floorstatus[self.robotx - 1][self.roboty - 1] == 1):
            self.move()
            print("move")
        elif (self.roboty >
              0) and (self.robotx > 0) and (self.direction == 1) and (
                  self.floorstatus[self.robotx - 1][self.roboty - 1] == 2
                  or self.floorstatus[self.robotx - 1][self.roboty - 1] == 1):
            self.move()
            print("move")
        elif (self.roboty <
              7) and (self.robotx > 0) and (self.direction == 2) and (
                  self.floorstatus[self.robotx - 1][self.roboty + 1] == 2
                  or self.floorstatus[self.robotx - 1][self.roboty + 1] == 1):
            self.move()
            print("move")
        elif (self.roboty <
              7) and (self.robotx < 7) and (self.direction == 3) and (
                  self.floorstatus[self.robotx + 1][self.roboty + 1] == 2
                  or self.floorstatus[self.robotx + 1][self.roboty + 1] == 1):
            self.move()
            print("move")
        elif (self.roboty >
              0) and (self.robotx < 7) and (self.direction == 4) and (
                  self.floorstatus[self.robotx + 1][self.roboty - 1] == 2
                  or self.floorstatus[self.robotx + 1][self.roboty - 1] == 1):
            self.move()
            print("move")
        elif (self.roboty <
              7) and (self.robotx < 7) and (self.direction == 1) and (
                  self.floorstatus[self.robotx + 1][self.roboty + 1] == 2
                  or self.floorstatus[self.robotx + 1][self.roboty + 1] == 1):
            self.turnright()
        elif (self.roboty >
              0) and (self.robotx < 7) and (self.direction == 1) and (
                  self.floorstatus[self.robotx + 1][self.roboty - 1] == 2
                  or self.floorstatus[self.robotx + 1][self.roboty - 1] == 1):
            self.turnleft()
        elif (self.roboty >
              0) and (self.robotx < 7) and (self.direction == 2) and (
                  self.floorstatus[self.robotx + 1][self.roboty - 1] == 2
                  or self.floorstatus[self.robotx + 1][self.roboty - 1] == 1):
            self.turnright()
        elif (self.roboty >
              0) and (self.robotx > 0) and (self.direction == 2) and (
                  self.floorstatus[self.robotx - 1][self.roboty - 1] == 2
                  or self.floorstatus[self.robotx - 1][self.roboty - 1] == 1):
            self.turnleft()
        elif (self.roboty >
              0) and (self.robotx > 0) and (self.direction == 3) and (
                  self.floorstatus[self.robotx - 1][self.roboty - 1] == 2
                  or self.floorstatus[self.robotx - 1][self.roboty - 1] == 1):
            self.turnright()
        elif (self.roboty <
              7) and (self.robotx > 0) and (self.direction == 3) and (
                  self.floorstatus[self.robotx - 1][self.roboty + 1] == 2
                  or self.floorstatus[self.robotx - 1][self.roboty + 1] == 1):
            self.turnleft()
        elif (self.roboty <
              7) and (self.robotx > 0) and (self.direction == 4) and (
                  self.floorstatus[self.robotx - 1][self.roboty + 1] == 2
                  or self.floorstatus[self.robotx - 1][self.roboty + 1] == 2):
            self.turnright()
        elif (self.roboty <
              7) and (self.robotx < 7) and (self.direction == 4) and (
                  self.floorstatus[self.robotx + 1][self.roboty + 1] == 2
                  or self.floorstatus[self.robotx + 1][self.roboty + 1] == 2):
            self.turnleft()
        else:
            if random.randint(0, 2) == 0:
                self.move()
            else:
                self.turnright()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = FormCreate()
    ex.show()

    sys.exit(app.exec_())
