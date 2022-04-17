from PyQt5 import uic
import sqlite3
import sys
from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets


class StalkerGator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/stalkergator.ui", self)
        self.label.mousePressEvent = self.test

    def test(self, event):
        x, y = event.x(), event.y()
        fath_x, fath_y = self.label.width(), self.label.height()
        cor_x = x // (fath_x / 40)
        cor_y = y // (fath_y / 30)
        pixmap = QPixmap(self.label.size())

        # pixmap.fill(Qt.transparent)
        qp = QPainter(pixmap)
        pen = QPen(Qt.red, 3)
        qp.setPen(pen)
        # pixmap.load('files/map.png')
        qp.drawLine(fath_x / 40 * cor_x, fath_y / 30 * cor_y, fath_x / 40 * (cor_x + 1), fath_y / 30 * (cor_y + 1))
        qp.drawLine(fath_x / 40 * cor_x, fath_y / 30 * (cor_y + 1), fath_x / 40 * (cor_x + 1), fath_y / 30 * cor_y)
        qp.end()
        self.label.setPixmap(pixmap)
        self.x_cords.setText(f"X: {int(cor_x)}")
        self.y_cords.setText(f"Y: {int(cor_y)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = StalkerGator()
    ex.show()
    sys.exit(app.exec())
