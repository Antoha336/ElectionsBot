import uuid

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Poll(Base):
    __tablename__ = 'Poll'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    slug = Column(String, default=uuid.uuid4().__str__())
    name = Column(String, nullable=False, default='Без названия')
    status = Column(String, default="Created")
    is_anonymous = Column(Boolean, nullable=False, default=False)
    is_public = Column(Boolean, nullable=False, default=True)
    can_retract_vote = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, nullable=False)

    options = relationship('Option', back_populates='poll', cascade='all, delete, delete-orphan')
    votes = relationship('Vote', back_populates='poll', cascade='all, delete, delete-orphan')


class Option(Base):
    __tablename__ = 'Option'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False)
    poll_id = Column(Integer, ForeignKey('Poll.id'), nullable=False)

    poll = relationship('Poll', back_populates='options')
    votes = relationship('Vote', back_populates='option', cascade='all, delete, delete-orphan')


class Vote(Base):
    __tablename__ = 'Vote'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_name = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    option_id = Column(Integer, ForeignKey('Option.id'), nullable=False)
    poll_id = Column(Integer, ForeignKey('Poll.id'), nullable=False)

    # Связь с Option и Poll
    option = relationship('Option', back_populates='votes')
    poll = relationship('Poll', back_populates='votes')


engine = create_engine(f'sqlite:///src/database/polls.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
