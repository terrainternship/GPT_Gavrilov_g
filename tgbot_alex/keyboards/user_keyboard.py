from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def drating_inline_buttons_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=str(i), callback_data=f"drate_{i}") for i in range(-2, 3)],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


