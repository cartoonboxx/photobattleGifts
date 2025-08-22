from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db import Base
from bot.utils import return_end_time_string, add_minutes

class Prize(Base):
    __tablename__ = "prizes"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    prize_size = Column(Integer, nullable=False)
    channel_link = Column(String, nullable=False)
    winners_count = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    telegram_post_id = Column(Integer, nullable=False)
    isFinished = Column(Boolean, default=False, nullable=False)

    users = relationship("User", back_populates="prize", cascade="all, delete-orphan")



class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    prize_id = Column(Integer, ForeignKey("prizes.id"))

    prize = relationship("Prize", back_populates="users")

async def get_all_prizes(session: AsyncSession):
    result = await session.execute(select(Prize))
    return result.scalars().all()

async def get_prize_by_id(session: AsyncSession, prize_id: int):
    result = await session.execute(select(Prize).where(Prize.id == prize_id))
    prize = result.scalar_one_or_none()
    return prize


async def add_prize(session: AsyncSession, prize_size: int, channel_link: str, winners_count: int, duration_minutes: int, telegram_post_id: str | int):
    prize = Prize(
        prize_size=prize_size,
        channel_link=channel_link,
        winners_count=winners_count,
        duration_minutes=duration_minutes,
        telegram_post_id=telegram_post_id,
        created=add_minutes(0),
        isFinished=False
    )
    session.add(prize)
    await session.commit()
    await session.refresh(prize)
    return prize

async def delete_prize_by_id(session: AsyncSession, prize_id: int):
    result = await session.execute(select(Prize).where(Prize.id == prize_id))
    prize = result.scalar_one_or_none()

    if prize is None:
        raise ValueError(f"Prize с id {prize_id} не найден")

    await session.delete(prize)
    await session.commit()

    return True

async def set_marker_to_prize(session: AsyncSession, prize_id: int):
    result = await session.execute(select(Prize).where(Prize.id == prize_id))
    prize = result.scalar_one_or_none()

    if prize is None:
        raise ValueError(f"Prize with id {prize_id} not found")

    prize.isFinished = True

    await session.commit()
    await session.refresh(prize)

    return prize


async def add_user(session: AsyncSession, telegram_id: int, username: str = None, prize_id: int = None):
    user = User(telegram_id=telegram_id, username=username, prize_id=prize_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()
