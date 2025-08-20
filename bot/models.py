from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Prize(Base):
    __tablename__ = "prizes"

    id = Column(Integer, primary_key=True, index=True)
    prize_size = Column(String, nullable=False)
    channel_link = Column(String, nullable=False)
    winners_count = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    users = relationship("User", back_populates="prize")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    prize_id = Column(Integer, ForeignKey("prizes.id"))

    prize = relationship("Prize", back_populates="users")
