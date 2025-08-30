from aiogram.fsm.state import StatesGroup, State

class CreateGiftState(StatesGroup):
    channelLink = State()
    prizeSize = State()
    winnersCount = State()
    durationMinutes = State()
    waiting_for_action = State()
    waiting_for_channel = State()