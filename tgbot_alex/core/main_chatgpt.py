import asyncio
import sys
from typing import Any, Dict, List
from dbase.models import History
from logger.logger import logger
from config import ROOT_DIR, SETTINGS_PATH, FAISS_DB_DIR, SYSTEM_PROMPT_FILE, USER_PROMPT_FILE, MODEL, TEMPERATURE, \
    MAX_TOKENS_FOR_REQUEST, MAX_TOKENS_FOR_ANSWER, TELEGRAM_MAX_MESSAGE_LENGTH
from create_bot import OPENAI_API_KEY
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from openai import AsyncOpenAI
import tiktoken
import re
import os


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
faiss_db_dir = os.path.join(ROOT_DIR, FAISS_DB_DIR)
os.chdir(faiss_db_dir)


class WorkerOpenAI:
    def __init__(self, faiss_db_dir=faiss_db_dir, list_indexes=None, mod=MODEL):
        # старт инициализации промптов
        system_prompt_file = os.path.join(ROOT_DIR, SETTINGS_PATH, SYSTEM_PROMPT_FILE)
        try:
            with open(system_prompt_file, 'r', encoding='utf-8') as file:
                system_prompt = file.read()
                #system_prompt = system_prompt.format(max_tokens = MAX_TOKENS_FOR_ANSWER, max_characters = TELEGRAM_MAX_MESSAGE_LENGTH)
                logger.info(f'(Прочитали system_prompt)')
        except Exception as e:
            print(f'Ошибка чтения system_prompt: {e}')

        user_prompt_file = os.path.join(ROOT_DIR, SETTINGS_PATH, USER_PROMPT_FILE)
        try:
            with open(user_prompt_file, 'r', encoding='utf-8') as file:
                user_prompt = file.read()
                logger.info(f'(Прочитали user_prompt)')
        except Exception as e:
            print(f'Ошибка чтения user_prompt: {e}')
        # конец инициализации промптов

        # Составим список всех индексов в папке faiss_db_dir:
        # print(f'Ищем список курсов: {faiss_db_dir}')
        if list_indexes is None:
            list_indexes = []
            for folder in os.listdir(faiss_db_dir):
                if os.path.isdir(os.path.join(faiss_db_dir, folder)):
                    list_indexes.append(os.path.basename(folder))
        #print(f'__init__: Нашли базы: {list_indexes}')

        self.model = mod
        self.list_indexes = list_indexes
        # системные настройки
        self.chat_manager_system = system_prompt
        self.chat_manager_user = user_prompt

        def create_search_index_old(db_path, indexes):
            flag = True
            # Перебор всех курсов в списке courses:
            # print(f'Старт create_search_index: {indexes =}')
            count_base = 0  # сосчитаем количество курсов
            for index_file in indexes:
                index_path = os.path.join(db_path, index_file)      # получаем полный путь к курсу
                # print(f'create_search_index - ищем индекс {count_base}: {index_file =}, {index_path =}')
                try:
                    # print(f'Пройдемся внутри папки {db_path =}:')
                    for current_base in os.listdir(db_path):    # Перебор всех баз данных в курсе
                        # print(f'Пройдемся внутри папки {db_path =}:')
                        count_base += 1
                        if flag:
                            # Если flag равен True, то загружается база данных FAISS из файла curr_base в папке index_path
                            path_to_current_base = os.path.join(index_path, current_base)
                            db = FAISS.load_local(index_path, OpenAIEmbeddings())
                            flag = False
                        else:
                            # Иначе происходит объединение баз данных FAISS
                            pass
                            #db.merge_from(FAISS.load_local(index_path, OpenAIEmbeddings()))

                    # print(f'Создали индекс {db =}')
                except Exception as e:
                    logger.error(f'1. Ошибка чтения индексов: {e}')
                    sys.exit(777)
            return db

        def create_search_index(indexes):
            """
                Чтение индексов из всех индексных файлов
                :param path: локальный путь в проекте до папки с индексами
                :return: база индексов
                """
            db_path = os.path.join(ROOT_DIR, FAISS_DB_DIR)
            flag = True  # Признак первой базы для чтения. Остальные базы будем добавлять к имеющейся
            # Перебор всех курсов в списке courses:
            # print(f'Старт read_faiss_indexes: {indexes =}')
            count_base = 0  # сосчитаем количество курсов
            for index_file in indexes:
                index_path = os.path.join(db_path, index_file)  # получаем полный путь к курсу
                # print(f'read_faiss_indexes - ищем индекс {count_base}: {index_file =}, {index_path =}')
                count_base += 1
                if flag:
                    # Если flag равен True, то создается база данных FAISS из папки index_path
                    db = FAISS.load_local(index_path, OpenAIEmbeddings())
                    flag = False
                    # print(f'read_faiss_indexes: прочитали новый индекс')
                else:
                    # Иначе происходит объединение баз данных FAISS
                    db.merge_from(FAISS.load_local(index_path, OpenAIEmbeddings()))
                    # print(f'read_faiss_indexes: Добавили в индекс')
            return db

        # Если База данных embedding уже создана ранее
        # print(f'Проверим путь до базы знаний: {faiss_db_dir}')
        if faiss_db_dir:
            # print(f'{os.getcwd() = }')
            # print("Ищем готовую базу данных. Путь: ", faiss_db_dir)
            # print("Курсы: ", self.list_indexes)
            self.search_index = create_search_index(self.list_indexes)

        self.client = AsyncOpenAI(
            api_key=OPENAI_API_KEY
        )

    # пример подсчета токенов
    # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    def num_tokens_from_messages(self, messages: List[Dict[str, str]]) -> int:
        """Return the number of tokens used by a list of messages."""
        model = self.model
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if model in {
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-3.5-turbo-1106",
            "gpt-4-0314",
            "gpt-4-32k-0314",
            "gpt-4-0613",
            "gpt-4-32k-0613",
            }:
            tokens_per_message = 3
            tokens_per_name = 1
        elif model == "gpt-3.5-turbo-0301":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif "gpt-3.5-turbo" in model:
            print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-1106.")
            return self.num_tokens_from_messages(messages)
        elif "gpt-4" in model:
            print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
            return self.num_tokens_from_messages(messages)
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
            )
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

    async def get_chatgpt_answer(self, topic: str, history_items: List[History]):
        # Выборка документов по схожести с вопросом
        docs = await self.search_index.asimilarity_search(topic, k=8)
        #print(f'get_chatgpt_answer: {docs}')
        doc_chunks = re.sub(r'\n{2}', ' ', '\n '.join(
            [f'\n==  ' + doc.page_content + '\n' for i, doc in enumerate(docs)]))
        
        system_prompt = self.chat_manager_system.format(
            max_tokens = MAX_TOKENS_FOR_ANSWER,
            max_characters = TELEGRAM_MAX_MESSAGE_LENGTH,
            doc_chunks=doc_chunks
        )

        user_prompt = self.chat_manager_user.format(topic=topic, doc_chunks=doc_chunks)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        messages = self.add_previous_messages(messages, history_items)

        # TODO: добавить вторую более дешевую модель. Выбирать модель в зависимости от объема передаваемого user_prompt
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=TEMPERATURE
        )

        #print(f'{completion["usage"]["total_tokens"]} токенов использовано всего (вопрос-ответ).')
        #print('ЦЕНА запроса с ответом :', 0.004*(completion.usage.total_tokens/1000), ' $')
        #print('===========================================: \n')
        #print('Ответ ChatGPT: ')
        #print(completion.choices[0].message.content)
        return completion, messages, docs
    
    def add_previous_messages(self, messages: List[Dict[str, str]], history_items: List[History]) -> List:
        new_messages = []

        new_messages.append(messages[0])

        for item in history_items:
            new_messages.append({"role": "user", "content": item.question})
            new_messages.append({"role": "assistant", "content": item.answer})

        new_messages.append(messages[1])

        num_tokens = self.num_tokens_from_messages(new_messages)
        while num_tokens > MAX_TOKENS_FOR_REQUEST and len(new_messages) > 2:
            del new_messages[1:3]
            num_tokens = self.num_tokens_from_messages(new_messages)

        return new_messages


if __name__ == '__main__':
    question = """
    Я прохожу урок Треккинга. Расскажи подробнее про Фильтр Калмана.
    """
    # Создаем объект для дообучения chatGPT
    # Если База данных embedding уже создана ранее
    print(f'{os.path.abspath(faiss_db_dir) = } ')
    curator = WorkerOpenAI(faiss_db_dir=faiss_db_dir)
    answer = asyncio.run(curator.get_chatgpt_answer(question, []))
    print(answer)
