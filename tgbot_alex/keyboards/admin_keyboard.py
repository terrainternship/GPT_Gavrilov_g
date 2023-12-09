from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def export_inline_buttons_keyboard() -> InlineKeyboardMarkup:

    # Show the menu with the export button for the admin user
    buttons = [
        [types.InlineKeyboardButton(text="Получить ОТЧЕТ", callback_data="export")]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
