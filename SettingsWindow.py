from PyQt5.QtWidgets import *
import sys
from common import ResultBox, ShowInfo
from PyQt5 import QtGui, QtCore

from SettingDB import SettingsDB


class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        setting_widget = SettingsWidget(self)
        self.setCentralWidget(setting_widget)


class SettingsWidget(QWidget):
    DB_NAME = 0
    FONT_SIZE = 1
    HISTORY_NUM = 2

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.labels = ['データベース名', 'フォントサイズ', '履歴表示数']
        self.setting_db = SettingsDB()
        settings = self.setting_db.getSettings()

        entry = SettingList(None)
        entry.addEntry(self.labels[self.DB_NAME],
                       default=settings['dbname'],
                       func=self.changeDbName)

        font_sizes = [str(i) for i in range(40)]
        entry.addCombo(self.labels[self.FONT_SIZE],
                       font_sizes,
                       current_index=settings['fontsize'],
                       func=self.changefontSize)

        self.history_nums = [str(i) for i in range(201) if i % 5 == 0 and i != 0]
        his_num = self.history_nums.index(str(settings['history_num']))

        entry.addCombo(self.labels[self.HISTORY_NUM],
                       self.history_nums,
                       current_index=his_num,
                       func=self.changeHistoryNum)
        main_layout.addWidget(entry)

        self.result_texts = ['' for _ in range(len(self.labels))]
        self.result_texts[self.DB_NAME] = settings['dbname']
        self.result_texts[self.FONT_SIZE] = settings['fontsize']
        self.result_texts[self.HISTORY_NUM] = settings['history_num']
        self.result_box = ResultBox(None)
        self.result_box.setFontSize(int(self.result_texts[self.FONT_SIZE]))
        main_layout.addWidget(self.result_box)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton('保存')
        ok_btn.clicked.connect(self.saveSettings)
        btn_layout.addWidget(ok_btn)

        cancel_btn = QPushButton('キャンセル')
        cancel_btn.clicked.connect(self.cancelSettings)
        btn_layout.addWidget(cancel_btn)

        main_layout.addLayout(btn_layout)

        self.setResult()
        print('ensd')

    def changeDbName(self, value):
        self.result_texts[self.DB_NAME] = value
        self.setResult()

    def changefontSize(self, value):
        self.result_texts[self.FONT_SIZE] = int(value)
        self.setResult()

    def changeHistoryNum(self, value):
        self.result_texts[self.HISTORY_NUM] = int(self.history_nums[value])
        self.setResult()

    def setResult(self):
        str = '\n'.join(['{} : {}'.format(label, self.result_texts[i]) for i, label in enumerate(self.labels)])
        self.result_box.setFontSize(int(self.result_texts[self.FONT_SIZE]))
        self.result_box.setText(str)

    def saveSettings(self):
        dbname = self.result_texts[self.DB_NAME]
        fontsize = self.result_texts[self.FONT_SIZE]
        history_num = self.result_texts[self.HISTORY_NUM]
        self.setting_db.updateSettings(dbname,
                                       fontsize,
                                       history_num)

        ShowInfo(text='保存されました。',
                 info_text='保存内容を反映させるためには、再起動をおこなってください。',
                 parent=self)
        self.parent.destroy()

    def cancelSettings(self):
        self.parent.destroy()
        pass


class SettingList(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QGridLayout(self)

        self.__inputs = []

        self.__rows = 0

    def addEntry(self, text, default=None, func=None):
        self.layout.addWidget(QLabel(text + ':'), self.__rows, 0)

        entry = QLineEdit()
        if not default is None:
            entry.setText(default)
        self.layout.addWidget(entry, self.__rows, 1)

        if not func is None:
            entry.textChanged.connect(func)
        self.__inputs.append(entry)

        self.__rows += 1

    def addCombo(self, text, items, current_index=0, func=None):
        self.layout.addWidget(QLabel(text + ':'), self.__rows, 0)

        cb = QComboBox()
        cb.addItems(items)
        cb.setStyleSheet("QComboBox { combobox-popup: 0; }");
        cb.setMaxVisibleItems(10)
        cb.setCurrentIndex(current_index)
        if not func is None:
            cb.currentIndexChanged.connect(func)
        self.layout.addWidget(cb, self.__rows, 1)

        self.__rows += 1

    def getEntry(self, index=0):
        return self.__inputs[index].text()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    sub = SettingsWindow()
    sub.show()
    sys, exit(app.exec_())
