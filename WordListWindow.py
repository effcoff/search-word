from PyQt5.QtWidgets import *
from common import *

from WordsDB import WordsDB


class WordListWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        wordlist_widget = WordListWidget()
        self.setCentralWidget(wordlist_widget)


class WordListWidget(WordList):
    def __init__(self):
        super().__init__()

        h_layout = QHBoxLayout()
        self.setLayout(h_layout)

        # 単語リストレイアウト
        wordlist_frame = ListFrame(self)
        h_layout.addWidget(wordlist_frame)

        # 右の表示ボックス
        self.box = self.createResultBox()
        h_layout.addWidget(self.box)

        self.initWordList()

    def initWordList(self):
        datas = self.getWords(WordsDB())
        print(datas)
        self.list_items = []
        if not datas is None:
            self.list_items = [(item[self.WORD], item[self.UPDATE_TIME])
                          for item in datas]
        self.initList(self.list_items)



class ListFrame(QFrame):
    def __init__(self, wordlist):
        super().__init__()

        # 単語リストレイアウト
        list_layout = QVBoxLayout()
        self.setLayout(list_layout)

        self.wordlist = wordlist
        # タイトル
        self.title = wordlist.createTitle('単語リスト', 18)
        list_layout.addWidget(self.title)

        # 単語リスト
        self.list = TreeList(None)
        self.list = wordlist.createList(2, ['単語', '日時'])
        list_layout.addWidget(self.list)

        #ボタン
        self.btn = QPushButton('削除')
        self.btn.clicked.connect(self.deleteWord)
        list_layout.addWidget(self.btn)

    def deleteWord(self):
        values = self.wordlist.getSelectedValues()
        if values is None:
            return False

        word = values[self.wordlist.WORD]
        db = WordsDB()
        res = db.deleteWord(word)
        if res is False:
            print('not delete word:{}'.format(word))
            return False

        print('deleted:{}'.format(word))

        self.wordlist.initWordList()




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = WordListWindow()
    win.show()

    sys.exit(app.exec_())
