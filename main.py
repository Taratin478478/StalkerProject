import requests
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from PyQt5 import uic
import sqlite3
import sys
from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import glob


class InexactFloat(float):
    def __eq__(self, other):
        try:
            return abs(self.real - other) / (0.5 * (abs(self.real) + abs(other))) < 0.1
        except ZeroDivisionError:
            return self.real == other

    def __ne__(self, other):
        return not self.__eq__(other)


class Anomaly:
    def __init__(self, id, x, y, rate):
        self.id = id
        self.x = x
        self.y = y
        self.rate = rate

    def okradius(self):
        return (self.rate / 2) ** 0.5


def safe_path(x1, y1, x2, y2, map):
    grid = Grid(matrix=map)
    start = grid.node(x1, y1)
    end = grid.node(x2, y2)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    print(grid.grid_str(path=path, start=start, end=end))
    return path


'''
def eq1(p, r):
    x1, x2, x3, y1,y2, y3, r1, r2, r3 = p
    xc, yc, k = r
    return (x1 - xc) ** 2 + (y1 - yc) ** 2 - (r1 * k) ** 2, (x2 - xc) ** 2 + (y2 - yc) ** 2 - (r2 * k) ** 2, (x3 - xc) ** 2 + (y3 - yc) ** 2 - (r3 * k) ** 2
'''
class StalkerGator(QMainWindow):
    def __init__(self):
        super().__init__()
        data = requests.get('https://dt.miet.ru/ppo_it_final', headers={'X-Auth-Token': 'dzxylhiz'}).json()["message"]
        raw_anomalies = dict()
        for detector in data:
            for anomaly in detector["swans"]:
                if anomaly["id"] in raw_anomalies.keys():
                    raw_anomalies[anomaly["id"]].append([detector["coords"], anomaly["rate"], anomaly["id"]])
                else:
                    raw = [[detector["coords"], anomaly["rate"], anomaly["id"]]]
                    raw_anomalies[anomaly["id"]] = raw
        anomalies = []
        for anomaly in raw_anomalies.values():
            br = False
            x1, y1 = anomaly[0][0]
            x2, y2 = anomaly[1][0]
            x3, y3 = anomaly[2][0]
            for x in range(40):
                for y in range(30):
                    for k in range(0, 1000):
                        k = k / 10
                        r1sq = k / anomaly[0][1]
                        r2sq = k / anomaly[1][1]
                        r3sq = k / anomaly[2][1]
                        if InexactFloat((x1 - x) ** 2 + (y1 - y) ** 2) == InexactFloat(r1sq) \
                                and InexactFloat((x2 - x) ** 2 + (y2 - y) ** 2) == InexactFloat(r2sq) \
                                and InexactFloat((x3 - x) ** 2 + (y3 - y) ** 2) == InexactFloat(r3sq):
                            anomalies.append(Anomaly(anomaly[0][2], x, y, k))
                            br = True
                            break
                    if br:
                        break
                if br:
                    break
        for anomaly in anomalies:
            print(anomaly.id, anomaly.x, anomaly.y, anomaly.rate)
        map = []
        for y in range(30):
            map.append([])
            for x in range(40):
                not_dangerous = True
                for anomaly in anomalies:
                    if (x - anomaly.x) ** 2 + (y - anomaly.y) ** 2 <= anomaly.okradius():
                        not_dangerous = False
                        break
                map[y].append(int(not_dangerous))
        safe_path(int(input("x start")), int(input("y start")), int(input("x end")), int(input("y end")), map)


        uic.loadUi("ui/stalkergator.ui", self)
        self.label.mousePressEvent = self.test
        self.pushButton.clicked.connect(self.test2)

        self.pixmap = QPixmap()

        pen = QPen(Qt.red, 3)
        self.qp = QPainter(self.pixmap)
        self.qp.setPen(pen)

        print(self.label.size())
        self.pixmap.load('files/map_r.png')
        self.pixmap.scaled(self.label.width(), self.label.height())
        print(self.pixmap.size())
        # self.pixmap = self.pixmap.scaled(699, 541, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label.setPixmap(self.pixmap)
        print(self.pixmap.size())
        print(self.label.size(), self.label.x(), self.label.y())
        self.installEventFilter(self)

    def test(self, event):
        x, y = event.x(), event.y()
        print(x, y)
        fath_x, fath_y = self.pixmap.width(), self.pixmap.height()
        print(fath_x, fath_y)
        cor_x = x // (fath_x / 39)
        cor_y = y // (fath_y / 29)
        pen = QPen(Qt.red, 3)
        self.qp = QPainter(self.pixmap)
        self.qp.setPen(pen)
        print(cor_x, cor_y)
        self.qp.drawLine(int(fath_x / 40 * cor_x), int(fath_y / 30 * cor_y), int(fath_x / 40 * (cor_x + 1)),
                         int(fath_y / 30 * (cor_y + 1)))
        self.qp.drawLine(int(fath_x / 40 * cor_x), int(fath_y / 30 * (cor_y + 1)), int(fath_x / 40 * (cor_x + 1)),
                         int(fath_y / 30 * cor_y))
        self.qp.end()
        self.label.setPixmap(self.pixmap)
        self.x_cords.setText(f"X: {int(cor_x)}")
        self.y_cords.setText(f"Y: {int(cor_y)}")

    def eventFilter(self, obj, event):
        if (event.type() == QtCore.QEvent.Resize):
            print('Inside event Filter')
            self.pixmap.scaledToWidth(self.label.width())
            self.pixmap.scaledToHeight(self.label.height())

        return super().eventFilter(obj, event)

    def test2(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = StalkerGator()
    ex.show()
    sys.exit(app.exec())