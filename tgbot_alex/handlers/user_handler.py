import json
import asyncio
from aiogram import Router
from aiogram import types
from aiogram import F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from core.utils import set_users_into_gsh, save_data_to_google_sheets
from create_bot import bot
from core import main_chatgpt
from dbase.models import User, History
from dbase.repository import add_user, add_history, user_exists, get_user, update_last_interaction, \
    update_dialog_state, update_dialog_state_and_score, update_dialog_statistics, get_dialog_state, get_num_queries
from keyboards.user_keyboard import drating_inline_buttons_keyboard
from bot import logger
from handlers.admin_handler import ADMIN_CHAT_ID

router = Router()  # [2]

welcome_message = "<b>Добро пожаловать!</b> 🙌🏻 \n\nЯ - полезный помощник, на основе ChatGPT.\nПрофессионал в " \
                  "области Технической поддержки компании Агент5.\nЯ работаю в демонстрационном режиме " \
                  "поэтому у вас есть 10 запросов ко мне.\nСоветую прочитать рекомендации " \
                  "прежде чем начать общаться со мной ➡️ /recommendations.\n\n " \
                  "Мы подготовили несколько примеров вопросов, которые можно задать боту (просто нажми на команду с " \
                  "нужным вопросом):\n" \
                  "/Example1(Привет! Расскажи про ... Что это?)\n" \
                  "/Example2(Что такое ..?)\n" \
                  "/Example3(Как ...?)"


@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    if not await user_exists(message.from_user.id):
        user = User(
            message.from_user.id,
            None,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
            datetime.now(),
            None,
            None,
            None,
            None,
            0,
            "finish",
            0,
            0,
            0
        )
        await add_user(user)
        try:
            set_users_into_gsh()
            logger.info(
                f"Добавили нового user в Google-таблицу!")
        except Exception as error:
            logger.warning(
                f"Ошибка добавления записи Пользователи: {error}")
        await message.reply(welcome_message + "\n\nЗадайте свой вопрос...", parse_mode='HTML')
        await update_dialog_state(message.from_user.id, 'start')
    else:
        if await get_dialog_state(message.from_user.id) == 'close':
            await bot.send_message(message.from_user.id, "Оцените предыдущий ответ чтобы продолжить использование "
                                                         "помощника.")
        else:
            await message.reply(welcome_message + "\n\nЗадайте свой вопрос...", parse_mode='HTML')
            await update_dialog_state(message.from_user.id, 'start')
    dialog_status = await get_dialog_state(message.from_user.id)
    #print(f'user_handler: cmd_start: {dialog_status = }')
    await asyncio.sleep(1)


@router.message(lambda message: asyncio.run(get_dialog_state(message.from_user.id)) == 'close')
async def any_action(message: types.Message):
    await bot.send_message(message.from_user.id, "Оцените предыдущий ответ чтобы продолжить использование помощника.")
    await asyncio.sleep(1)


@router.message(Command(commands=['recommendations']))
async def send_recommendations(message: types.Message):
    """
    This handler will be called when user sends `/recommendations` command
    """
    recommendations_student = '''
    Я - полезный помощник, на основе ChatGPT.
    Профессионал в области Техподдержки Компании Агент5.
    Советую прочитать полностью прежде чем начать общаться со мной.

    1. Сложные вопросы я рекомендую задавать мне на английском языке, так же на английском языке я работаю быстрее.

    2. Будьте конкретны и ясны: задавая вопрос, предоставьте как можно больше релевантной информации, чтобы помочь 
    мне лучше понять, что вам нужно. 

    3. Используйте правильную грамматику и орфографию: так мне будет легче понять ваше сообщение и ответить на него.

    4. Будьте вежливы и корректны в высказываниях: использование вежливых выражений и проявление уважения могут иметь 
    большое значение для обеспечения позитивного взаимодействия. 

    5. Избегайте использования аббревиатур или текстовой речи: это может затруднить мне понимание того, 
    что вы пытаетесь донести. 

    6. Задавайте по одному вопросу за раз: Если у вас есть несколько вопросов, лучше задавать их по одному, 
    чтобы помочь мне дать четкий и целенаправленный ответ. 

    7. Укажите контекст: Если ваш вопрос связан с определенной темой, предоставьте некоторую справочную информацию, 
    которая поможет мне понять, о чем вы спрашиваете. 

    8. Избегайте использования всех заглавных букв: ввод текста всеми заглавными буквами часто воспринимается как 
    крик и может затруднить продуктивную беседу. 

    9. Будьте терпеливы: я являюсь языковой моделью искусственного интеллекта, и мне может понадобиться некоторое 
    время, чтобы обработать ваш запрос. Ответы на некоторые вопросы могут длиться до 2 минут. 

    Готов общаться в чате.
    '''

    await message.reply(recommendations_student, parse_mode='HTML')
    await asyncio.sleep(1)


@router.message(Command(commands=['Example1']))
async def send_question_example1(message: types.Message):
    """
    This handler will be called when user sends `/recommendations` command
    """
    question_example1 = '''
    <b>Вопрос1</b>
    
    Привет!
    Расскажи про ... Что это?
    
    <b>Ответ ChatGPT:</b> 
    Привет! Тут будет ответ 1. 
    '''

    await asyncio.sleep(2)
    await message.reply(question_example1, parse_mode='HTML')


@router.message(Command(commands=['Example2']))
async def send_question_example2(message: types.Message):
    """
    This handler will be called when user sends `/recommendations` command
    """
    question_example2 = '''
    <b>Вопрос2</b>

    Что такое ...?

    <b>Ответ ChatGPT:</b> 
    ... - это основной 
     Тут будет ответ 2'''

    await asyncio.sleep(2)
    await message.reply(question_example2, parse_mode='HTML')


