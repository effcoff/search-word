from PyQt5.QtWidgets import *
import sys
from common import ResultBox, ShowInfo

from SettingDB import SettingsDB


# 設定画面メイン
class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        setting_widget = SettingsWidget(self)
        self.setCentralWidget(setting_widget)


# 設定画面のウィジェット
class SettingsWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # 設定データベース
        self.setting_db = SettingsDB()

        # メインレイアウト設定
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 設定入力エントリー
        self.entry = SettingEntryPanel(self.setResult)
        main_layout.addWidget(self.entry)

        # 変更結果表示ボックス
        self.result_box = ResultBox(None)
        main_layout.addWidget(self.result_box)

        # ボタン
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton('保存')
        ok_btn.clicked.connect(self.saveSettings)
        btn_layout.addWidget(ok_btn)

        cancel_btn = QPushButton('キャンセル')
        cancel_btn.clicked.connect(self.cancelSettings)
        btn_layout.addWidget(cancel_btn)
        main_layout.addLayout(btn_layout)

        self.setResult()

    # 結果表示ボックスに表示させる
    def setResult(self):
        str = '\n'.join([
            '{} : {}'.format(setting['label'], setting['value'])
            for setting in self.entry.getSettings()
        ])
        fontsize = self.entry.getFontSize()
        self.result_box.setFontSize(int(fontsize))
        self.result_box.setText(str)

    # 設定を保存する
    def saveSettings(self):
        dbname = self.entry.getDBName()
        fontsize = self.entry.getFontSize()
        history_num = self.entry.getHistoryNum()
        self.setting_db.updateSettings(dbname, fontsize, history_num)

        ShowInfo(
            text='保存されました。',
            info_text='保存内容を反映させるためには、再起動をおこなってください。',
            parent=self)

    # 設定をキャンセルし元にもどる
    def cancelSettings(self):
        self.parent.destroy()


# 設定入力パネル
class SettingEntryPanel(QFrame):
    DB_NAME = 0
    FONT_SIZE = 1
    HISTORY_NUM = 2

    def __init__(self, callback=None):
        super().__init__()

        # 設定内容を変更した際に呼び出させる関数
        if not callback is None:
            self.callback = callback

        # メインレイアウト
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 設定値の初期化
        db = SettingsDB()
        settings = db.getSettings()
        self.values = [
            settings['dbname'], settings['fontsize'], settings['history_num']
        ]
        self.labels = ['データベース名', 'フォントサイズ', '履歴表示数']

        # データベース名設定項目
        entry = SettingList(None)
        entry.addEntry(
            self.labels[self.DB_NAME],
            default=self.values[self.DB_NAME],
            func=self.changeDbName)

        # フォントサイズ設定項目
        font_sizes = [str(i) for i in range(40)]
        entry.addCombo(
            self.labels[self.FONT_SIZE],
            font_sizes,
            current_index=self.values[self.FONT_SIZE],
            func=self.changefontSize)

        # 履歴表示数設定項目
        self.history_nums = [
            str(i) for i in range(201) if i % 5 == 0 and i != 0
        ]
        his_num = self.history_nums.index(str(self.values[self.HISTORY_NUM]))
        entry.addCombo(
            self.labels[self.HISTORY_NUM],
            self.history_nums,
            current_index=his_num,
            func=self.changeHistoryNum)

        layout.addWidget(entry)

    def callBack(self):
        if not self.callback is None:
            self.callback()

    def changeDbName(self, value):
        self.values[self.DB_NAME] = value
        self.callBack()

    def changefontSize(self, value):
        self.values[self.FONT_SIZE] = value
        self.callBack()

    def changeHistoryNum(self, value):
        self.values[self.HISTORY_NUM] = int(self.history_nums[value])
        self.callBack()

    def getSettings(self):
        settings = [{
            'label': self.labels[self.DB_NAME],
            'value': self.getDBName()
        }, {
            'label': self.labels[self.FONT_SIZE],
            'value': self.getFontSize()
        }, {
            'label': self.labels[self.HISTORY_NUM],
            'value': self.getHistoryNum()
        }]
        return settings

    # 設定取得
    def getDBName(self):
        return self.values[self.DB_NAME]

    def getFontSize(self):
        return self.values[self.FONT_SIZE]

    def getHistoryNum(self):
        return self.values[self.HISTORY_NUM]







# 設定エントリ生成クラス
class SettingList(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QGridLayout(self)

        self.__inputs = []

        self.__rows = 0

    # ラベルとエントリの追加
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

    # ラベルとコンボボックスの追加
    def addCombo(self, text, items, current_index=0, func=None):
        self.layout.addWidget(QLabel(text + ':'), self.__rows, 0)

        cb = QComboBox()
        cb.addItems(items)
        cb.setStyleSheet("QComboBox { combobox-popup: 0; }")
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
