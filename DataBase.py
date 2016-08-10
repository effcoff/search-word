import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import reconstructor, sessionmaker
from contextlib import contextmanager
import datetime as dt

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

class Words(DataBase.Base):
    __tablename__ = 'words'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    word = sa.Column(sa.String(length=64), unique=True, nullable=False)
    mean = sa.Column(sa.Binary, nullable=False)
    created_time = sa.Column(sa.DateTime, default=dt.datetime.now())
    updated_time = sa.Column(sa.DateTime, default=dt.datetime.now(),
                             onupdate=dt.datetime.now())

    @reconstructor
    def initialize(self):
        pass

if __name__ == '__main__':
    db = DataBase(echo=False)

    with db.start_session(commit=True) as session:
        word = Words()
        word.word = 'Test'
        data = ['data', 'data']
        import pickle
        dump = pickle.dumps(data)
        word.mean =  dump
        session.add(word)

    with db.start_session(commit=True) as session:
        word = Words()
        word.word = 'aaaa'
        data = ['data', 'data']
        import pickle
        dump = pickle.dumps(data)
        word.mean =  dump
        session.add(word)

    with db.start_session() as session:
        words = session.query(Words).order_by(sa.desc(Words.created_time)).all()
        print(words[0].word)
        data = pickle.loads(words[0].mean)
        [print(x) for x in data]

    with db.start_session() as session:
        words = session.query(Words).filter_by(word='Test')
        print(words[0].word)
