from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_channel_menu(channels: list[int]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="➕ Добавить канал", callback_data="add_channel")]
    ]
    if channels:
        buttons.append([InlineKeyboardButton(text="➡️ Далее", callback_data="next_step")])
    else:
        buttons.append([InlineKeyboardButton(text="⏭ Пропустить", callback_data="next_step")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)