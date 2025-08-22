from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from bot.db import *
from bot.models import *
from bot.states import *
from bot.utils import *
from bot.grammatics import *

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
            kb.button(text=f'TG STARS - {prize.prize_size}', callback_data=f"checkPrize/{prize.id}")
        kb.button(text='Создать розыгрыш', callback_data='createNewGift')
        kb.adjust(1)
        await message.answer("Доступные конкурсы", reply_markup=kb.as_markup())

@router.callback_query(F.data.startswith('checkPrize'))
async def checkPrizeHandler(call: CallbackQuery):
    print("hell")
    async with async_session_maker() as session:
        prize_id = int(call.data.split('/')[-1])
        print(prize_id)
        current_prize = await get_prize_by_id(session, prize_id)
        print(current_prize)
        kb = InlineKeyboardBuilder()
        kb.button(text='Ссылка на розыгрыш', url='https://google.com')
        kb.button(text='🗑 Удалить розыгрыш', callback_data=f'deletePrize/{prize_id}')
        kb.button(text='◀️ Назад', callback_data='backToShowGiftsAllHandler')
        kb.adjust(1)

        until_time = get_time_until_event(current_prize.created, current_prize.duration_minutes)
        await call.message.answer(text=f'<b>TG STARS - {current_prize.prize_size}</b>\n\n'
                                       f'Завершается через {until_time["minutes"]} минут {until_time["seconds"]} секунд',
                                  reply_markup=kb.as_markup())
        await call.message.delete()

@router.callback_query(F.data.startswith('deletePrize'))
async def deletePrizeHandler(call: CallbackQuery):
    async with async_session_maker() as session:

        prize_id = int(call.data.split('/')[-1])
        await delete_prize_by_id(session, prize_id)

        await backToShowGiftsAllHandler(call)

@router.callback_query(F.data == "createNewGift")
async def createNewGiftHandler(call: CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.button(text='◀️ Назад', callback_data='backToShowGiftsAllHandler')
    kb.adjust(1)
    await call.message.answer("<b>Пришлите ссылку на канал, в котором нужно создать розыгрыш</b>"
                              "\n\nБот должен быть адимнистратором",
                              reply_markup=kb.as_markup())
    await call.message.delete()
    await state.set_state(CreateGiftState.channelLink)

@router.callback_query(F.data == 'backToShowGiftsAllHandler')
async def backToShowGiftsAllHandler(call: CallbackQuery):
    await showGiftsAllHandler(call.message)
    await call.message.delete()


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
    await call.message.answer("<b>[1/3] Введите размер приза:</b>")
    await call.message.delete()
    await state.set_state(CreateGiftState.prizeSize)


@router.message(CreateGiftState.prizeSize)
async def setPrizeSizeHandler(message: Message, state: FSMContext):
    await state.update_data(prizeSize=message.text)
    await message.answer("<b>[2/3] Введите количество победителей:</b>")
    await state.set_state(CreateGiftState.winnersCount)


@router.message(CreateGiftState.winnersCount)
async def setWinnersCountHandler(message: Message, state: FSMContext):
    await state.update_data(winnersCount=message.text)
    await message.answer("<b>[3/3] Введите длительность розыгрыша в минутах:</b>")
    await state.set_state(CreateGiftState.durationMinutes)


@router.message(CreateGiftState.durationMinutes)
async def setDurationMinutesHandler(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(durationMinutes=message.text)
    data = await state.get_data()

    channelLink = data['channelLink']
    prize = int(data['prizeSize'])
    winnersCount = int(data['winnersCount'])
    duration = int(data['durationMinutes'])

    await message.answer(
        f"Розыгрыш создан:\n"
        f"Канал: {data['channelLink']}\n"
        f"Приз: {data['prizeSize']}\n"
        f"Победителей: {data['winnersCount']}\n"
        f"Время: {data['durationMinutes']} минут"
    )

    await state.clear()

    try:
        kb = InlineKeyboardBuilder()
        kb.button(text="Принять участие", url="https://google.com")
        kb.adjust(1)

        photo = FSInputFile("images/gift.jpg")

        send_message = await bot.send_photo(
            chat_id=channelLink,
            photo=photo,
            caption=(
                f"🎁 Раздача {prize} TG STARS 🌟 для {winnersCount} {decline_participant('победител', winnersCount)}. "
                f"Каждому победителю по {prize // winnersCount} TG STARS 🌟"
                f"\n\nНажмите кнопку «Принять участие» и ожидайте объявления победителя "
                f"в {return_end_time_string(duration)} по МСК (через {duration} минут)."
            ),
            reply_markup=kb.as_markup()
        )

        print(send_message, send_message.message_id)
        async with async_session_maker() as session:
            await add_prize(session, prize, channelLink, winnersCount, duration, send_message.message_id)

    except Exception as e:
        await message.answer(f"Не удалось отправить сообщение в канал ❌\nОшибка: {e}")
