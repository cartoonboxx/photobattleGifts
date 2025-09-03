from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from bot.db import *
from bot.models import *
from bot.states import *
from bot.utils import *
from bot.grammatics import *
from bot.keyboards import *
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")

router = Router()


@router.message(CommandStart())
async def startHandler(message: Message, command: CommandStart, bot: Bot):

    args = command.args
    if args and args.startswith("compet"):
        try:
            compet_id = int(args.replace("compet", ""))
        except ValueError:
            await message.answer("❌ Ошибка: некорректный ID")
            return


        async with async_session_maker() as session:
            current_prize = await get_prize_by_id(session, compet_id)
            kb = InlineKeyboardBuilder()
            print(current_prize)
            for channel in current_prize.channels:
                chat_info = await bot.get_chat(chat_id=channel)
                kb.button(text=str(chat_info.username), url=f'https://t.me/{chat_info.username}')

            kb.button(text='Подписался', callback_data=f'subscribed/{current_prize.id}')
            kb.adjust(1)

            if current_prize.channels:
                await message.answer('Перед участием в конкурсе необходимо подписался на каналы',
                                     reply_markup=kb.as_markup())
            else:
                subKb = InlineKeyboardBuilder()
                subKb.button(
                    text='Участвовать в розыгрыше',
                    web_app=WebAppInfo(url=f'https://{HOST}/prize/{compet_id}')
                )
                await message.answer('Для участия нажмите кнопку', reply_markup=subKb.as_markup())

        return

    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Создать конкурс")]], resize_keyboard=True)

    await message.answer(
        "Выберите инструмент:",
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith('subscribed'))
async def subscribedHandlerCheck(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    data = call.data.split("/")
    compet_id = int(data[1])

    async with async_session_maker() as session:  # твой session maker
        current_prize = await get_prize_by_id(session, compet_id)

        not_subscribed = []
        for channel_id in current_prize.channels:
            try:
                member = await bot.get_chat_member(channel_id, user_id)
                if member.status in ("left", "kicked"):
                    not_subscribed.append(channel_id)
            except Exception as e:
                print(f"Ошибка проверки канала {channel_id}: {e}")
                not_subscribed.append(channel_id)

        if not not_subscribed:
            await call.message.edit_text("🎉 Вы успешно подписаны на все каналы!")

            kb = InlineKeyboardBuilder()
            kb.button(
                text='Участвовать в розыгрыше',
                web_app=WebAppInfo(url=f'https://{HOST}/prize/{compet_id}')
            )
            await call.message.answer("Теперь вы можете принять участие:", reply_markup=kb.as_markup())
        else:
            kb = InlineKeyboardBuilder()
            for ch_id in not_subscribed:
                try:
                    chat_info = await bot.get_chat(ch_id)
                    kb.button(text=f"{chat_info.username}", url=f"https://t.me/{chat_info.username}")
                except:
                    kb.button(text=f"Канал {ch_id}", url=f"https://t.me/{ch_id}")
            kb.button(text="Подписался ✅", callback_data=f"subscribed/{compet_id}")
            kb.adjust(1)

            await call.message.edit_text(
                "❌ Вы ещё не подписаны на все каналы. Подпишитесь и нажмите «Подписался» ещё раз:",
                reply_markup=kb.as_markup()
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
    async with async_session_maker() as session:
        prize_id = int(call.data.split('/')[-1])
        current_prize = await get_prize_by_id(session, prize_id)
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

@router.callback_query(F.data == 'continueGiftCreation')
async def continueGiftCreationAddChannels(call: CallbackQuery, state: FSMContext):
    await state.set_state(CreateGiftState.waiting_for_action)
    await state.update_data(channels=[])  # создаем пустой список
    await call.message.edit_text(
        "Добавьте каналы для розыгрыша.\n"
        "Вы можете прикрепить несколько каналов или пропустить этот шаг.",
        reply_markup=get_channel_menu([])
    )

@router.callback_query(F.data == "add_channel", CreateGiftState.waiting_for_action)
async def add_channel_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CreateGiftState.waiting_for_channel)
    await callback.message.edit_text(
        "Отправьте ссылку или юзернейм канала (например, @mychannel или https://t.me/mychannel)\n\nБот должен быть администратором в этом канале"
    )
    await callback.answer()

@router.message(CreateGiftState.waiting_for_channel)
async def receive_channel(message: Message, state: FSMContext):
    try:
        chat = await message.bot.get_chat(message.text.strip())
        channel_id = chat.id

        member = await message.bot.get_chat_member(chat_id=message.text.strip(), user_id=message.bot.id)

        if member.status not in ("administrator", "creator"):
            await message.answer("Бота нет в админах канала ❌\nДобавьте бота и попробуйте снова.")
            return
    except Exception:
        await message.answer("❌ Не удалось получить канал. Проверьте ссылку или юзернейм. Убедитесь в том, что бот находится в админах канала")
        return

    data = await state.get_data()
    channels = data.get("channels", [])
    if channel_id not in channels:
        channels.append(channel_id)
        await state.update_data(channels=channels)

    await state.set_state(CreateGiftState.waiting_for_action)
    await message.answer(
        f"✅ Канал добавлен: {chat.title} ({channel_id})",
        reply_markup=get_channel_menu(channels)
    )

@router.callback_query(F.data == "next_step", CreateGiftState.waiting_for_action)
async def next_step_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    channels = data.get("channels", [])
    await state.update_data(channels=list(set(channels)))
    await continueGiftCreationHandler(callback, state)


async def continueGiftCreationHandler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("<b>[1/3] Введите размер приза:</b>")
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
    channels = data['channels']

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
        kb.button(text="Принять участие", url=f"https://t.me/testgiftsBotbot_bot?start=compet{0}")
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

        async with async_session_maker() as session:
            current_prize = await add_prize(session, prize, channelLink, winnersCount, duration, send_message.message_id, channels)

        new_kb = InlineKeyboardBuilder()
        new_kb.button(text="Принять участие", url=f"https://t.me/testgiftsBotbot_bot?start=compet{current_prize.id}")
        new_kb.adjust(1)

        await bot.edit_message_reply_markup(
            chat_id=channelLink,
            message_id=send_message.message_id,
            reply_markup=new_kb.as_markup()
        )


    except Exception as e:
        await message.answer(f"Не удалось отправить сообщение в канал ❌\nОшибка: {e}")

# -- user handlers --



