import sqlalchemy as sa
from sqlalchemy.orm import reconstructor

from DataBase import DataBase


class Version(DataBase.Base):
    __tablename__ = 'version'
    db_name = sa.Column(sa.String(length=64), primary_key=True)
    now_ver = sa.Column(sa.String(length=64), nullable=False, default='1')
    latest_ver = sa.Column(sa.String(length=64), nullable=False, default='1')

    @reconstructor
    def initialize(self):
        pass


class VersionDB(DataBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def insert(self, dbname):
        with self.start_session(commit=True) as s:
            if self.checkFirst(dbname) is False:
                return None

            new_data = Version()
            new_data.db_name = dbname

            s.add(new_data)

    def checkData(self, dbname, data):
        if data is None:
            print('db:{} not exists!!'.format(dbname))
            return None

        return True

    def checkFirst(self, dbname):
        with self.start_session() as s:
            data = s.query(Version).filter_by(db_name=dbname).first()
            if not data is None:
                return False

            return True

    def checkVersion(self, dbname):
        with self.start_session() as s:
            data = s.query(Version).filter_by(db_name=dbname).first()
            if self.checkData(dbname, data) is None:
                return None

            if data.now_ver == data.latest_ver:
                return True

            return False

    def updateNowVer(self, dbname, ver):
        with self.start_session(commit=True) as s:
            data = s.query(Version).filter_by(db_name=dbname).first()
            if self.checkData(dbname, data) is None:
                return False

            data.now_ver = ver
            return True

    def updateLatestVer(self, dbname, ver):
        with self.start_session(commit=True) as s:
            data = s.query(Version).filter_by(db_name=dbname).first()
            if self.checkData(dbname, data) is None:
                return None

            data.latest_ver = ver
            return True

    def updateSameVer(self, dbname):
        with self.start_session(commit=True) as s:
            data = s.query(Version).filter_by(db_name=dbname).first()
            if self.checkData(dbname, data) is None:
                return None

            data.now_ver = data.latest_ver


if __name__ == '__main__':
    db = VersionDB()
    db.insert('words')
    db.insert('history')

    db.updateLatestVer('words', '1.1')
    db.updateSameVer('words')

    print(db.checkVersion('words'))
