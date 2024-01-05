from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import SYSTEM_PROMPT_FILE, FAISS_DB_DIR

load_dotenv(override=True)

TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GSERVICEACCOUNTFILE = os.getenv("GSERVICEACCOUNTFILE")
SHEETID_PARAM = os.getenv("SHEETID_PARAM")

POSTGRE_HOST=os.getenv('POSTGRE_HOST')
POSTGRE_DB=os.getenv('POSTGRE_DB')
POSTGRE_USER=os.getenv('POSTGRE_USER')
POSTGRE_PASSW=os.getenv('POSTGRE_PASSW')
POSTGRE_PORT=os.getenv('POSTGRE_PORT')


#SYSTEM_PROMPT_FILE = os.getenv("SYSTEM_PROMPT_FILE")
#FAISS_DB_DIR = os.getenv("FAISS_DB_DIR")
storage = MemoryStorage()

bot = Bot(token=TOKEN, parse_mode=None)
dp = Dispatcher(storage=storage)


