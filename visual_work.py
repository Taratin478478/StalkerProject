from PyQt5 import uic
import sqlite3
import sys
from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import glob

class StalkerGator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/stalkergator.ui", self)
        self.label.mousePressEvent = self.test
        self.pushButton.clicked.connect(self.test2)

        self.pixmap = QPixmap()
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
