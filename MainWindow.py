from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore

from WordSearch import WordSerach

class MainTitle(QLabel):
    def __init__(self, parent, title):
        super().__init__(parent)

        self.setText(title)
        main_font = QtGui.QFont('test', 40, QtGui.QFont.Bold)
        self.setFont(main_font)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

class MyEntry(QGridLayout):
    def __init__(self, parent):
        super().__init__(parent)

        self. rows = 0

    def addEntry(self, text, btn_text, func):
        rows = self.rows
        self.addWidget(QLabel(text + ':'), rows, 0)
        self.inputLine = QLineEdit()
        self.addWidget(self.inputLine, rows, 1)
        search_button = QPushButton(btn_text)
        search_button.clicked.connect(func)
        self.addWidget(search_button, rows, 2)

        self.rows += 1


class ResultBox(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWidgetResizable(True)

        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setReadOnly(True)
        self.setWidget(self.plainTextEdit)

    def appendText(self, text):
        self.plainTextEdit.appendPlainText(text)

class WordList(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)

        self.setSortingEnabled(True)

        self.index = 0

    def addModel(self, cols, textes):
        self.model = QtGui.QStandardItemModel(0, cols)

        if cols != len(textes):
            print('cols: {}  !=  textes length: {}'.format(cols, len(textes)))
            exit()
        else:
            for col in range(cols):
                self.model.setHeaderData(col, QtCore.Qt.Horizontal, textes[col])

        self.setModel(self.model)

    def addItem(self, word):
        item = QtGui.QStandardItem(word)
        self.model.setItem(self.index, 0, item)

        self.index += 1





class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(400, 500)
        self.resize(400, 500)

        self.ws = WordSerach()


        main_layout = QVBoxLayout()

        # self.word_list = WordList(None)
        # self.word_list.addModel(1, ['単語'])
        # self.word_list.addItem('testasd')
        #
        # main_layout.addWidget(self.word_list)

        main_title = MainTitle(None, 'Search Word')
        main_layout.addWidget(main_title)

        self.entry = MyEntry(None)
        self.entry.addEntry('検索単語', '検索', self.searchWord)

        main_layout.addLayout(self.entry)

        self.result_box = ResultBox(None)

        main_layout.addWidget(self.result_box)

        self.setLayout(main_layout)
        self.setWindowTitle('Test')

    def searchWord(self):
        word = self.entry.inputLine.text()
        self.ws.insertDB(word)
        mean = self.ws.readWord(word)
        mean = '\n'.join(mean)
        self.result_box.appendText(mean + '\n')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
