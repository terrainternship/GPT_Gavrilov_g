from sqlalchemy import Column, Integer, String, create_engine, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_TYPE
from create_bot import POSTGRE_HOST, POSTGRE_DB, POSTGRE_USER, POSTGRE_PASSW

#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine(f'postgresql://{POSTGRE_USER}:{POSTGRE_PASSW}@{POSTGRE_HOST}/{POSTGRE_DB}')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    e_mail = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    last_interaction = Column(String)
    last_dialog = Column(String)
    last_question = Column(String)
    last_answer = Column(String)
    last_num_token = Column(Float)
    dialog_state = Column(String, default='finish')
    dialog_score = Column(Integer, default=0)
    last_time_duration = Column(Float)
    num_queries = Column(Integer, default=0)

    def __init__(self, user_data):
        """
        Создаем нового пользователя в таблице
        :param user_data:
        :return:
        """
        self.user_id = user_data[0]
        self.e_mail = user_data[1]
        self.first_name = user_data[2]
        self.last_name = user_data[3]
        self.username = user_data[4]
        self.last_interaction = user_data[5]
        self.last_dialog = user_data[6]
        self.last_question = user_data[7]
        self.last_answer = user_data[8]
        self.last_num_token = user_data[9]
        self.dialog_state = user_data[10]
        self.dialog_score = user_data[11]
        self.last_time_duration = user_data[12]
        self.num_queries = user_data[13]


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    score_name = Column(String)
    score_text = Column(String)
    score = Column(Integer)
    num_token = Column(Integer)
    date_estimate = Column(String)
    time_duration = Column(Float)

    def __init__(self, history_data):
        self.user_id = history_data[0]
        self.score_name = history_data[1]
        self.score_text = history_data[2]
        self.score = history_data[3]
        self.num_token = history_data[4]
        self.date_estimate = history_data[5]
        self.time_duration = history_data[6]

# Создание таблицы
Base.metadata.create_all(engine)
