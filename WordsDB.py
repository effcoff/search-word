import datetime as dt
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import reconstructor

from DataBase import DataBase
from VersionDB import VersionDB


class Words(DataBase.Base):
    __tablename__ = 'words'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    word = sa.Column(sa.String(length=64), unique=True, nullable=False)
    mean = sa.Column(sa.Text, nullable=False)
    created_time = sa.Column(sa.DateTime, default=dt.datetime.now())
    updated_time = sa.Column(sa.DateTime, default=dt.datetime.now(),
                             onupdate=dt.datetime.now())

    ID = 'id'
    WORD = 'word'
    MEAN = 'mean'
    CREATED_TIME = 'created_time'
    UPDATED_TIME = 'updated_time'

    @reconstructor
    def initialize(self):
        pass


class WordsDB(DataBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checkVer()

    def checkVer(self):
        dbname = 'words'
        ver = '1.1'

        version_db = VersionDB(dburl='sqlite:///version.db')
        version_db.insert(dbname)
        version_db.updateLatestVer(dbname, ver)
        res = version_db.checkVersion(dbname)

        if res is False:
            datas = self.selectAll()
            Words.__table__.drop(self.engine)
            print('{} database deleted!!'.format(dbname))
            version_db.updateSameVer(dbname)
            Words.__table__.create(self.engine)
            if datas is None:
                return None
            [self.insertWithData(data) for data in datas]
            print('{} database created!!'.format(dbname))

    def insert(self, word, mean):
        with self.start_session(commit=True) as s:
            # 既に単語が登録されていたら、更新日時を更新して終了
            res = self.updateTimeWithWord(word)
            if not res is False:
                return res

            # 新しい単語を登録
            new_data = Words()
            new_data.word = word
            new_data.mean = mean
            new_data.created_time = datetime.now()
            new_data.updated_time = datetime.now()
            s.add(new_data)

            return self.createDic(new_data.word,
                                  new_data.mean,
                                  new_data.created_time,
                                  new_data.updated_time)

    def insertWithData(self, data):
        with self.start_session(commit=True) as s:
            # 新しい単語を登録
            new_data = Words()
            new_data.word = data[Words.WORD]
            new_data.mean = data[Words.MEAN]
            new_data.created_time = data[Words.CREATED_TIME]
            new_data.updated_time = data[Words.UPDATED_TIME]
            s.add(new_data)

    def createDic(self, word, mean, created_time, updated_time):
        return {'word': word,
                'mean': mean,
                'created_time': created_time,
                'updated_time': updated_time}

    def createWordDic(self, data):
        return self.createDic(data.word,
                              data.mean,
                              data.created_time,
                              data.updated_time)

    def deleteWord(self, word):
        with self.start_session(commit=True) as s:
            data = s.query(Words).filter_by(word=word).first()
            if data is None:
                return False

            s.delete(data)
        return True

    def selectAll(self):
        with self.start_session() as s:
            words = s.query(Words).order_by(Words.id).all()
            if len(words) <= 0:
                return None

            datas = [self.createWordDic(word) for word in words]
            return datas

    def selectAllOrderByUpdatedDesc(self, limit=40):
        with self.start_session() as s:
            words = s.query(Words).order_by(sa.desc(Words.updated_time)).limit(limit).all()
            if len(words) <= 0:
                return None

            datas = [self.createWordDic(word) for word in words]
            return datas

    def selectWord(self, word):
        with self.start_session() as s:
            data = s.query(Words).filter_by(word=word).first()
            if data is None:
                return None

            return self.createWordDic(data)

    def updateTimeWithWord(self, word):
        with self.start_session(commit=True) as s:
            data = s.query(Words).filter_by(word=word).first()
            if data is None:
                return False

            data.updated_time = datetime.now()
            return self.createWordDic(data)


if __name__ == '__main__':
    word_db = WordsDB()
    for i in range(10):
        word_db.insert('word' + str(i), 'test')

    word_db.updateTimeWithWord('word4')

    [print(x) for x in word_db.selectAll()]
    print(word_db.selectWord('word1'))
    word_db.deleteWord('word')
