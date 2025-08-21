from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession

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


# -------- CRUD-функции --------

# Получить всех пользователей
async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()

# Получить все призы
async def get_all_prizes(session: AsyncSession):
    result = await session.execute(select(Prize))
    return result.scalars().all()

# Добавить пользователя
async def add_user(session: AsyncSession, telegram_id: int, username: str = None, prize_id: int = None):
    user = User(telegram_id=telegram_id, username=username, prize_id=prize_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

# Добавить приз
async def add_prize(session: AsyncSession, prize_size: str, channel_link: str, winners_count: int, duration_minutes: int):
    prize = Prize(
        prize_size=prize_size,
        channel_link=channel_link,
        winners_count=winners_count,
        duration_minutes=duration_minutes,
    )
    session.add(prize)
    await session.commit()
    await session.refresh(prize)
    return prize
