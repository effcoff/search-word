from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *


class MainTitle(QLabel):
    def __init__(self, parent, title, font_size=40):
        super().__init__(parent)

        font = QtGui.QFont()
        font.setPointSize(font_size)
        font.setWeight(QtGui.QFont.Bold)

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


from SettingDB import SettingsDB


class ResultBox(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWidgetResizable(True)

        self.text_box = QTextEdit()
        self.text_box.setAcceptRichText(True)
        self.text_box.setReadOnly(True)
        font_size = SettingsDB().getSettings()['fontsize']
        self.setFontSize(int(font_size))
        self.setWidget(self.text_box)

    def appendText(self, text):
        self.text_box.append(text)

    def setText(self, text):
        self.text_box.setText(text)

    def setFontSize(self, font_size):
        font = QtGui.QFont()
        font.setPointSize(font_size)
        self.setFont(font)


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
        for item in items:
            self.addItem(item)

    def clearItems(self):
        # リストが存在していたら、リスト全削除
        if not self.model.hasChildren() is None:
            count = self.model.rowCount()
            self.model.removeRows(0, count)
            self.index = 0
            return True
        return False


class ShowInfo(QMessageBox):
    def __init__(self, text, info_text=None, func=None, parent=None):
        super().__init__(parent)

        self.setIcon(QMessageBox.Information)
        self.setWindowTitle('お知らせ')
        self.setText(text)
        if not info_text is None:
            self.setInformativeText(info_text)

        self.exec_()


class WordList(QFrame):
    WORD = 0
    MEAN = 2
    UPDATE_TIME = 1

    def __init__(self, parent=None):
        super().__init__(parent)

        self.title = None
        self.list = None
        self.result_box = None

        self.__cols = 0

    def createTitle(self, text, fontsize):
        self.title = MainTitle(None, text, fontsize)
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        return self.title

    def createList(self, cols, headers, clicked_func=None):
        self.list = TreeList(None)
        self.list.addModel(cols, headers)
        if not clicked_func is None:
            self.list.addClicked(clicked_func)
        else:
            self.list.addClicked(self.selectWord)

        self.__cols = cols

        return self.list

    def createResultBox(self):
        self.result_box = ResultBox(None)

        return self.result_box

    # 引数datas には、リスト生成の時のheadersに対する配列
    def initList(self, datas):
        self.list.clearItems()

        # 配列の中身がなく、リストヘッダーの個数でなけれな、処理終える
        if len(datas) <= 0 and len(datas[0]) != self.__cols:
            print('Wordlist input datas-length: {}, datas[0]-length: {}'.format(
                len(datas), len(datas[0])
            ))
            return None

        # 正しいデータならば初期化を行う
        items = [(x for x in data) for data in datas]
        self.list.addItems(items)

    def addItem(self, item):
        self.list.addItem(item)
        self.items.append(item)

    def getSelectValues(self, q_model):
        index = q_model.row()
        return self.items[index]

    def setResultBox(self, text):
        self.result_box.setText(text + '\n')

    def appendReusltBox(self, text):
        self.result_box.appendText(text + '\n')

    def selectWord(self, q_model):
        value = self.getSelectValues(q_model)
        self.setResultBox(value[self.MEAN])

    def getWords(self, db, limit=-1):
        datas = db.selectAllOrderByUpdatedDesc(limit)

        if datas is None:
            print('単語が登録されていません')
            return None

        self.items = [(item['word'], item['updated_time'].strftime('%Y-%m-%d'),
                       item['mean']) for item in datas]
        return self.items


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ShowInfo('aasd')
    sys.exit(app.exec_())
