import sys
from PyQt5.QtWidgets import *
import qdarkgraystyle
import AlgorithmSA as algorithm
from PyQt5.QtGui import QIcon
from pathlib import Path
import re


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
        self.btn1.clicked.connect(self.btn_clicked)
        self.btn2.clicked.connect(self.btn_clicked)
        self.btn3.clicked.connect(self.btn_clicked)

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

    def btn_clicked(self):
        text = self.textBox1.toPlainText()
        sender = self.sender()
        if sender.text() == 'Do sentiment analysis':
            self.tableResult.setRowCount(0)
            if text != "":
                self.btn2.setEnabled(True)
                self.btn3.setEnabled(True)
                result, total_value_of_doc, sentiment = algorithm.form_data(text)
                count_words = 0
                for i in result:
                    count_words += len(i[0].split())
                    num_rows = self.tableResult.rowCount()
                    self.tableResult.insertRow(num_rows)
                    for j in range(3):
                        self.tableResult.setItem(num_rows, j, QTableWidgetItem(str(i[j])))
                self.textBox2.setPlainText("The number of words in the document: " + str(count_words)
                                           + "\nTotal count of the document: " + str(total_value_of_doc))
                self.textBox2.appendPlainText("Conclusion: positive" if sentiment > 0 else "Conclusion: negative")
        elif sender.text() == 'Positive':
            self.btn2.setEnabled(False)
            self.btn3.setEnabled(False)
            text = self.textBox2.toPlainText()
            result = re.search(r'Conclusion:(.*)', text).group(1).replace(' ', '')
            self.textBox2.appendPlainText(result)
            if result == "positive":
                algorithm.write_confusion_matrix(0)
            else:
                algorithm.write_confusion_matrix(1)
        elif sender.text() == 'Negative':
            self.btn2.setEnabled(False)
            self.btn3.setEnabled(False)
            text = self.textBox2.toPlainText()
            result = re.search(r'Conclusion:(.*)', text).group(1).replace(' ', '')
            self.textBox2.appendPlainText(result)
            if result == "negative":
                algorithm.write_confusion_matrix(2)
            else:
                algorithm.write_confusion_matrix(3)


class TabForFile(QWidget):
    def __init__(self):
        super().__init__()

        self.Width = 1200
        self.btnFile = QPushButton('Select file', self)
        self.btnFile.resize(self.btnFile.sizeHint())
        self.btnFile.clicked.connect(self.show_dialog)

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

        # Кнопки
        self.btn2 = QPushButton('Positive', self)
        self.btn2.resize(self.btn2.sizeHint())
        self.btn3 = QPushButton('Negative', self)
        self.btn3.resize(self.btn3.sizeHint())
        self.btn2.clicked.connect(self.btn_evaluation)
        self.btn3.clicked.connect(self.btn_evaluation)
        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)
        # textBox для отображения результатов
        self.textBox2 = QPlainTextEdit(self)
        self.textBox2.Width = 1210
        self.textBox2.height = int(0.10 * self.Width)
        self.textBox2.setFixedSize(self.textBox2.Width, self.textBox2.height)

        self.layout = QGridLayout()
        self.layout.addWidget(self.btnFile, 0, 0, 1, 2)
        self.layout.addWidget(self.tableResult, 1, 0, 1, 2)
        self.layout.addWidget(self.btn2, 2, 0)
        self.layout.addWidget(self.btn3, 2, 1)
        self.layout.addWidget(self.textBox2, 3, 0, 1, 2)
        self.setLayout(self.layout)

    def show_dialog(self):
        home_dir = str(Path.home())
        file_filter = "csv (*.csv);;tsv (*.tsv);;text file (*.txt)"
        file_name = QFileDialog.getOpenFileName(self, 'Open file', home_dir, file_filter)

        result, total_value_of_doc, sentiment = algorithm.make_sentiment_analysis(file_name[0])
        if result != None:
            self.tableResult.setRowCount(0)
            count_words = 0
            for i in result:
                count_words += len(i[0].split())
                num_rows = self.tableResult.rowCount()
                self.tableResult.insertRow(num_rows)
                for j in range(3):
                    self.tableResult.setItem(num_rows, j, QTableWidgetItem(str(i[j])))
            self.textBox2.setPlainText("The number of words in the document: " + str(count_words)
                                       + "\nTotal count of the document: " + str(total_value_of_doc))
            self.textBox2.appendPlainText("Conclusion: positive" if sentiment > 0 else "Conclusion: negative")
            self.btn2.setEnabled(True)
            self.btn3.setEnabled(True)

    def btn_evaluation(self):
        sender = self.sender()
        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)
        if sender.text() == 'Positive':
            text = self.textBox2.toPlainText()
            result = re.search(r'Conclusion:(.*)', text).group(1).replace(' ', '')
            self.textBox2.appendPlainText(result)
            if result == "positive":
                algorithm.write_confusion_matrix(0)
            else:
                algorithm.write_confusion_matrix(1)
        elif sender.text() == 'Negative':
            text = self.textBox2.toPlainText()
            result = re.search(r'Conclusion:(.*)', text).group(1).replace(' ', '')
            self.textBox2.appendPlainText(result)
            if result == "negative":
                algorithm.write_confusion_matrix(2)
            else:
                algorithm.write_confusion_matrix(3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    window = AppWindow()

    sys.exit(app.exec_())

# 10139,2364,6216,6286
