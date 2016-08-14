import datetime as dt
from contextlib import contextmanager

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import reconstructor, sessionmaker


class DataBase:
    Base = declarative_base()

    def __init__(self, dburl='sqlite:///:memory:', checkfirst=True, echo=False):
        engine = sa.create_engine(dburl, echo=echo)
        self.Base.metadata.create_all(engine, checkfirst=checkfirst)

        self.Session = sessionmaker(bind=engine, autocommit=False)

    @contextmanager
    def start_session(self, commit=False):
        session = None
        try:
            session = self.Session()
            try:
                yield session
                if commit:
                    session.commit()
            except:
                session.rollback()
                raise
        finally:
            if session is not None:
                session.close()


if __name__ == '__main__':
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


    db = DataBase(echo=False)


    def print_words(word):
        print('{}   {}  {}  {}'.format(word.word, word.mean,
                                       word.created_time, word.updated_time))


    with db.start_session(commit=True) as session:
        word = Words()
        word.word = 'Test'
        word.mean = 'data'
        session.add(word)

    with db.start_session(commit=True) as session:
        word = Words()
        word.word = 'aaaa'
        word.mean = 'data'
        session.add(word)

    with db.start_session(commit=True) as session:
        words = session.query(Words).filter_by(word='Test').first()
        words.mean = 'lkjsdf'

    with db.start_session() as session:
        words = session.query(Words).order_by(sa.desc(Words.created_time)).all()
        for word in words:
            print_words(word)

    with db.start_session() as session:
        words = session.query(Words).filter_by(word='Test').first()
        print_words(word)
