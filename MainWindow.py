from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

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

        self.rows = 0

    def addEntry(self, text, btn_text, func=None):
        rows = self.rows
        self.addWidget(QLabel(text + ':'), rows, 0)
        self.inputLine = QLineEdit()
        self.addWidget(self.inputLine, rows, 1)
        search_button = QPushButton(btn_text)
        if not func is None:
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

    def setText(self, text):
        self.plainTextEdit.setPlainText(text)


class TreeList(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)

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

    def addClicked(self, func):
        self.clicked.connect(func)

    def addItem(self, item):
        for i, data in enumerate(item):
            s_item = QtGui.QStandardItem(data)
            s_item.setEditable(False)
            self.model.setItem(self.index, i, s_item)

        self.index += 1

    def addItems(self, items):
        pass


class History(QVBoxLayout):
    def __init__(self, parent, ws):
        super().__init__(parent)

        self.ws = ws

        # history list
        self.history_list = TreeList(None)
        self.history_list.addModel(2, ['単語', '日時'])
        self.history_list.addClicked(self.selectHistory)
        self.addWidget(self.history_list)

        # result box
        self.result_box = ResultBox(None)
        self.addWidget(self.result_box)

        self.initHistory()

    def initHistory(self):
        if not self.history_list.model.hasChildren() is None:
            count = self.history_list.model.rowCount()
            self.history_list.model.removeRows(0, count)
            self.history_list.index = 0

        datas = self.ws.getHistory()
        if not datas is None:
            self.items = [(item['word'], item['updated_time'].strftime('%Y-%m-%d'),
                           item['mean']) for item in datas]
            self.addItems(self.items)

    def addItems(self, datas):
        for data in datas:
            self.history_list.addItem([data[0], data[1]])

    def selectHistory(self, q_model):
        index = q_model.row()
        mean = self.items[index][2]
        self.result_box.setText(mean + '\n')


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(600, 500)
        self.resize(600, 500)
        self.setWindowTitle('Test')

        self.ws = WordSerach()

        main_h_layout = QHBoxLayout()
        self.setLayout(main_h_layout)

        # histoy layout
        self.history_panel = History(None, self.ws)
        main_h_layout.addLayout(self.history_panel)

        main_layout = QVBoxLayout()
        main_h_layout.addLayout(main_layout)

        # main title
        main_title = MainTitle(None, 'Search Word')
        main_layout.addWidget(main_title)

        # search word entry
        self.entry = MyEntry(None)
        self.entry.addEntry('検索単語', '検索', self.searchWord)
        main_layout.addLayout(self.entry)

        # reuslt box
        self.result_box = ResultBox(None)
        main_layout.addWidget(self.result_box)

    def searchWord(self):
        word = self.entry.inputLine.text()
        self.ws.insertDB(word)
        mean = self.ws.getWord(word)['mean']
        self.result_box.appendText(mean + '\n')

        self.history_panel.history_list.addItem([word, word])

        self.history_panel.initHistory()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
