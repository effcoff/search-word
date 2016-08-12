import re

import lxml.html
import requests

import WordsDB as db


class WordSerach:
    def __init__(self, **kwargs):
        self.target_url = 'http://www.weblio.jp/content/'
        self.cssselect = '.kiji .NetDicHead, .kiji .NetDicBody'
        self.cssselect += ', .kiji .midashigo, .kiji .Jtnhj'

        self.css = []
        self.css.append('.kiji .NetDicHead, .kiji .NetDicBody')
        self.css.append('.kiji .midashigo, .kiji .Jtnhj')

        self.db = db.DataBase(**kwargs)
        self.word_db = db.WordsDB()
        self.history_datas = []
        self.getHistory()

    def getMean(self, word):
        url = self.target_url + word
        target_html = requests.get(url).text

        root = lxml.html.fromstring(target_html)
        texts = None
        for css in self.css:
            data = root.cssselect(css)
            if len(data) <= 0:
                continue
            texts = [texts.text_content() for texts in root.cssselect(css)]
            break

        # 複数取れた場合は改行
        mean = '\n'.join(texts)
        # 複数意味がある場合は、①のように順番になっているので、改行に変更
        mean = re.sub('[①-⑳]', '\n', mean)

        return mean

    def addHistory(self, data):
        tmp_data = [data]
        if len(self.history_datas) >= 1:
            print('aaa')
            self.history_datas = [h for h in self.history_datas if h['word'] != tmp_data[0]['word']]
            tmp_data.extend(self.history_datas)

        self.history_datas = tmp_data

    def insertDB(self, word):
        mean = self.getMean(word)
        data = self.word_db.insert(word, mean)
        self.addHistory(data)

        self.word = word

    def deleteWord(self, word=None):
        if word is None:
            word = self.word

        res = self.word_db.deleteWord(word)
        if res is False:
            print('{}は、保存されていません。'.format(word))

    def getWord(self, word):
        res = self.word_db.selectWord(word)

        if res is None:
            print('{}は、保存されていません。'.format(word))
            return None

        return res

    def getAllWord(self):
        res = self.word_db.selectAll()

        if res is None:
            print('単語が一つも登録されていません。')
            return None

        return res

    def getHistory(self, count=None):
        if len(self.history_datas) <= 0:
            res = self.word_db.selectAllOrderByUpdatedDesc()

            if res is None:
                print('履歴が一つも登録されていません。')
                return None

            self.history_datas = res
        return self.history_datas


if __name__ == '__main__':
    ws = WordSerach()

    print(ws.getHistory())
    ws.getMean('逡巡')
    ws.insertDB('逡巡')
    ws.insertDB('神妙')
    ws.insertDB('逡巡')
    print(len(ws.getHistory()))
    ws.deleteWord('逡巡')
    print(ws.getWord('逡巡'))
