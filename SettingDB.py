from DataBase import DataBase
import sqlalchemy as sa
import pickle


class Settings(DataBase.Base):
    __tablename__ = 'settings'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    setting = sa.Column(sa.Binary, nullable=False)


class SettingsDB(DataBase):
    def __init__(self):
        super().__init__(dburl='sqlite:///settings.st')
        self.initInsert()

    def initInsert(self):
        if self.isInit() is False:
            return
        with self.start_session(commit=True) as s:
            setting = Settings()
            datas = {'dbname': ':memory:',
                     'fontsize': 12,
                     'history_num': 10}

            dump_data = pickle.dumps(datas)
            setting.setting = dump_data
            s.add(setting)
        print('init settings database end!!')

    def updateSettings(self, dbname, fontsize, history_num):
        datas = {
            'dbname': dbname,
            'fontsize': fontsize,
            'history_num': history_num
        }
        dump_data = pickle.dumps(datas)
        with self.start_session(commit=True) as s:
            data = s.query(Settings).first()
            data.setting = dump_data

    def isInit(self):
        with self.start_session() as s:
            words = s.query(Settings).all()
            if len(words) <= 0:
                return True

        return False

    def getSettings(self):
        with self.start_session() as s:
            data = s.query(Settings).first()
            if data is None:
                return None

            return pickle.loads(data.setting)


if __name__ == '__main__':
    db = SettingsDB()
    print(db.getSettings())
