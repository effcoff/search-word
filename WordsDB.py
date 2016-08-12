import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import reconstructor

from DataBase import DataBase


class Words(DataBase.Base):
    __tablename__ = 'words'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    word = sa.Column(sa.String(length=64), unique=True, nullable=False)
    mean = sa.Column(sa.Text, nullable=False)
    created_time = sa.Column(sa.DateTime, default=dt.datetime.now())
    updated_time = sa.Column(sa.DateTime, default=dt.datetime.now(),
                             onupdate=dt.datetime.now())

    @reconstructor
    def initialize(self):
        pass

from datetime import datetime

class WordsDB(DataBase):
    def insert(self, word, mean):
        with self.start_session(commit=True) as s:
            new_data = Words()
            new_data.word = word
            new_data.mean = mean
            new_data.created_time = datetime.now()
            new_data.updated_time = datetime.now()

            s.add(new_data)

    def createWord(self, data):
        return {'word': data.word,
                'mean': data.mean,
                'created_time': data.created_time,
                'updated_time': data.updated_time}

    def deleteWord(self, word):
        with self.start_session(commit=True) as s:
            data = s.query(Words).filter_by(word=word).first()
            if data is None:
                return False

            s.delete(data)
        return True

    def selectAll(self):
        with self.start_session() as s:
            words = s.query(Words).all()
            if len(words) <= 0:
                return None

            datas = [self.createWord(word) for word in words]
        return datas

    def selectWord(self, word):
        with self.start_session() as s:
            data = s.query(Words).filter_by(word=word).first()
            if data is None:
                return None

        return self.createWord(data)


if __name__ == '__main__':
    word_db = WordsDB()
    for i in range(10):
        word_db.insert('word'+str(i), 'test')
    [print(x) for x in word_db.selectAll()]
    print(word_db.selectWord('word'))
    word_db.deleteWord('word')
