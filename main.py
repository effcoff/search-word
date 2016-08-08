import lxml.html
import requests
import re
import pickle
import io
import sys
import DataBase as db

class WordSerach:
    def __init__(self, dbname):
        self.target_url = 'http://www.weblio.jp/content/'
        self.cssselect = '.kiji .NetDicHead, .kiji .NetDicBody'
        self.cssselect += ', .kiji .midashigo, .kiji .Jtnhj'

        self.css = []
        self.css.append('.kiji .NetDicHead, .kiji .NetDicBody')
        self.css.append('.kiji .midashigo, .kiji .Jtnhj')

        self.db = db.DataBase(dbname)

    def getMean(self, word):
        url = self.target_url + word
        target_html = requests.get(url).text

        root = lxml.html.fromstring(target_html)
        texts = ''
        for css in self.css:
            data = root.cssselect(css)
            if len(data) <= 0:
                continue
            texts = [texts.text_content() for texts in root.cssselect(css)]
            break
        return '@'.join(texts)

    def insertDB(self, word):
        mean = self.getMean(word)
        result = re.sub('\s', '', mean)
        result = re.sub('[①-⑳]', '@', result).split('@')
        dump_reuslt = pickle.dumps(result)

        with self.db.start_session(commit=True) as s:
            words = db.Words()
            words.word = word
            words.mean = dump_reuslt
            s.add(words)

        self.word = word

    def deleteWord(self, word=None):
        with self.db.start_session(commit=True) as s:
            if word is None:
                word = self.word
            delete_column = s.query(db.Words).filter_by(word=word).first()
            s.delete(delete_column)

    def readWord(self, word):
        with self.db.start_session() as s:
            data = s.query(db.Words).filter_by(word=word)
            data = list(data)
        return pickle.loads(data[0].mean)


    def readAllWord(self):
        with self.db.start_session() as s:
            datas = s.query(db.Words).all()
            datas = list(datas)
            datas = [[data.word, pickle.loads(data.mean)] for data in datas]
        return  datas


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors='replace')

    wordSearch = WordSerach('sqlite:///word.db')
    line = None
    while True:
        print('< 終了する場合は q を入力してください。 >')
        print('< 検索する言葉を入力してください。 >')
        line = input()
        if line == 'q':
            print('----- 検索終了 -----')
            break
        elif line == 'd':
            while True:
                word = wordSearch.word
                print('< {} を削除しますか？ [t/f] >'.format(word))
                d_line = input()
                if d_line == 't':
                    wordSearch.deleteWord()
                    break
                elif d_line == 'f':
                    break
            continue
        elif line == 'all':
            datas = wordSearch.readAllWord()
            for data in datas:
                print(data[0])
                [print(x) for x in data[1]]
                print('')
            continue

        wordSearch.insertDB(line)
        datas = wordSearch.readWord(line)
        for data in datas:
            print(data)
        word = wordSearch.word
        print('\n< [{}] を削除したい場合は、 d を入力してください。 >'.format(word))
