from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from WordSearch import WordSerach
from SettingsWindow import SettingsWindow

from common import *
from WordListWindow import WordListWindow


class History(WordList):
    def __init__(self, parent, ws):
        super().__init__(parent)

        self.setMinimumWidth(250)

        layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.ws = ws

        # タイトル
        self.title = self.createTitle('履歴', 18)
        layout.addWidget(self.title)

        # リスト設定
        self.list = self.createList(2, ['単語', '日時'])
        layout.addWidget(self.list)

        # 意味表示ボックス
        self.box = self.createResultBox()
        layout.addWidget(self.box)

        self.initHistoryList()

    def initHistoryList(self):
        datas = self.getWords(self.ws.word_db)
        if not datas is None:
            list_items = [(item[self.WORD], item[self.UPDATE_TIME])
                          for item in self.items]
            self.initList(list_items)


class MainWidget(QWidget):
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

        self.history.initHistoryList()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        main_widget = MainWidget()
        self.setCentralWidget(main_widget)

        self.statusBar().showMessage('Ready')

        self.setMenuBar()

    def setMenuBar(self):
        exit_action = QAction('&終了', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit search word')
        exit_action.triggered.connect(qApp.quit)

        setting_action = QAction('&設定', self)
        setting_action.setShortcut('Ctrl+Alt+S')
        setting_action.setStatusTip('Setting search word')
        setting_action.triggered.connect(self.showSettingsWindow)

        wordlist_action = QAction('&単語一覧', self)
        wordlist_action.setShortcut('Ctrl+Alt+S')
        wordlist_action.setStatusTip('Setting search word')
        wordlist_action.triggered.connect(self.showWordList)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(setting_action)
        file_menu.addAction(wordlist_action)
        file_menu.addAction(exit_action)

    def showSettingsWindow(self):
        settings_win = SettingsWindow(self)
        settings_win.show()
        print('showshow')

    def showWordList(self):
        wordlist_win = WordListWindow(self)
        wordlist_win.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
