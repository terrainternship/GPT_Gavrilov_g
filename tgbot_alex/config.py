"""
Настройки параметров и переменных проекта для разработчика.
Файл будет храниться во внутренней папке Docker,
доступа извне не будет в отличие от папки Settings.

В папке Settings должна быть проброшена из Docker в систему,
чтобы хранящиеся там переменные, можно было обновлять налету.

Так же и папка FAISS_DB_DIR должна быть проброшена из Docker в систему,
чтобы хранящиеся там индексы, можно было добавлять боту налету.
"""
import os

# Модели
CHEAP_MODEL = 'gpt-3.5-turbo'
EXPENSIVE_MODEL = 'gpt-3.5-turbo-1106'
# Используемая модель
MODEL = EXPENSIVE_MODEL
# Максимальное количество токенов модели
MAX_TOKEN_LIMIT = 16385
# Зарезервированное количество токенов для ответа
MAX_TOKENS_FOR_ANSWER = 2048
# Максимальное количество токенов для запроса к ChatGPT с учетом резерва для ответа
MAX_TOKENS_FOR_REQUEST = MAX_TOKEN_LIMIT - MAX_TOKENS_FOR_ANSWER
# Максимальная длительность диалога в часах
MAX_DIALOG_PERIOD_IN_HOURS = 24
# Температура 
TEMPERATURE = 0.01

# Максимальная длина сообщения в Telegram
TELEGRAM_MAX_MESSAGE_LENGTH = 4096

# Промпты
SYSTEM_PROMPT_FILE = 'system_prompt.txt'
USER_PROMPT_FILE = 'user_prompt.txt'

# папки и пути
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))   # Корневой каталог
LOG_PATH = 'logs'               # хранение логов
FAISS_DB_DIR = 'faiss_indexes'  # хранение индексов
TXT_DB_DIR = 'txt_docs'
SETTINGS_PATH = 'settings'      # хранение внешних настроек, промптов

# Настройки логирования:
LOGGING_SERVICE = "aio_3"

# путь до внешней папки с настройками уведомлений TG_bot
APPRISE_CONFIG_PATH = "settings/apprise.yml"

# Настройка БД
RECREATE_DB = False  # удаляем ли старые таблицы при запуске бота (обновляем структуры таблицы, но теряем данные)
DB_TYPE = 'POSTGRE'
#DB_TYPE = 'SQLite3'

