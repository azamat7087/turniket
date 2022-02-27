import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
SQL_ALCHEMY_DATABASE_URL = f"postgresql://root:root@localhost/turniket"


engine = create_engine(SQL_ALCHEMY_DATABASE_URL,)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class ChildActivities(Base):
    __tablename__ = "child_activities"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(length=100), nullable=False,)
    db_id = Column(Integer, nullable=False, unique=True)
    arrive_time = Column(String(length=200), nullable=False)
    leaving_time = Column(String(length=200), nullable=False)
    is_send = Column(Boolean, default=False)
    date_of_add = Column('date_of_add', DateTime, default=datetime.datetime.now, nullable=False)
    date_of_update = Column('date_of_update', DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now, nullable=False)
    parents = relationship("Parents", back_populates="child")


class Parents(Base):

    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    telegram_id = Column(String(length=70), nullable=False, unique=True)
    is_activated = Column(Boolean, default=False)
    username = Column(String(length=200), nullable=True, default="Аноним")
    child_id = Column(Integer, ForeignKey("child_activities.id"), nullable=True)
    date_of_add = Column('date_of_add', DateTime, default=datetime.datetime.now, nullable=False)
    date_of_update = Column('date_of_update', DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now, nullable=False)

    child = relationship("ChildActivities", back_populates="parents")


