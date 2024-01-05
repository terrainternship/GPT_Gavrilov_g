from datetime import datetime, timedelta
from typing import List, Optional, Tuple
import pandas as pd
from sqlalchemy import select, update
from config import MAX_DIALOG_PERIOD_IN_HOURS
from dbase.database import connect_db
from dbase.models import User, History


async def add_user(user: User) -> None:
    """
    Добавляет нового пользователя в базу данных.

    :param user: Объект пользователя, который будет добавлен в базу данных.
    """
    async with await connect_db() as session:
        session.add(user)
        await session.commit()

async def add_history(history: History) -> None:
    """
    Добавляет новую запись истории в базу данных.

    :param history: Объект истории, который будет добавлен в базу данных.
    """
    async with await connect_db() as session:
        session.add(history)
        await session.commit()

async def user_exists(tg_user_id: int) -> bool:
    """
    Проверяет, существует ли пользователь с заданным идентификатором.

    :param tg_user_id: Идентификатор пользователя в Telegram.
    :return: True, если пользователь существует, иначе False.
    """
    return await get_user(tg_user_id) is not None

async def get_user(tg_user_id: int) -> Optional[User]:
    """
    Получает пользователя по его идентификатору.

    :param tg_user_id: Идентификатор пользователя в Telegram.
    :return: Объект пользователя или None, если пользователь не найден.
    """
    async with await connect_db() as session:
        result = await session.execute(select(User).filter(User.tg_id == tg_user_id))
        return result.scalar_one_or_none()
    
async def get_user_id(tg_user_id: int) -> Optional[User]:
    """
    Получает идентификатор пользователя по его идентификатору в Telegram.

    :param tg_user_id: Идентификатор пользователя в Telegram.
    :return: Идентификатор пользователя или None, если пользователь не найден.
    """
    async with await connect_db() as session:
        result = await session.execute(select(User.id).where(User.tg_id == tg_user_id))
        return result.scalar_one_or_none()

async def update_last_question_time(tg_user_id: int, last_question_time: datetime) -> None:
    """
    Обновляет информацию о времени последнего вопроса пользователя.

    :param tg_user_id: Идентификатор пользователя в Telegram.
    :param last_question_time: Время последнего вопроса пользователя.
    """
    async with await connect_db() as session:
        stmt = update(User).where(User.tg_id == tg_user_id).values(last_question_time=last_question_time)
        await session.execute(stmt)
        await session.commit()

async def update_last_interaction(tg_user_id: int, last_interaction: datetime) -> None:
    """
    Обновляет информацию о последнем взаимодействии пользователя.

    :param tg_user_id: Идентификатор пользователя в Telegram.
    :param last_interaction: Время последнего взаимодействия.
    """
    async with await connect_db() as session:
        stmt = update(User).where(User.tg_id == tg_user_id).values(last_interaction=last_interaction)
        await session.execute(stmt)
        await session.commit()

async def update_dialog_state(tg_user_id: int, dialog_state: str) -> None:
    """
    Обновляет состояние диалога пользователя.

    :param tg_user_id: Идентификатор пользователя в Telegram.
    :param dialog_state: Новое состояние диалога.
    """
    async with await connect_db() as session:
        stmt = update(User).where(User.tg_id == tg_user_id).values(dialog_state=dialog_state)
        await session.execute(stmt)
        await session.commit()

async def update_dialog_state_and_score(tg_user_id: int, dialog_state: str, dialog_score: int) -> None:
    """
    Обновляет состояние диалога пользователя и его баллы.

    :param tg_user_id: Идентификатор пользователя в Telegram.
    :param dialog_state: Новое состояние диалога.
    :param dialog_score: Новое количество баллов.
    """
    async with await connect_db() as session:
        stmt = update(User).where(User.tg_id == tg_user_id).values(dialog_state=dialog_state, dialog_score=dialog_score)
        await session.execute(stmt)
        await session.commit()

async def update_dialog_statistics(
        tg_user_id: int, last_dialog: str, last_question: str,
        last_answer: str, last_chunks: str, last_num_token: int,
        dialog_state: str, last_time_duration: float, num_queries: int) -> None:
    """
    Обновляет статистику диалога пользователя.

    :param tg_user_id: Идентификатор пользователя в Telegram.
    :param last_dialog: Последний диалог пользователя.
    :param last_question: Последний вопрос пользователя.
    :param last_answer: Последний ответ пользователя.
    :param last_chunks: Последние чанки диалога пользователя.
    :param last_num_token: Количество токенов в последнем сообщении пользователя.
    :param dialog_state: Состояние диалога пользователя.
    :param last_time_duration: Длительность последнего взаимодействия.
    :param num_queries: Количество запросов пользователя.
    """
    async with await connect_db() as session:
        stmt = update(User).where(User.tg_id == tg_user_id).values(
            last_dialog=last_dialog, last_question=last_question,
            last_answer=last_answer, last_chunks=last_chunks,
            last_num_token=last_num_token, dialog_state=dialog_state,
            last_time_duration=last_time_duration, num_queries=num_queries)
        await session.execute(stmt)
        await session.commit()

async def get_dialog_state(tg_user_id: int) -> Optional[str]:
    """
    Получает состояние диалога пользователя.

    :param tg_user_id: Идентификатор пользователя в Telegram.
    :return: Состояние диалога пользователя или None, если информация отсутствует.
    """
    async with await connect_db() as session:
        result = await session.execute(select(User.dialog_state).where(User.tg_id == tg_user_id))
        return result.scalar_one_or_none()

async def get_num_queries(tg_user_id: int) -> Optional[int]:
    """
    Получает количество запросов пользователя.

    :param tg_user_id: Идентификатор пользователя в Telegram.
    :return: Количество запросов пользователя или None, если информация отсутствует.
    """
    async with await connect_db() as session:
        result = await session.execute(select(User.num_queries).where(User.tg_id == tg_user_id))
        return result.scalar_one_or_none()

async def get_all_users() -> List[User]:
    """
    Получает список всех пользователей из базы данных.

    :return: Список объектов пользователей.
    """
    async with await connect_db() as session:
        result = await session.execute(select(User))
        return result.scalars().all()
    
async def get_history_for_dialog(user_id: int) -> List[History]:
    """
    Получает список записей истории для формировния диалога.

    :param user_id: Идентификатор пользователя.
    :return: Список объектов истории.
    """
    async with await connect_db() as session:
        result = await session.execute(select(History).where(
            History.user_id == user_id,
            History.question_time >= datetime.utcnow() - timedelta(hours=MAX_DIALOG_PERIOD_IN_HOURS)
        ).order_by(History.question_time))

        return result.scalars().all()

async def get_df_users() -> pd.DataFrame:
    """
    Получает список всех пользователей из базы данных в виде DataFrame.

    :return: DataFrame с информацией о пользователях.
    """
    async with await connect_db() as session:
        result = await session.execute(select(User))
        return pd.DataFrame(result.mappings().all())

async def get_df_history() -> pd.DataFrame:
    """
    Получает список всех записей истории из базы данных в виде DataFrame.

    :return: DataFrame с записями истории.
    """
    async with await connect_db() as session:
        result = await session.execute(select(History))
        return pd.DataFrame(result.mappings().all())
