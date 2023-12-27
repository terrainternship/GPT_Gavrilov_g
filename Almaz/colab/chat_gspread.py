
import gspread                  # Импортируем API для работы с Google таблицами
import timeit
from chat_functions import *

class ChatSheetQuestions:
    # введем словарь, чтобы можно было обращаться по имени к столбцу
    column_name = {'Ответственный': 0,
        'URL': 1,
        'Название': 2,
        'Вопрос': 3,
        'Ожидаемый ответ': 4,
        'Ответ GPT': 5,
        'Оценка': 6,
        'Ошибка': 7,
        'Комментарий': 8,
        'Чанк №1': 9,
        'Чанк №2': 10,
        'Чанк №3': 11}


        
    top_documents = 3 
    temperature = 0 
    limit_score = 0 
    question_norma = False 
    chat_promt = ""
    bd_index = None
    gpt_model ='gpt-3.5-turbo-1106'
    SELECT_MODEL_GPT = MODEL_COST[gpt_model]
    
    def __init__(self, url_table, gc_auth) -> None:
        # Название файла с вопросами.
        # Ссылка на общий файл.
        try:
            self.spreadsheet = gc_auth.open_by_url(url_table)
            print(f'Подключились к документу - {self.spreadsheet.title}')
            # Получаем список всех страниц файла.
            self.worksheet_list = self.spreadsheet.worksheets()
            print('\nСтраницы документа:')
            print('-------------------')
            for i, worksheet in enumerate(self.worksheet_list):
                    print(f'{i}. {worksheet.title}')


        except Exception as e:
            print(e)
            print(f'Ошибка подключения к документу. Проверьте ссылку.')

    def select_sheet(self, number_sheet=6):
        # Выбор страницы в таблице. 
        # Устанавливаем номер рабочего листа по списку выше.
        self.number_sheet = number_sheet
        for c in self.column_name:
            self.column_name[c]=-1

        if not number_sheet==None:
            # Выбор нужного листа из списка.
            self.worksheet = self.worksheet_list[number_sheet]
            worksheet = self.worksheet
            # Проверка текущей страницы.
            print(f'Текущая страница - "{worksheet.title}"\n')
            # Список всех столбцов на странице.
            print('-----№---------Название---')
            for i, col in enumerate(worksheet.row_values(1)):
                print(f'Колонка № {i}. {col}')
                self.column_name[col]=i
        else:
            print('Введите номер страницы.')    

    def load_sheet(self):
        # Загрузка вопросов. 

        column_question = self.column_name['Вопрос']
        verbose_question = 0 # @param {type:"integer"} #

        worksheet = self.worksheet
        # В данном блоке происходит заполнение списка запросов вопросами и дополнительной
        # информацией с выбранного листа. Загрузка выполняется ВСЕХ строк с вопросами для
        # последующей корректной работы. Далее из этого списка выбирается нужный диапазон
        # вопросов для группового запроса к GPT.

        # Выбор всех вопросов.
        column = worksheet.col_values(column_question)
        if self.question_norma: print("Вопросы будут нормализованы.")
        # Создаем пустой список запросов.
        list_query = []
        column_name = self.column_name
        r_person = column_name['Ответственный']
        r_link = column_name['URL']
        r_subject = column_name['Название']
        r_question = column_name['Вопрос']
        r_answer = column_name['Ожидаемый ответ']
        r_appraisal = column_name['Оценка']

        # Заполнение списка запросов информацией с выбранного листа.
        for i in range(len(column)-1):
            row = worksheet.row_values(i+2)
            # Считывание ячеек с контролем их наличия для избежании ошибки чтения.
            # Проверить индексы row со списком в ячейке выше.
            person = row[r_person] if len(row)>r_person else ""      # Автор вопроса.
            link = row[r_link] if len(row)>r_link else ""        # Ссылка на тему.
            subject = row[r_subject] if len(row)>r_subject else ""     # Тема вопроса.
            question = row[r_question] if len(row)>r_question else ""    # Вопрос.
            answer = row[r_answer] if len(row)>r_answer else ""      # Ожидаемый ответ.
            appraisal = row[r_appraisal] if len(row)>r_appraisal else ""   # Оценка.
            # Нормализация вопроса.
            question = question_normalization(question) if self.question_norma else question
            # Словарь запроса.
            query = {
                "line": i+2,            # Номер строки в документе. Берем строки с вопросами.
                "person": person,       # Автор вопроса.
                "subject": subject,     # Тема вопроса.
                "link": link,           # Ссылка на тему.
                "question": question,   # Вопрос.
                "answer": answer,       # Ожидаемый ответ.
                "answer_gpt": "",       # Ответ GPT.
                "appraisal": appraisal, # Оценка ответа.
                "bug": "",              # Ошибка.
                "comments": "",         # Комментарии.
                "chank_1": "",          # Чанк №1.
                "chank_2": "",          # Чанк №2.
                "chank_3": "",          # Чанк №3.
                "price_query": 0,       # Стоимость запроса общая.
                "price_question": 0,    # Стоимость вопроса с контекстом.
                "price_answer": 0,      # Стоимость ответа.
                "token_query": 0,       # Количество токенов всего вопро-ответ.
                "token_question": 0,    # Количество токенов в вопросе с контекстом.
                "token_answer": 0,      # Количество токенов в ответе.
            }
            list_query.append(query)

        # Вывод вопросов.
        if verbose_question:
            for query in list_query:
                print(f'Строка №{query["line"]}. Вопрос: {query["question"]}')

        # Диапазон строк с вопросами на выбранной странице.
        print(f'\n\nЗагрузка списка вопросов завершена. Количество вопросов: {len(column)-1}.')
        print(f"Диапазон номеров строк с вопросами (включительно): [{list_query[0]['line']}:{list_query[-1]['line']}].")
        self.list_query = list_query

    def execute(self,  row_first = 51, row_end = 51, verbose_answer = 0, verbose_chank = 0):

        # @title Выбор диапазона вопросов группого запроса. Отправка запроса. { vertical-output: true }

        # Определение диапазона строк с вопросами. Начало диапазона, конец диапазона (включительно).

        # Если подвис ответ от GPT можно прервать обработку, установить row_first
        # в значение на которой была прервана обработка и запустить обработку заново.
        # Ранее обработанные вопросы будут сохранены в файле.

        # Обнуление общих затрат на групповой запрос.
        total_price_query, total_token_query, total_query = 0, 0, 0
        # Фиксация времени.
        start_group = timeit.default_timer()
        list_query = self.list_query
        for query in list_query[row_first-2:row_end-1]:
            # Проверка на пустой вопрс. Если пустой пропуск цикла.
            if not bool(query['question'].strip ()):
                print(f'На строке № {query["line"]} - вопроса нет.')
                continue
            # Отправка запроса. Фиксация времени.
            start = timeit.default_timer()
            try:
                query["answer_gpt"]= answer_index(
                    model = self.SELECT_MODEL_GPT,
                    system = self.chat_promt,
                    topic = "",
                    query = query,
                    search_index = self.bd_index,
                    temp = self.temperature,
                    verbose_documents = 0,
                    verbose_price = 0,
                    top_documents = self.top_documents,
                    limit_score = self.limit_score,
                )
                total_price_query += query['price_query']
                total_token_query += query['token_query']
                total_query +=1
            except Exception as e:
                print(f'Ошибка ответа GPT на строке №{query["line"]}. - {e}')
            end = timeit.default_timer()
            # Сообщение об успешности ответа от GPT.
            print(f'Строка №{query["line"]}. Ответ на вопрос получен за - {round(end-start, 3)} сек.')

            # Запись ответа в файл.
            worksheet = self.worksheet
            r_answer_gpt = self.column_name['Ответ GPT']
            r_chank_1 = self.column_name['Чанк №1']
            r_chank_2 = self.column_name['Чанк №2']
            r_chank_3 = self.column_name['Чанк №3']

            def update_cell(row, name):
                worksheet.update_cell(query['line'], row, query[name]) # Ответ GPT.

            try:
                if bool(query['answer_gpt']):
                    update_cell(r_answer_gpt, 'answer_gpt') # Ответ GPT.
                    update_cell(r_chank_1, 'chank_1') # Чанк №1.
                    update_cell(r_chank_2, 'chank_2') # Чанк №2.
                    update_cell(r_chank_3, 'chank_3') # Чанк №3.

                    print(f'Строка №{query["line"]}. Ответ записан в файл.')
                    # Контроль номализации вопроса и перезапись его в таблице.
                    if self.question_norma:
                        question_old = worksheet.row_values(query['line'])[self.column_question]
                        if not (question_old == query['question']):
                            print("    Вопрос нормализован и перезаписан в таблице.")
                            print(f"    Старый вариант: {question_old}")
                            print(f"    Новый вариант : {query['question']}")
                            worksheet.update_cell(query['line'], self.column_question+1, query['question'])
            except Exception as e:
                print('\n========================================================')
                print(f'!!!Ошибка записи строки №{query["line"]} в файл. - {e}')
                print('========================================================')

        end_group = timeit.default_timer()

        # Вывод вопросов и ответов.
        if verbose_answer:
            for i, query in enumerate(list_query):
                if query['answer_gpt']:
                    print()
                    print(insert_newlines(f"ВОПРОС №{i+2}: {query['question']}"))
                    print('---------------------------')
                    print(insert_newlines(f"\nОТВЕТ: {query['answer_gpt']}"))
                    print('===========================\n')
                    if verbose_chank:
                        print(query['chank_1'])
                        print()
                        print(query['chank_2'])
                        print()
                        print(query['chank_3'])

        print()
        print('-------------------------------------------')
        print(f'Вопросов в пакетной обработке - {total_query} шт.')
        print(f'Время пакетной обработки      - {round(end_group-start_group, 1)} сек.')
        print(f'Стоимость пакетной обработки  - {round(total_price_query, 4)} $.')
        print(f'Токенов в пакетной обработке  - {total_token_query} шт.')

