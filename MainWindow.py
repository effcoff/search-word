from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from WordSearch import WordSerach


# from Singleton import Singleton


class MainTitle(QLabel):
    def __init__(self, parent, title, font_size=40):
        super().__init__(parent)

        font = QtGui.QFont(None, font_size, QtGui.QFont.Bold)

        self.setText(title)
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)


class MyEntry(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QGridLayout(self)

        self.__inputs = []

        self.__rows = 0

    def addEntry(self, text, btn_text, func=None):
        # ラベル 設定
        self.layout.addWidget(QLabel(text + ':'), self.__rows, 0)

        # 入力枠 設定
        entry = QLineEdit()
        entry.returnPressed.connect(func)
        self.layout.addWidget(entry, self.__rows, 1)
        self.__inputs.append(entry)

        # ボタン 設定
        search_btn = QPushButton(btn_text)
        if not func is None:
            search_btn.clicked.connect(func)
        self.layout.addWidget(search_btn, self.__rows, 2)

        self.__rows += 1

    def getEntry(self, index=0):
        return self.__inputs[index].text()


class ResultBox(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWidgetResizable(True)

        self.text_box = QPlainTextEdit()
        self.text_box.setReadOnly(True)
        self.setWidget(self.text_box)

    def appendText(self, text):
        self.text_box.appendPlainText(text)

    def setText(self, text):
        self.text_box.setPlainText(text)


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

    def clearItems(self):
        # リストが存在していたら、リスト全削除
        if not self.model.hasChildren() is None:
            count = self.model.rowCount()
            self.model.removeRows(0, count)
            self.index = 0
            return True
        return False


class History(QFrame):
    def __init__(self, parent, ws):
        super().__init__(parent)

        self.setMinimumWidth(250)

        layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.ws = ws

        # タイトル
        self.title = MainTitle(None, '履歴', 18)
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.title)

        # リスト設定
        self.list = TreeList(None)
        self.list.addModel(2, ['単語', '日時'])
        self.list.addClicked(self.selectHistory)
        layout.addWidget(self.list)

        # 意味表示ボックス
        self.result_box = ResultBox(None)
        layout.addWidget(self.result_box)

        self.initHistory()

    def getList(self):
        if not self.list is None:
            return self.list
        return None

    def initHistory(self):
        self.list.clearItems()

        datas = self.ws.getHistory()
        if not datas is None:
            self.items = [(item['word'], item['updated_time'].strftime('%Y-%m-%d'),
                           item['mean']) for item in datas]
            self.addItems(self.items)

    def addItems(self, datas):
        for data in datas:
            self.list.addItem([data[0], data[1]])

    def selectHistory(self, q_model):
        index = q_model.row()
        mean = self.items[index][2]
        self.result_box.setText(mean + '\n')


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(700, 600)
        self.resize(700, 600)
        self.setWindowTitle('Test')

        self.ws = WordSerach()
        splitter = QSplitter(self)

        main_h_layout = QHBoxLayout()
        self.setLayout(main_h_layout)

        # 履歴部分
        self.history = History(self, self.ws)
        # main_h_layout.addWidget(self.history)
        splitter.addWidget(self.history)

        # メイン部分
        main_layout = MainFrame(self, self.ws, self.history)
        # main_h_layout.addWidget(main_layout)
        splitter.addWidget(main_layout)
        main_h_layout.addWidget(splitter)

    def separatorV(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        return sep


class MainFrame(QFrame):
    def __init__(self, parent, ws, history):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.ws = ws
        self.history = history

        # メインタイトル
        main_title = MainTitle(None, 'Search Word')
        main_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(main_title)

        # 検索単語
        self.entry = MyEntry(None)
        self.entry.addEntry('検索単語', '検索', self.searchWord)
        layout.addWidget(self.entry)
        layout.addWidget(self.separatorH())

        result_title = MainTitle(None, '-----  検索結果  -----', 10)
        result_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(result_title)

        # reuslt box
        self.result_box = ResultBox(None)
        layout.addWidget(self.result_box)

    def separatorH(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        return sep

    def searchWord(self):
        word = self.entry.getEntry()
        main = MainWindow()
        datas = self.ws.insertDB(word)
        if datas is None:
            self.result_box.appendText('意味が見つかりませんでした。' + '\n')
            return None
        self.result_box.appendText(datas['mean'] + '\n')

        self.history.initHistory()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
