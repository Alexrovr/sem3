import sys
import sqlite3
import datetime as dt
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.Qt import *


class List(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pr.ui', self)
        self.load()

    def load(self):
        self.setWindowTitle('Paint')
        self.kar = False
        self.place = []
        self.sc = QPoint()
        self.fc = QPoint()
        self.im = QPixmap()
        self.size = 1
        self.color = QColor(255, 255, 255)
        self.color2 = QColor(0, 0, 0)
        self.im.fill(self.color)
        self.pushButton.clicked.connect(self.change_painter)
        self.pushButton_4.clicked.connect(self.openim)
        self.pushButton_2.clicked.connect(self.saveim)
        self.pushButton_3.clicked.connect(self.new_image)
        self.pushButton_5.setStyleSheet("background-color: {}".format(self.color.name()))
        self.pushButton_10.setStyleSheet("background-color: {}".format(self.color2.name()))
        self.pushButton_5.clicked.connect(self.change_color)
        self.pushButton_10.clicked.connect(self.change_color2)
        self.comboBox.addItem('1')
        self.comboBox.addItem('2')
        self.comboBox.addItem('3')
        self.comboBox.addItem('4')
        self.comboBox.addItem('5')
        self.comboBox.addItem('6')
        self.comboBox.addItem('7')
        self.comboBox.addItem('8')
        self.comboBox.addItem('9')
        self.comboBox.addItem('10')
        self.pushButton_6.clicked.connect(self.change_painter)
        self.painter = 0
        self.comboBox.activated[str].connect(self.change_size)
        self.pushButton_8.clicked.connect(self.change_painter)
        self.pushButton_7.clicked.connect(self.change_painter)
        self.pushButton_9.clicked.connect(self.change_painter)
        self.pushButton_11.clicked.connect(self.show_db)
        self.maincolor = QColor(255, 255, 255)
        self.las = False
        self.kar = False
        self.db = False

    def save_to_db(self, p):
        date = dt.datetime.now().date()
        time = dt.datetime.now().time()
        con = sqlite3.connect('pro_db.sqlite')
        cur = con.cursor()
        cur.execute(f"""INSERT INTO saves(Путь,Дата,Время) VALUES('Сохранено({str(p)})','{str(date)}','{str(time)}')""")
        con.commit()
        con.close()
        self.show_db()
        self.show_db()

    def show_db(self):
        if self.db:
            self.stop_show()
        else:
            self.tableWidget = QTableWidget(self)
            self.tableWidget.resize(330, 560)
            self.tableWidget.move(780, 110)
            con = sqlite3.connect('pro_db.sqlite')
            cur = con.cursor()
            res = cur.execute("""SELECT * from saves""").fetchall()
            con.commit()
            con.close()
            self.tableWidget.setRowCount(len(res))
            self.tableWidget.setColumnCount(3)
            for i in range(len(res)):
                for t in range(3):
                    self.tableWidget.setItem(i, t, QTableWidgetItem(res[i][t]))
            self.tableWidget.show()
            self.db = True

    def stop_show(self):
        self.tableWidget.deleteLater()
        self.tableWidget = 0
        self.db = False

    def change_painter(self):
        a = self.sender().text()
        if a == 'Прямоугольник':
            self.painter = self.draw_rect
            self.las = False
            self.kar = False
        elif a == 'Линия':
            self.painter = self.draw_line
            self.las = False
            self.kar = False
        elif a == 'Эллипс':
            self.painter = self.draw_ellipse
            self.las = False
            self.kar = False
        elif a == 'Ластик':
            self.painter = self.lastik
            self.las = True
            self.kar = False
        elif a == 'Карандаш':
            self.painter = self.karandash
            self.las = False
            self.kar = True

    def change_color(self):
        color = QColorDialog.getColor()
        self.color = color
        self.pushButton_5.setStyleSheet("background-color: {}".format(self.color.name()))

    def change_color2(self):
        color = QColorDialog.getColor()
        self.color2 = color
        self.pushButton_10.setStyleSheet("background-color: {}".format(self.color2.name()))

    def change_size(self):
        t = self.comboBox.currentText()
        self.size = int(t)

    def karandash(self, p):
        p = QPainter(self.im)
        p.setBrush(self.color2)
        pen = QPen(self.color2)
        pen.setWidth(self.size)
        p.setPen(pen)

        # Проблема здесь - self.size / 2 дает float
        # Исправляем на целочисленное деление или int()
        x = self.fc.x() - 50 - self.size // 2  # или int(self.size / 2)
        y = self.fc.y() - 150 - self.size // 2
        x2 = self.fc.x() - 50 + self.size // 2
        y2 = self.fc.y() - 150 + self.size // 2

        a1 = QPoint(x, y)
        a2 = QPoint(x2, y2)
        rect = QRect(a1, a2)
        p.drawEllipse(rect)

    def new_image(self):
        self.im = QPixmap(500, 500)
        self.im.fill(self.color)
        self.maincolor = self.color
        self.update()

    def saveim(self):
        a = QFileDialog.getSaveFileName(self, 'Выбрать файл', '')[0]
        self.im.save(a)
        self.save_to_db(a)

    def openim(self):
        a = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.im = QPixmap(a)
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.drawPixmap(50, 150, self.im)
        if self.las or self.kar:
            self.painter(qp)
        qp.setBrush(self.color)
        pen = QPen(self.color2)
        pen.setWidth(self.size)
        qp.setPen(pen)
        if self.painter != 0:
            self.painter(qp)

    def lastik(self, p):
        p = QPainter(self.im)
        p.setBrush(self.maincolor)
        pen = QPen(self.maincolor)
        pen.setWidth(self.size)
        p.setPen(pen)
        a1 = QPoint(self.fc.x() - 50 - self.size, self.fc.y() - 150 - self.size)
        a2 = QPoint(self.fc.x() - 50 + self.size, self.fc.y() - 150 + self.size)
        rect = QRect(a1, a2)
        p.drawRect(rect)

    def draw_rect(self, qp, a1=0, a2=0):
        if a1 == 0:
            rect = QRect(self.sc, self.fc)
        else:
            rect = QRect(a1, a2)
        qp.drawRect(rect)

    def draw_ellipse(self, qp, a1=0, a2=0):
        if a1 == 0:
            rect = QRect(self.sc, self.fc)
        else:
            rect = QRect(a1, a2)
        qp.drawEllipse(rect)

    def draw_line(self, qp, a1=0, a2=0):
        if a1 == 0:
            line = QLine(self.sc, self.fc)
        else:
            line = QLine(a1, a2)
        qp.drawLine(line)

    def mousePressEvent(self, event):
        if self.painter != 0 and event.button() == Qt.LeftButton:
            a = event.pos()
            self.sc = event.pos()
            self.fc = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if self.painter != 0:
            self.fc = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.painter != 0 and event.button() == Qt.LeftButton and not self.las and not self.kar:
            p = QPainter(self.im)
            p.setBrush(self.color)
            pen = QPen(self.color2)
            pen.setWidth(self.size)
            p.setPen(pen)
            a1 = QPoint(self.sc.x() - 50, self.sc.y() - 150)
            a2 = QPoint(self.fc.x() - 50, self.fc.y() - 150)
            self.painter(p, a1=a1, a2=a2)
            self.sc = QPoint()
            self.fc = QPoint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = List()
    form.show()
    sys.exit(app.exec_())
