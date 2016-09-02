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
        pass

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


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ShowInfo('aasd')
    sys.exit(app.exec_())