@router.message(Command(commands=['Example3']))
async def send_question_example1(message: types.Message):
    """
    This handler will be called when user sends `/recommendations` command
    """
    question_example3 = '''
    <b>Вопрос3</b>

    Как ... ?
    
    <b>Ответ ChatGPT:</b> Тут будет ответ 3'''

    await asyncio.sleep(2)
    await message.reply(question_example3, parse_mode='HTML')


@router.message(Command(commands=['balance']))
async def send_balance(message: types.Message):
    await asyncio.sleep(1)


@router.message(Command(commands=['context']))
async def reset_context(message: types.Message):
    await asyncio.sleep(1)


@router.callback_query(lambda c: c.data.startswith("drate_"))
async def process_callback_qrating(callback_query: types.CallbackQuery):
    if await get_dialog_state(callback_query.from_user.id) == 'close':
        user = await get_user(callback_query.from_user.id)   # получим из БД информацию о пользователе
        #print(f'process_callback_qrating: {user_data = }')
        # print(f'process_callback_qrating: {score_chuncks = }')
        rating = int(callback_query.data[6:])
        #print(f'process_callback_qrating: {type(rating)}, {rating = }')
        await bot.answer_callback_query(callback_query.id, text=f"Спасибо за вашу оценку: {rating}!", show_alert=True)
        if callback_query.from_user.id in ADMIN_CHAT_ID:
            await bot.send_message(callback_query.from_user.id, f"Спасибо за вашу оценку: {rating}! Можете задать "
                                                                f"следующий вопрос")
        else:
            await bot.send_message(callback_query.from_user.id, f"Спасибо за вашу оценку: {rating}! Можете задать "
                                                                f"следующий вопрос (осталось "
                                                                f"{int(10 - (await get_num_queries(callback_query.from_user.id)))} запрос(ов).")
        # Здесь сохраняется оценка пользователя для дальнейшего анализа или использования
        await update_dialog_state_and_score(callback_query.from_user.id, 'finish', rating)

        # переда записью истории проверим содержимое user_data:
        # for i, item in enumerate(user_data):
        #     print(f'User_data[{i}]. {item}')

        # Запись истории
        history = History(
            callback_query.from_user.id,
            "question",
            "\n".join([f'Пользователь: {user.last_question}', f'Ассистент: {user.last_answer}']),
            user.last_chunks,
            rating,
            user.last_num_token,
            datetime.now(),
            user.last_time_duration
        )

        # переда записью истории проверим содержимое history_data:
        # for i, item in enumerate(history_data):
        #     print(f'history_data[{i}]. {item}')

        await add_history(history)
        try:
            logger.info(
                f"Оценка вопроса! Добаление записи в таблицу Оценка")
            save_data_to_google_sheets('Оценки', history)
        except Exception as error:
            logger.warning(
                f"Ошибка добавления записи Оценки: {error}")
    await bot.answer_callback_query(callback_query.id)
    await asyncio.sleep(1)


@router.message(lambda message: asyncio.run(get_dialog_state(message.from_user.id)) in ['start', 'finish'])
async def generate_answer(message: types.Message):
    #print(f'generate_answer: starting...')
    await update_last_interaction(message.from_user.id, datetime.now())
    num_queries = await get_num_queries(message.from_user.id)
    #print(f'generate_answer: {num_queries = }')
    if num_queries < 10 or message.from_user.id in ADMIN_CHAT_ID:       # ограничение по ответам: менее 10 ответов или админ - неограничено
        try:
            msg = await message.answer("Идет подготовка ответа. Ждите...⏳")  # msg["message_id"]
            time1 = datetime.now()
            logger.info(f"Запрос пошел: {message.text}")
            completion, dialog, chunks = await main_chatgpt.WorkerOpenAI().get_chatgpt_answer(message.text)
            #logger.info(f"Запрос вернулся: {completion}")
            logger.info(f"Запрос вернулся: [completion]")
            #content_to_print = dialog[1]['content']
            #print(f'user_handler: generate_answer: {content_to_print = }')
            #print(f'user_handler: generate_answer: {chunks = }')
            time2 = datetime.now()
            duration = time2 - time1
            await msg.edit_text(completion.choices[0].message.content)
            #logger.info(f"ЦЕНА запроса: {0.0002 * (completion['usage']['total_tokens'] / 1000)}$\n {completion['usage']}")
            logger.info(f"ЦЕНА запроса: {0.004 * (completion['usage']['total_tokens'] / 1000)}$")
            
            last_chunks = '\n '.join([f'\n==  ' + doc.page_content + '\n' for doc in chunks])

            await update_dialog_statistics(
                message.from_user.id, json.dumps(dialog), message.text, completion.choices[0].message.content,
                last_chunks, completion['usage']['total_tokens'], 'close', duration.total_seconds(), num_queries + 1
            )

            await asyncio.sleep(1)
            await message.answer("Пожалуйста, оцените качество консультации от -2 до 2:",
                                 reply_markup=drating_inline_buttons_keyboard())
        except Exception as error:
            logger.warning(
                f"Ошибка генерации: {error}")
            await bot.send_message(message.from_user.id, f"ОШИБКА: {error}")
            await bot.send_message(message.from_user.id, "Модель в настоящее время перегружена. Попробуйте позже.")
    else:
        await bot.send_message(message.from_user.id, "Вы исчерпали всё количество запросов (10) демонстрационного "
                                                     "режима.\nСпасибо что воспользовались нашим Помощником! 🤝")
    await asyncio.sleep(1)


async def generate_algorithm_error(message: types.Message):
    logger.warning(f"Ошибка алгоритма бота. Сообщение пользователя не обработано")
    await message.answer("Извините, сбой в алгоритме Бота: ваше сообщение не обработано")
    await asyncio.sleep(1)
