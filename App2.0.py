import sys
from PyQt5.QtWidgets import *
import qdarkgraystyle
import AlgorithmSA as algorithm
from PyQt5.QtGui import QIcon
from pathlib import Path

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
        self.tab3 = QWidget()
        self.Width = 1200
        self.height = int(0.618 * self.Width)
        self.tabs.resize(self.Width, self.height)

        self.tabForTextBox = TabForTextBox()
        self.tabForFile = TabForFile()

        # Add tabs
        self.tabs.addTab(self.tabForTextBox, "Sentiment Analysis (textbox)")
        self.tabs.addTab(self.tabForFile, "Sentiment Analysis (file)")
        self.tabs.addTab(self.tab2, "Statistics")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class TabForTextBox(QWidget):
    def __init__(self):
        super().__init__()

        self.Width = 1200
        # textBox для вставки текста для обработки
        self.textBox1 = QPlainTextEdit()
        self.textBox1.Width = 500
        self.textBox1.height = int(0.45 * self.Width)
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
        self.textBox2.Width = 1210
        self.textBox2.height = int(0.10 * self.Width)
        self.textBox2.setFixedSize(self.textBox2.Width, self.textBox2.height)

        # Таблица с результатами
        self.tableResult = QTableWidget(self)
        self.tableResult.Width = 700
        self.tableResult.height = int(0.45 * self.Width)
        self.tableResult.setFixedSize(self.tableResult.Width, self.tableResult.height)
        self.tableResult.setColumnCount(3)
        self.tableResult.setHorizontalHeaderLabels(['Sentence', 'Markup', 'Count'])
        self.tableResult.setColumnWidth(0, 350)
        self.tableResult.setColumnWidth(1, 270)
        self.tableResult.setColumnWidth(2, 60)

        self.layout = QGridLayout()
        self.layout.addWidget(self.textBox1, 0, 0, 1, 1)
        self.layout.addWidget(self.tableResult, 0, 1, 1, 2)
        self.layout.addWidget(self.btn1, 1, 0)
        self.layout.addWidget(self.btn2, 1, 1)
        self.layout.addWidget(self.btn3, 1, 2)
        self.layout.addWidget(self.textBox2, 2, 0, 1, 3)

        self.setLayout(self.layout)


class TabForFile(QWidget):
    def __init__(self):
        super().__init__()

        self.Width = 1200
        self.btnFile = QPushButton('Select file', self)
        self.btnFile.resize(self.btnFile.sizeHint())
        self.btnFile.clicked.connect(self.showDialog)

        # Таблица с результатами
        self.tableResult = QTableWidget(self)
        self.tableResult.Width = 1210
        self.tableResult.height = int(0.45 * self.Width)
        self.tableResult.setFixedSize(self.tableResult.Width, self.tableResult.height)
        self.tableResult.setColumnCount(3)
        self.tableResult.setHorizontalHeaderLabels(['Sentence', 'Markup', 'Count'])
        self.tableResult.setColumnWidth(0, 550)
        self.tableResult.setColumnWidth(1, 550)
        self.tableResult.setColumnWidth(2, 100)

        # textBox для отображения результатов
        self.textBox2 = QPlainTextEdit(self)
        self.textBox2.Width = 1210
        self.textBox2.height = int(0.10 * self.Width)
        self.textBox2.setFixedSize(self.textBox2.Width, self.textBox2.height)

        self.layout = QGridLayout()
        self.layout.addWidget(self.btnFile, 0, 0, 1, 1)
        self.layout.addWidget(self.tableResult, 1, 0, 1, 1)
        self.layout.addWidget(self.textBox2, 2, 0, 1, 1)
        self.setLayout(self.layout)

    def showDialog(self):
        home_dir = str(Path.home())
        filter = "csv (*.csv);;tsv (*.tsv);;text file (*.txt)"
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir, filter)

        result, total_value_of_doc, sentiment = algorithm.make_sentiment_analysis(fname[0])
        if result != None:
            self.tableResult.setRowCount(0)
            for i in result:
                num_rows = self.tableResult.rowCount()
                self.tableResult.insertRow(num_rows)
                for j in range(3):
                    self.tableResult.setItem(num_rows, j, QTableWidgetItem(str(i[j])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    window = AppWindow()

    sys.exit(app.exec_())
