from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from db import *
from models import *
from states import *
from utils import *

router = Router()


@router.message(CommandStart())
async def startHandler(message: Message):

    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Создать конкурс")]], resize_keyboard=True)

    await message.answer(
        "Выберите инструмент:",
        reply_markup=keyboard
    )

@router.message(lambda message: message.text == "Создать конкурс")
async def showGiftsAllHandler(message: Message):
    async with async_session_maker() as session:
        prizes = await get_all_prizes(session)
        kb = InlineKeyboardBuilder()
        for prize in prizes:
            kb.button(text=f'TG STARS - {prize.prize_size}', callback_data=f"{prize.channel_link}")
        kb.button(text='Создать розыгрыш', callback_data='createNewGift')
        kb.adjust(1)
        await message.answer("Доступные конкурсы", reply_markup=kb.as_markup())

@router.callback_query(F.data == "createNewGift")
async def createNewGiftHandler(call: CallbackQuery, state: FSMContext):
    await call.message.answer("<b>Пришлите ссылку на канал, в котором нужно создать розыгрыш</b>\n\nБот должен быть адимнистратором")
    await state.set_state(CreateGiftState.channelLink)


@router.message(CreateGiftState.channelLink)
async def processChannelLink(message: Message, state: FSMContext, bot: Bot):
    raw = message.text or ""
    chat_ref = normalize_channel_ref(raw)

    if not chat_ref:
        await message.answer(
            "Нужна публичная ссылка вида:\n"
            "`https://t.me/<username>` или `@username`.\n"
            "Инвайт-ссылки (`joinchat`, `+...`) не подходят для проверки.",
            parse_mode="Markdown"
        )
        return

    try:
        member = await bot.get_chat_member(chat_id=chat_ref, user_id=bot.id)

        if member.status not in ("administrator", "creator"):
            await message.answer("Бота нет в админах канала ❌\nДобавьте бота и попробуйте снова.")
            return

        await state.update_data(channelLink=chat_ref)

        kb = InlineKeyboardBuilder()
        kb.button(text="Продолжить", callback_data="continueGiftCreation")

        await message.answer("Канал успешно добавлен ✅", reply_markup=kb.as_markup())

    except Exception:
        await message.answer(
            "Бота нет в админах канала ❌\n"
            "Проверьте, что канал публичный и бот добавлен в администраторы, затем попробуйте снова."
        )


@router.callback_query(F.data == "continueGiftCreation")
async def continueGiftCreationHandler(call: CallbackQuery, state: FSMContext):
    await call.message.answer("[1/3] Введите размер приза:")
    await state.set_state(CreateGiftState.prizeSize)


@router.message(CreateGiftState.prizeSize)
async def setPrizeSizeHandler(message: Message, state: FSMContext):
    await state.update_data(prizeSize=message.text)
    await message.answer("[2/3] Введите количество победителей:")
    await state.set_state(CreateGiftState.winnersCount)


@router.message(CreateGiftState.winnersCount)
async def setWinnersCountHandler(message: Message, state: FSMContext):
    await state.update_data(winnersCount=message.text)
    await message.answer("[3/3] Введите длительность розыгрыша в минутах:")
    await state.set_state(CreateGiftState.durationMinutes)


@router.message(CreateGiftState.durationMinutes)
async def setDurationMinutesHandler(message: Message, state: FSMContext):
    await state.update_data(durationMinutes=message.text)
    data = await state.get_data()

    await message.answer(
        f"Розыгрыш создан:\n"
        f"Канал: {data['channelLink']}\n"
        f"Приз: {data['prizeSize']}\n"
        f"Победителей: {data['winnersCount']}\n"
        f"Время: {data['durationMinutes']} минут"
    )

    await state.clear()

# @dp.message(Command("start"))
# async def cmd_start(message: Message):
#     async with async_session_maker() as session:
#         user = await add_user(session, telegram_id=message.from_user.id, username=message.from_user.username)
#         await message.answer(f"Привет, {user.username or 'незнакомец'}! Ты добавлен в базу ✅")
#
#
# # 📌 Проверка списка пользователей
# @dp.message(Command("users"))
# async def cmd_users(message: Message):
#     async with async_session_maker() as session:
#         users = await get_all_users(session)
#         text = "👥 Пользователи:\n" + "\n".join([f"{u.id}: {u.username or u.telegram_id}" for u in users])
#         await message.answer(text if users else "В базе пока пусто.")
