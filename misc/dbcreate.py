import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime,Float,BigInteger
from datetime import datetime
'''
Thie script creates an empty DB for crypto info
'''
Base = declarative_base()


class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    symbol = Column(String(10))
    describtion = Column(String(250))
    marketcap = Column(BigInteger, nullable=False)
    web = Column(String(100))
    reddit = Column(String(100))
    github = Column(String(100))
    telegram = Column(String(100))
    discord = Column(String(100))
    twitter = Column(String(100))
    facebook = Column(String(100))
    linkedin = Column(String(100))
    wechat = Column(String(100))
    youtube = Column(String(100))


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