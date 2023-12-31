import asyncio
import logging
from logger.logger import logger    # импортируем свой Логгер из папки logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from core.utils import set_users_into_gsh
from handlers import user_handler, admin_handler
from create_bot import dp, bot
from dbase.database import init_db, create_db

#logger = logging.getLogger(__name__)      # старый логгер

# # Запускаем логирование
# logger = Logger(enable_notifications=False)
logger.info("Start bot")


#Настройка логирования в stdout
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
#     # filename="bot_log.log",
#     # filemode='a',
# )


async def on_startup(_):
    logger.info('Бот вышел в онлайн')


# Запуск бота
async def main():
    logger.info(f"Starting main")

    await create_db()

    dp.include_router(admin_handler.router)
    logger.info(f"Router ADMIN is started")
    dp.include_router(user_handler.router)
    logger.info(f"Router USER is started")

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    scheduler = AsyncIOScheduler(time_zone="Europe/Moscow")
    scheduler.add_job(set_users_into_gsh, trigger='interval', minutes=10, start_date=datetime.now())
    scheduler.start()
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == "__main__":
    init_db()
    asyncio.run(main())
