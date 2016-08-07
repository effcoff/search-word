import lxml.html
import requests
import re
import sqlite3
import pickle
import io
import sys

class WordSerach:
    def __init__(self, db_name=':memory:'):
        self.target_url = 'http://www.weblio.jp/content/'
        self.cssselect = '.kiji .NetDicHead, .kiji .NetDicBody'
        self.cssselect += ', .kiji .midashigo, .kiji .Jtnhj'

        self.css = []
        self.css.append('.kiji .NetDicHead, .kiji .NetDicBody')
        self.css.append('.kiji .midashigo, .kiji .Jtnhj')

        self.dbname = db_name
        self.conn = None

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

    def startDB(self):
        self.conn = sqlite3.connect(self.dbname)

    def dbCursor(self):
        if self.conn is None:
            print('not connect db: {}'.format(self.dbname))
            exit()

        return self.conn.cursor()

    def createDB(self):
        c = self.dbCursor()

        sql = 'CREATE TABLE word (id integer primary key autoincrement, word text, mean blob)'
        c.execute(sql)

        sql = 'CREATE TABLE dual (id integer)'
        c.execute(sql)
        sql = 'INSERT INTO dual values (1)'
        c.execute(sql)

        self.conn.commit()
        c.close()

    def insertDB(self, word):
        mean = self.getMean(word)
        result = re.sub('\s', '', mean)
        result = re.sub('[①-⑳]', '@', result).split('@')
        dump_reuslt = pickle.dumps(result)

        c = self.dbCursor()

        c.execute('INSERT INTO word (word, mean) SELECT :word, :mean from dual '
                  'WHERE NOT EXISTS (SELECT "X" FROM word WHERE word = :word)',
                  (word, sqlite3.Binary(dump_reuslt)))

        self.conn.commit()
        c.close()

        self.word = word

    def deleteWord(self, word=None):
        c = self.dbCursor()

        if word is None:
            word = self.word

        c.execute('DELETE FROM word WHERE word = :word',
                  (word,))

        self.conn.commit()
        c.close()

    def readWord(self, word):
        c = self.dbCursor()

        c.execute('SELECT mean from word WHERE word = :word',
                  (word,))

        data = [pickle.loads(row[0]) for row in c]
        c.close()
        return data

    def readAllWord(self):
        c = self.dbCursor()

        c.execute('SELECT word, mean FROM word')

        data = [{'word': row[0], 'mean': pickle.loads(row[1])} for row in c]

        c.close()

        return data


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors='replace')

    wordSearch = WordSerach('word.db')
    wordSearch.startDB()
    # wordSearch.createDB()
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
            data = wordSearch.readAllWord()
            for x in data:
                print(x['word'])
                [print(mean) for mean in x['mean']]
                print('\n')
            continue

        wordSearch.insertDB(line)
        data = wordSearch.readWord(line)[0]
        [print(x) for x in data]
        word = wordSearch.word
        print('\n< [{}] を削除したい場合は、 d を入力してください。 >'.format(word))
