from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    e_mail = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    username = Column(Text)
    last_interaction = Column(DateTime)
    last_dialog = Column(Text)
    last_question = Column(Text)
    last_answer = Column(Text)
    last_chunks = Column(Text)
    last_num_token = Column(Integer)
    dialog_state = Column(Text, default='finish')
    dialog_score = Column(Integer)
    last_time_duration = Column(Float)
    num_queries = Column(Integer, default=0)

    def __init__(self, user_id: int, e_mail: str, first_name: str, last_name: str, username: str, 
                 last_interaction: Optional[datetime] = None, last_dialog: str = '', 
                 last_question: str = '', last_answer: str = '', last_chunks: str = '', 
                 last_num_token: int = 0, dialog_state: str = 'finish', 
                 dialog_score: int = 0, last_time_duration: float = 0.0, 
                 num_queries: int = 0) -> None:
        
        self.user_id = user_id
        self.e_mail = e_mail
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.last_interaction = last_interaction or datetime.now()
        self.last_dialog = last_dialog
        self.last_question = last_question
        self.last_answer = last_answer
        self.last_chunks = last_chunks
        self.last_num_token = last_num_token
        self.dialog_state = dialog_state
        self.dialog_score = dialog_score
        self.last_time_duration = last_time_duration
        self.num_queries = num_queries

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    score_name = Column(Text)
    score_text = Column(Text)
    score_chunk = Column(Text)
    score = Column(Integer)
    num_token = Column(Integer)
    date_estimate = Column(DateTime)
    time_duration = Column(Float)

    def __init__(self, user_id: int, score_name: str = '', score_text: str = '', 
                 score_chunk: str = '', score: int = 0, num_token: int = 0, 
                 date_estimate: Optional[datetime] = None, time_duration: float = 0.0) -> None:
        
        self.user_id = user_id
        self.score_name = score_name
        self.score_text = score_text
        self.score_chunk = score_chunk
        self.score = score
        self.num_token = num_token
        self.date_estimate = date_estimate or datetime.now()
        self.time_duration = time_duration
