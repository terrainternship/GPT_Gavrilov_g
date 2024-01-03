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

CHEAP_MODEL = 'gpt-3.5-turbo'
EXPENSIVE_MODEL = 'gpt-3.5-turbo-16k'
TEMPERATURE = 0.01

# Промты
SYSTEM_PROMT_FILE = 'system_promt.txt'
USER_PROMT = "Analyze and use these tips in your answer: {}. Give a detailed correct answer to the Client's question: {}\nAnswer:"

# папки и пути
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))   # Корневой каталог
LOG_PATH = 'logs'               # хранение логов
FAISS_DB_DIR = 'faiss_indexes'  # хранение индексов
TXT_DB_DIR = 'txt_docs'
SETTINGS_PATH = 'settings'      # хранение внешних настроек, промтов

# Настройки логирования:
LOGGING_SERVICE = "gavrilov_bot"

# путь до внешней папки с настройками уведомлений TG_bot
APPRISE_CONFIG_PATH = "settings/apprise.yml"

# Настройка БД
RECREATE_DB = False  # удаляем ли старые таблицы при запуске бота (обновляем структуры таблицы, но теряем данные)
DB_TYPE = 'POSTGRE'
#DB_TYPE = 'SQLite3'

