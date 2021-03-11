import sys
from PyQt5.QtWidgets import *
import qdarkgraystyle
import AlgorithmSA as algorithm


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
        self.tabs.addTab(self.tab2, "Statistics")

        # Create first tab ----------------------------------------------------------
        self.tab1.layout = QGridLayout(self)
        # textBox для вставки текста для обработки
        self.textBox1 = QPlainTextEdit(self)
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

        self.tab1.layout.addWidget(self.textBox1, 0, 0, 1, 1)
        self.tab1.layout.addWidget(self.tableResult, 0, 1, 1, 2)
        self.tab1.layout.addWidget(self.btn1, 1, 0)
        self.tab1.layout.addWidget(self.btn2, 1, 1)
        self.tab1.layout.addWidget(self.btn3, 1, 2)

        self.tab1.layout.addWidget(self.textBox2, 2, 0, 1, 3)


        # create second tab --------------------------------------------------------------
        self.tab2.layout = QGridLayout(self)

        self.statistics = QPushButton('Statistics', self)
        self.statistics.resize(self.statistics.sizeHint())
        self.doc = QPushButton('Documents', self)
        self.doc.resize(self.doc.sizeHint())

        self.table2 = QTableWidget(self)
        self.tab2.layout.addWidget(self.statistics, 0, 0, 1, 1)
        self.tab2.layout.addWidget(self.doc, 1, 0, 1, 1)
        self.tab2.layout.addWidget(self.table2, 0, 1, 7, 1)

        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.btn1.clicked.connect(self.btn_clicked)
        self.btn2.clicked.connect(self.btn_clicked)
        self.btn3.clicked.connect(self.btn_clicked)
        self.statistics.clicked.connect(self.btn_statistics)
        self.doc.clicked.connect(self.btn_statistics)

    def btn_clicked(self):
        text = self.textBox1.toPlainText()
        sender = self.sender()
        if sender.text() == 'Do sentiment analysis':
            self.tableResult.setRowCount(0)
            if text != "":
                self.btn2.setEnabled(True)
                self.btn3.setEnabled(True)
                result_data, total_count = algorithm.form_data(text)
                count_word = algorithm.count_words(text)
                self.textBox2.setPlainText("The number of words in the document: "+str(count_word)
                                           + "\nTotal count of the document: " + str(total_count))
                self.textBox2.appendPlainText("Conclusion: positive" if total_count > 0 else "Conclusion: negative")
                conf_t = algorithm.read_confusion_matrix()
                tp = int(conf_t[0][0])
                fp = int(conf_t[0][1])
                fn = int(conf_t[0][3])

                #self.textBox2.appendPlainText("Precision: " + str(int(conf_t[0][0])/(int(conf_t[0][0])+int(conf_t[0][1]))))
               # self.textBox2.appendPlainText("Recall: " + str(int(conf_t[0][0]) / (int(conf_t[0][0]) + int(conf_t[0][3]))))
                for i in result_data:
                    num_rows = self.tableResult.rowCount()
                    self.tableResult.insertRow(num_rows)
                    self.tableResult.setItem(num_rows, 0, QTableWidgetItem(i[0]))
                    self.tableResult.setItem(num_rows, 1, QTableWidgetItem(i[1]))
                    self.tableResult.setItem(num_rows, 2, QTableWidgetItem(str(i[2])))

        elif sender.text() == 'Positive':
            if text != "":
                result_data, total_count = algorithm.form_data(text)
                self.textBox2.setPlainText(' '.join(sender.text()))
                if total_count > 0:
                    algorithm.write_confusion_matrix(0)
                else:
                    algorithm.write_confusion_matrix(3)
                self.btn2.setEnabled(False)
                self.btn3.setEnabled(False)
        elif sender.text() == 'Negative':
            if text != "":
                result_data, total_count = algorithm.form_data(text)
                self.textBox2.setPlainText(' '.join(sender.text()))
                if total_count > 0:
                    algorithm.write_confusion_matrix(1)
                else:
                    algorithm.write_confusion_matrix(2)
                self.btn2.setEnabled(False)
                self.btn3.setEnabled(False)

    def btn_statistics(self):
        sender = self.sender()
        if sender.text() == 'Statistics':
            self.table2.setRowCount(0)
            self.table2.setColumnCount(7)
            self.table2.setHorizontalHeaderLabels(['TP', 'FP', 'TN', 'FN', 'Precision', 'Recall', 'F1'])
            self.table2.setColumnWidth(0, 120)
            self.table2.setColumnWidth(1, 120)
            self.table2.setColumnWidth(2, 120)
            self.table2.setColumnWidth(3, 120)
            self.table2.setColumnWidth(4, 200)
            self.table2.setColumnWidth(5, 150)
            self.table2.setColumnWidth(6, 150)

            conf_t = algorithm.read_confusion_matrix()
            tp = int(conf_t[0][0])
            fp = int(conf_t[0][1])
            fn = int(conf_t[0][3])
            precision = tp/(tp+fp)
            recall =tp/(tp+fn)
            f1 = 2*(precision*recall/(precision+recall))
            num_rows = self.table2.rowCount()
            self.table2.insertRow(num_rows)
            for i in range(len(conf_t[0])):
                self.table2.setItem(num_rows, i, QTableWidgetItem(conf_t[0][i]))
            self.table2.setItem(num_rows, 4, QTableWidgetItem(str(precision)))
            self.table2.setItem(num_rows, 5, QTableWidgetItem(str(recall)))
            self.table2.setItem(num_rows, 6, QTableWidgetItem(str(f1)))

        elif sender.text() == 'Documents':
            self.table2.setRowCount(0)
            self.table2.setColumnCount(6)
            self.table2.setHorizontalHeaderLabels(['doc', 'markup', 'count', 'ton'])
            self.table2.setColumnWidth(0, 500)
            self.table2.setColumnWidth(1, 400)
            self.table2.setColumnWidth(2, 150)
            self.table2.setColumnWidth(3, 150)
            docs = algorithm.read_doc()
            for i in docs:
                num_rows = self.table2.rowCount()
                self.table2.insertRow(num_rows)
                self.table2.setItem(num_rows, 0, QTableWidgetItem(i[0]))
                self.table2.setItem(num_rows, 1, QTableWidgetItem(i[1]))
                self.table2.setItem(num_rows, 2, QTableWidgetItem(i[2]))
                self.table2.setItem(num_rows, 3, QTableWidgetItem(i[3]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    window = AppWindow()

    sys.exit(app.exec_())
