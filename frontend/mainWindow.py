# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from functools import partial
import numpy
import detect as Detect


class Ui_Dialog(object):
    def __init__(self):
        self.coordinates = []
        self.color_buttons = []
        self.color_boxes = []
        self.color_types = []
        self.color_map = []
        self.images = [[], [], [], []]
        self.type = 0
        self.color = 0
        self.lines = []

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.Dialog = Dialog
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(70, 240, 81, 20))
        self.pushButton_2.setStyleSheet("background-color : rgb(255, 0, 0);\n"
                                        "border-radius: 10px;")
        self.pushButton_2.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(250, 240, 81, 20))
        self.pushButton_3.setStyleSheet("background-color: rgb(103, 101, 104);\n"
                                        "border-radius: 10px;")
        self.pushButton_3.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 60, 221, 41))
        self.label.setStyleSheet("font: 36pt \"Hannotate SC\";")
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.pushButton_3.clicked.connect(self.pick_image)
        self.pushButton_2.pressed.connect(lambda: self.button_press(0))
        self.pushButton_3.pressed.connect(lambda: self.button_press(1))
        self.pushButton_2.released.connect(lambda: self.button_release(0))
        self.pushButton_3.released.connect(lambda: self.button_release(1))
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_2.setText(_translate("Dialog", "退出"))
        self.pushButton_3.setText(_translate("Dialog", "选择图片"))
        self.label.setText(_translate("Dialog", "瓶盖形态检测"))

    def pick_image(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        print(filename[0])
        if filename[0] != '':
            image = cv2.imread(filename[0])
            # image = cv2.resize(image, (1000, 1000))

            box_list, color_list, image_list, class_list, marked_image = Detect.detect(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            """box_list = numpy.array([[[30, 30], [60, 30], [60, 60], [30, 60]],
                                    [[100, 100], [150, 100], [150, 150], [100, 150]],
                                    [[80, 80], [90, 80], [90, 90], [80, 90]]])
            color_list = numpy.array([[250, 25, 25], [120, 20, 120], [250, 25, 25]])
            type_list = numpy.array([0, 1, 2])
            """
            self.display(image, box_list, color_list, class_list)

            """
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            image_result = Image.fromarray(image)
            image_result.show()
            """

    def display_init(self):
        self.result_window = QtWidgets.QWidget()
        self.result_window.paintEvent = self.paintEvent1
        self.result_window.setGeometry(100, 100, 850, 720)
        self.result_window.setWindowTitle("Result")
        self.picture = QtWidgets.QLabel(self.result_window)
        self.super_paintEvent = self.picture.paintEvent
        self.picture.paintEvent = self.paintEvent2

        self.button_front = QtWidgets.QPushButton(self.result_window)
        self.button_front.setGeometry(QtCore.QRect(600, 10, 50, 30))
        self.button_front.setText("正面")
        self.button_front.clicked.connect(lambda: self.change_type(0))
        self.button_back = QtWidgets.QPushButton(self.result_window)
        self.button_back.setGeometry(QtCore.QRect(650, 10, 50, 30))
        self.button_back.setText("背面")
        self.button_back.clicked.connect(lambda: self.change_type(1))
        self.button_side = QtWidgets.QPushButton(self.result_window)
        self.button_side.setGeometry(QtCore.QRect(700, 10, 50, 30))
        self.button_side.setText("侧面")
        self.button_side.clicked.connect(lambda: self.change_type(2))
        self.button_none = QtWidgets.QPushButton(self.result_window)
        self.button_none.setGeometry(QtCore.QRect(750, 10, 100, 30))
        self.button_none.setText("不是瓶盖")
        self.button_none.clicked.connect(lambda: self.change_type(3))
        self.button_front.setEnabled(False)

        self.label_none = QtWidgets.QLabel(self.result_window)
        self.label_none.setGeometry(QtCore.QRect(650, 30, 160, 40))
        self.label_none.setText("没有此种类型")

        self.coordinates = []
        self.color_buttons = []
        self.color_boxes = []
        self.color_types = []
        self.color_map = []
        self.images = [[], [], [], []]
        self.type = 0
        self.color = 0

    def display(self, img, box_list, color_list, type_list):
        self.display_init()
        self.img = img
        w = self.img.shape[1]
        h = self.img.shape[0]

        for i, color in enumerate(color_list):
            result = self.exist_color(color, self.color_map)
            if result >= 0:
                self.color_boxes[result].append(box_list[i])
                self.color_types[result].append(type_list[i])
            else:
                self.color_boxes.append([box_list[i]])
                self.color_types.append([type_list[i]])
                self.color_map.append(color)
        self.color_boxes.append(box_list)
        self.color_types.append(type_list)

        self.color_buttons = []
        for i, color in enumerate(self.color_map):
            self.color_buttons.append(QtWidgets.QPushButton(self.result_window))
            self.color_buttons[i].setGeometry(QtCore.QRect(50 + 50 * i, 10, 20, 20))
            if i == 0:
                self.color_buttons[i].setStyleSheet(
                    "background-color:rgb(" + str(self.color_map[i][0]) + ", " + str(self.color_map[i][1]) + ", "
                    + str(self.color_map[i][2]) + ");\nborder-radius: 10px;\n\
                                                                        border-color: #800000;\n\
                                                                        border-width: 1px;\n\
                                                                        border-style: solid;")
            else:
                self.color_buttons[i].setStyleSheet("background-color:rgb(" + str(color[0]) + ", " + str(color[1]) + ", "
                                                + str(color[2]) + ");\nborder-radius: 10px;")
            self.color_buttons[i].setIconSize(QtCore.QSize(15, 15))
            self.color_buttons[i].clicked.connect(partial(self.change_color, i))
            for j in range(0, 4):
                img_copy = self.img.copy()

                img_copy = img_copy * 0.2
                img_copy = img_copy.astype(numpy.uint8)

                for index, box in enumerate(self.color_boxes[i]):
                    if self.color_types[i][index] != j:
                        continue
                    x1, x2, y1, y2=self.find_corner(box)
                    img_copy[y1:y2, x1:x2] = self.img[y1:y2, x1:x2]

                # for xi in range(0, w):
                #     for xj in range(0, h):
                #         if not self.inside(i, xi, xj, j):
                #             img_copy[xj, xi, 0] = int(self.img[xj, xi, 0] * 0.2)
                #             img_copy[xj, xi, 1] = int(self.img[xj, xi, 1] * 0.2)
                #             img_copy[xj, xi, 2] = int(self.img[xj, xi, 2] * 0.2)
                img_copy = cv2.resize(img_copy, (500, 500))
                # image_result = Image.fromarray(img_copy)
                # image_result.show()
                self.images[j].append(img_copy)
        self.color_buttons.append(QtWidgets.QPushButton(self.result_window))
        self.color_buttons[len(self.color_buttons)-1].setText("所有颜色")
        self.color_buttons[len(self.color_buttons)-1].setGeometry(QtCore.QRect(50 + 50 * (len(self.color_buttons)-1), 10, 100, 30))
        self.color_buttons[len(self.color_buttons)-1].clicked.connect(partial(self.change_color, len(self.color_buttons)-1))

        for j in range(0, 4):
            img_copy = self.img.copy()
            img_copy = img_copy * 0.2
            img_copy = img_copy.astype(numpy.uint8)

            for index, box in enumerate(self.color_boxes[len(self.color_buttons)-1]):
                if self.color_types[len(self.color_buttons)-1][index] != j:
                    continue
                x1, x2, y1, y2 = self.find_corner(box)
                img_copy[y1:y2, x1:x2] = self.img[y1:y2, x1:x2]
            img_copy = cv2.resize(img_copy, (500, 500))
            self.images[j].append(img_copy)

        self.draw_image(self.color)

    def paintEvent1(self, event):
        qp = QtGui.QPainter()
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        qp.begin(self.result_window)
        qp.setPen(pen)
        for line in self.lines:
            qp.drawLine(50+line[0], 50+line[1], 600, line[2]+10)
        qp.end()

    def paintEvent2(self, event):
        self.super_paintEvent(event)
        qp = QtGui.QPainter()
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        qp.begin(self.picture)
        qp.setPen(pen)
        for line in self.lines:
            qp.drawLine(line[0], line[1], 550, line[2]-40)
        qp.end()

    def draw_image(self, i):
        w = self.img.shape[1]
        h = self.img.shape[0]

        self.picture.resize(QtCore.QSize(500, 500))
        self.frame = QtGui.QImage(self.images[self.type][i], 500, 500, QtGui.QImage.Format_RGB888)
        self.picture.setPixmap(QtGui.QPixmap.fromImage(self.frame))
        self.picture.setGeometry(QtCore.QRect(50, 50, 500, 500))

        self.draw_coordinate(i)
        self.result_window.show()
        self.result_window.update()
        QtWidgets.QApplication.processEvents()

    def draw_coordinate(self, index):
        self.lines = []
        self.label_none.hide()
        for i, coordinate in enumerate(self.coordinates):
            self.coordinates[i].hide()

        self.coordinates = []
        j = 0
        for i, box in enumerate(self.color_boxes[index]):
            if self.color_types[index][i] == self.type:
                center_string, center_x, center_y = self.get_center(box, i)
                self.coordinates.append(QtWidgets.QLabel(self.result_window))
                self.coordinates[j].setText(center_string)
                self.coordinates[j].setGeometry(QtCore.QRect(600, 50 + i * 40, 200, 20))
                self.coordinates[j].setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                self.coordinates[j].show()
                self.lines.append([center_x, center_y, 50 + i * 40])
                j = j+1
        if j == 0:
            self.label_none.show()

    def change_color(self, index):
        for i, button in enumerate(self.color_buttons):
            if i == len(self.color_buttons)-1:
                break
            button.setStyleSheet("background-color:rgb(" + str(self.color_map[i][0]) + ", " + str(self.color_map[i][1]) + ", "
                                            + str(self.color_map[i][2]) + ");\nborder-radius: 10px;")

        if index == len(self.color_buttons)-1:
            self.color_buttons[index].setEnabled(False)
        else:
            self.color_buttons[len(self.color_buttons)-1].setEnabled(True)
            self.color_buttons[index].setStyleSheet("background-color:rgb(" + str(self.color_map[index][0]) + ", " + str(self.color_map[index][1]) + ", "
                                            + str(self.color_map[index][2]) + ");\nborder-radius: 10px;\n\
                                                        border-color: #800000;\n\
                                                        border-width: 1px;\n\
                                                        border-style: solid;")
        self.color = index
        self.draw_image(index)

    def change_type(self, i):
        self.button_front.setEnabled(True)
        self.button_back.setEnabled(True)
        self.button_side.setEnabled(True)
        self.button_none.setEnabled(True)
        if i == 0:
            self.button_front.setEnabled(False)
        if i == 1:
            self.button_back.setEnabled(False)
        if i == 2:
            self.button_side.setEnabled(False)
        if i == 3:
            self.change_color(len(self.color_buttons)-1)
            self.button_none.setEnabled(False)
        self.type = i
        self.draw_image(self.color)

    @staticmethod
    def exist_color(test_color, color_map):
        for i, color in enumerate(color_map):
            if test_color == color:
                return i
        return -1

    @staticmethod
    def find_corner(box):
        x1 = box[0][0]
        x2 = box[0][0]
        y1 = box[0][1]
        y2 = box[0][1]
        for i in range(1, 4):
            if box[i][0] < x1:
                x1 = box[i][0]
            if box[i][0] > x2:
                x2 = box[i][0]
            if box[i][1] < y1:
                y1 = box[i][1]
            if box[i][1] > y2:
                y2 = box[i][1]
        return x1, x2, y1, y2

    def inside(self, i, x, y, j):
        for index, box in enumerate(self.color_boxes[i]):
            if self.color_types[i][index] != j:
                continue
            if box[0][0] <= x <= box[1][0] and box[0][1] <= y <= box[3][1]:
                return True
        return False

    def get_center(self, box, i):
        center_x = round((box[0][0] + box[1][0] + box[2][0] + box[3][0]) / 4 / self.img.shape[1] * 500, 3)
        center_y = round((box[0][1] + box[1][1] + box[2][1] + box[3][1]) / 4 / self.img.shape[0] * 500, 3)
        center_string = str(i + 1) + ':   ' + str(center_x) + '   ' + str(center_y)
        return center_string, center_x, center_y,

    def button_press(self, index):
        if index == 0:
            self.pushButton_2.setStyleSheet("background-color : rgb(255, 63, 76);\n"
                                            "border-radius: 10px;")
        else:
            self.pushButton_3.setStyleSheet("background-color : rgb(85, 85, 85);\n"
                                            "border-radius: 10px;")

    def button_release(self, index):
        if index == 0:
            self.Dialog.close()
        else:
            self.pushButton_3.setStyleSheet("background-color: rgb(103, 101, 104);\n"
                                            "border-radius: 10px;")
