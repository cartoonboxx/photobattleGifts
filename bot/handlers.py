from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from models import *

router = Router()

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Создать конкурс")],
    ],
    resize_keyboard=True
)

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Выберите инструмент:",
        reply_markup=main_keyboard
    )



@router.message(lambda message: message.text == "Создать конкурс")
async def create_raffle_handler(message: Message):
    prizes = await get_all_prizes()
    kb = InlineKeyboardBuilder()
    for prize in prizes:
        kb.button(text=f'TG STARS - {prize.prize_size}', callback_data=f"{prize.channel_link}")
    kb.button(text='Создать розыгрыш', callback_data='createNewGift')
    kb.adjust(1)
    await message.answer("Доступные конкурсы", reply_markup=kb.as_markup())
