import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkgraystyle


class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Sentiment Analysis")

        self.Width = 1200
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        self.tabs = Tabs(self)
        self.setCentralWidget(self.tabs)
        self.show()


class Tabs(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.Width = 1200
        self.height = int(0.618 * self.Width)
        self.tabs.resize(self.Width, self.height)

        # Add tabs
        self.tabs.addTab(self.tab1, "Sentiment Analysis")
        self.tabs.addTab(self.tab2, "Evaluating the classifier's efficiency")

        # Create first tab ----------------------------------------------------------
        self.tab1.layout = QGridLayout(self)
        # textBox для вставки текста для обработки
        self.textBox1 = QPlainTextEdit(self)
        self.textBox1.Width = 1200
        self.textBox1.height = int(0.19 * self.Width)
        self.textBox1.setFixedSize(self.textBox1.Width, self.textBox1.height)
        # Кнопки
        self.btn1 = QPushButton('Do sentiment analysis', self)
        self.btn1.resize(self.btn1.sizeHint())
        self.btn2 = QPushButton('Positive', self)
        self.btn2.resize(self.btn2.sizeHint())
        self.btn2.setEnabled(False)
        self.btn3 = QPushButton('Negative', self)
        self.btn3.resize(self.btn3.sizeHint())
        self.btn3.setEnabled(False)
        # textBox для отображения результатов
        self.textBox2 = QPlainTextEdit(self)
        self.textBox2.Width = 1200
        self.textBox2.height = int(0.16 * self.Width)
        self.textBox2.setFixedSize(self.textBox2.Width, self.textBox2.height)

        # Таблица с результатами
        self.tableResult = QTableWidget(self)
        self.tableResult.Width = 1200
        self.tableResult.height = int(0.21 * self.Width)
        self.tableResult.setFixedSize(self.tableResult.Width, self.tableResult.height)
        self.tableResult.setColumnCount(4)
        self.tableResult.setHorizontalHeaderLabels(['№', 'Sentence', 'Markup', 'Count'])
        self.tableResult.setColumnWidth(0, 98)
        self.tableResult.setColumnWidth(1, 500)
        self.tableResult.setColumnWidth(2, 500)
        self.tableResult.setColumnWidth(3, 100)

        self.tab1.layout.addWidget(self.textBox1, 0, 0, 1, 3)
        self.tab1.layout.addWidget(self.btn1, 1, 0, 1, 1)
        self.tab1.layout.addWidget(self.btn2, 1, 1, 1, 1)
        self.tab1.layout.addWidget(self.btn3, 1, 2, 1, 1)
        self.tab1.layout.addWidget(self.textBox2, 2, 0, 1, 3)
        self.tab1.layout.addWidget(self.tableResult, 3, 0, 1, 3)

        # create second tab --------------------------------------------------------------
        self.tab2.layout = QGridLayout(self)

        self.statistics = QPushButton('Statistics', self)
        self.statistics.resize(self.statistics.sizeHint())
        self.doc = QPushButton('Documents', self)
        self.doc.resize(self.doc.sizeHint())
        self.pos = QPushButton('Pos', self)
        self.pos.resize(self.pos.sizeHint())
        self.neg = QPushButton('Neg', self)
        self.neg.resize(self.neg.sizeHint())
        self.alt = QPushButton('Alt', self)
        self.alt.resize(self.alt.sizeHint())
        self.th = QPushButton('Th', self)
        self.th.resize(self.th.sizeHint())
        self.inner = QPushButton('Inner', self)
        self.inner.resize(self.inner.sizeHint())

        self.textBox3 = QPlainTextEdit(self)
        self.tab2.layout.addWidget(self.statistics, 0, 0, 1, 1)
        self.tab2.layout.addWidget(self.doc, 1, 0, 1, 1)
        self.tab2.layout.addWidget(self.pos, 2, 0, 1, 1)
        self.tab2.layout.addWidget(self.neg, 3, 0, 1, 1)
        self.tab2.layout.addWidget(self.alt, 4, 0, 1, 1)
        self.tab2.layout.addWidget(self.th, 5, 0, 1, 1)
        self.tab2.layout.addWidget(self.inner, 6, 0, 1, 1)
        self.tab2.layout.addWidget(self.textBox3, 0, 1, 7, 1)

        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    window = AppWindow()

    sys.exit(app.exec_())
