import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime,Float,BigInteger
from datetime import datetime

Base = declarative_base()


class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    describtion = Column(String(250))
    marketcap = Column(BigInteger, nullable=False)
    web = Column(String(50))
    reddit = Column(String(50))
    github = Column(String(50))
    telegram = Column(String(50))


class RedditInfo(Base):
    __tablename__ = 'reddit_info'
    # Here we define columns
    id = Column(Integer, primary_key=True)
    url = Column(String(50), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    subscribers = Column(Integer)
    online = Column(Integer)
    timedelta_mean = Column(Float)
    timedelta_std = Column(Float)
    comment_mean = Column(Float) #average comment
    comment_std = Column(Float)
    vote_mean = Column(Float)
    vote_std = Column(Float)
    topic_id = Column(Integer, ForeignKey('topic.id'))
    topic = relationship(Topic)


if __name__ == "__main__":
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
    engine = create_engine('sqlite:///bigdata.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
    Base.metadata.create_all(engine)