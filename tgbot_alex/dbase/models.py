from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, BigInteger, Text, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    e_mail = Column(String(320))
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64))
    username = Column(String(32))
    last_interaction = Column(DateTime, nullable=False)
    last_dialog = Column(Text)
    last_question = Column(Text)
    last_answer = Column(Text)
    last_chunks = Column(Text)
    last_num_token = Column(Integer)
    dialog_state = Column(Text, nullable=False, default='finish')
    dialog_score = Column(Integer)
    last_question_time = Column(DateTime)
    last_time_duration = Column(Float)
    num_queries = Column(Integer, default=0)

    def __init__(self, tg_id: int, e_mail: str, first_name: str, last_name: str, username: str, 
                 last_interaction: Optional[datetime] = None, last_dialog: str = None, 
                 last_question: str = None, last_answer: str = None, last_chunks: str = None, 
                 last_num_token: int = None, dialog_state: str = 'finish', 
                 dialog_score: int = None, last_question_time: Optional[datetime] = None,
                 last_time_duration: float = None, num_queries: int = 0) -> None:
        
        self.tg_id = tg_id
        self.e_mail = e_mail
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.last_interaction = last_interaction
        self.last_dialog = last_dialog
        self.last_question = last_question
        self.last_answer = last_answer
        self.last_chunks = last_chunks
        self.last_num_token = last_num_token
        self.dialog_state = dialog_state
        self.dialog_score = dialog_score
        self.last_question_time = last_question_time
        self.last_time_duration = last_time_duration
        self.num_queries = num_queries

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    score_name = Column(Text, nullable=False)
    score_text = Column(Text, nullable=False)
    score_chunk = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    num_token = Column(Integer, nullable=False)
    question_time = Column(DateTime, nullable=False, index=True)
    time_duration = Column(Float, nullable=False)
    score_time = Column(DateTime, nullable=False)

    def __init__(self, user_id: int, question: str = None, answer: str = None, score_name: str = None, score_text: str = None, 
                 score_chunk: str = None, score: int = None, num_token: int = None, 
                 question_time: Optional[datetime] = None, time_duration: float = None, score_time: Optional[datetime] = None) -> None:
        
        self.user_id = user_id
        self.question = question
        self.answer = answer
        self.score_name = score_name
        self.score_text = score_text
        self.score_chunk = score_chunk
        self.score = score
        self.num_token = num_token
        self.question_time = question_time
        self.time_duration = time_duration
        self.score_time = score_time
