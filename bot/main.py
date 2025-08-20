import asyncio
import logging
import os
from contextlib import suppress

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from db import engine, Base
from handlers import router

logging.basicConfig(level=logging.INFO)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
print('bot', BOT_TOKEN)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def on_startup():
    # создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await on_startup()
    with suppress(Exception):
        await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
