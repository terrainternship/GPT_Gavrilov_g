from aiogram import Router
from aiogram import types
from aiogram.filters.command import Command
import asyncio
import os
from create_bot import bot, SHEETID_PARAM
from core.utils import get_report, set_report_into_gsh
from keyboards.admin_keyboard import export_inline_buttons_keyboard

router = Router()  # [1]

# добавляй админов тут:
ADMIN_CHAT_ID = [
    412539319, 1612759951 # el_prosto
]


@router.message(Command(commands=["ourCommand"]))
async def cmd_start(message: types.Message):
    if message.from_user.id in ADMIN_CHAT_ID:
        await message.answer(f"Отчет доступен в GoogleSheets по ссылке: "
                             f"https://docs.google.com/spreadsheets/d/{SHEETID_PARAM}/edit?usp=drive_link"
                             f"\n\nДля экспорта данных в чат нажмите на кнопку: ",
                             reply_markup=export_inline_buttons_keyboard())


@router.callback_query(lambda callback_query: callback_query.data == "export")
async def callback_export(callback_query: types.CallbackQuery):
    report_name = get_report()
    await bot.answer_callback_query(callback_query.id)
    doc = types.input_file.FSInputFile(path=report_name, filename=report_name)
    await callback_query.message.answer_document(doc)
    try:
        os.remove(report_name)
    except Exception as e:
        print(f'Ошибка удаления отчета {e}')

