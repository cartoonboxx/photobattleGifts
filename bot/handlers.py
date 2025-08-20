from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from models import *

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать розыгрыш")]
        ],
        resize_keyboard=True
    )

    await message.answer("Выберите инструмент:", reply_markup=keyboard)


@router.message(lambda message: message.text == "Создать розыгрыш")
async def create_raffle_handler(message: Message):

    await message.answer("Доступные команды:\n/start - запуск\n/help - помощь")
