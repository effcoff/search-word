import datetime as dt
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import reconstructor

from DataBase import DataBase
from VersionDB import VersionDB


class History(DataBase.Base):
    __tablename__ = 'history'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    word = sa.Column(sa.String(length=64), nullable=False)
    mean = sa.Column(sa.Text, nullable=False)
    created_time = sa.Column(sa.DateTime, default=dt.datetime.now())

    ID = 'id'
    WORD = 'word'
    MEAN = 'mean'
    CREATED_TIME = 'created_time'

    def __init__(self):
        pass

    @reconstructor
    def initialize(self):
        pass


class HistoryDB(DataBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checkVer()

    def checkVer(self):
        dbname = 'history'
        ver = '1.1'

        version_db = VersionDB(dburl='sqlite:///version.db')
        version_db.insert(dbname)
        version_db.updateLatestVer(dbname, ver)
        res = version_db.checkVersion(dbname)

        if res is False:
            datas = self.selectAll()
            History.__table__.drop(self.engine)
            print('{} database deleted!!'.format(dbname))
            version_db.updateSameVer(dbname)
            History.__table__.create(self.engine)
            if datas is None:
                return None
            [self.insertWithData(data) for data in datas]
            print('{} database created!!'.format(dbname))

    def insert(self, word, mean):
        with self.start_session(commit=True) as s:
            # 新しい単語を登録
            new_data = History()
            new_data.word = word
            new_data.mean = mean
            new_data.created_time = datetime.now()
            s.add(new_data)

            return self.createDic(new_data.word,
                                  new_data.mean,
                                  new_data.created_time)

    def insertWithData(self, data):
        with self.start_session(commit=True) as s:
            # 新しい単語を登録
            new_data = History()
            new_data.word = data[History.WORD]
            new_data.mean = data[History.MEAN]
            new_data.created_time = data[History.CREATED_TIME]
            s.add(new_data)

    def createDic(self, word, mean, created_time):
        return {History.WORD: word,
                History.MEAN: mean,
                History.CREATED_TIME: created_time}

    def createHistoryDic(self, data):
        return self.createDic(data.word,
                              data.mean,
                              data.created_time)

    def deleteHistory(self, id):
        with self.start_session(commit=True) as s:
            data = s.query(History).filter_by(id=id).first()
            if data is None:
                return False

            s.delete(data)
        return True

    def selectAll(self):
        with self.start_session() as s:
            histories = s.query(History).order_by(History.id).all()
            if len(histories) <= 0:
                return None

            datas = [self.createHistoryDic(history) for history in histories]
            return datas

    def selectAllOrderByUpdatedDesc(self, limit=-1):
        with self.start_session() as s:
            histories = s.query(History).order_by(sa.desc(History.created_time)).limit(limit).all()
            if len(histories) <= 0:
                return None

            datas = [self.createHistoryDic(history) for history in histories]
            return datas

    def selectWord(self, id):
        with self.start_session() as s:
            data = s.query(History).filter_by(id=id).first()
            if data is None:
                return None

            return self.createHistoryDic(data)


if __name__ == '__main__':
    history_db = HistoryDB(dburl='sqlite:///test.db')
    for i in range(10):
        history_db.insert('word' + str(i), 'test')

    [print(x) for x in history_db.selectAll()]
    print(history_db.selectWord(1))
    history_db.deleteHistory(1)
