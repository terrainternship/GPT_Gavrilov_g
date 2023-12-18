import asyncio
import os

import pandas as pd
from dbase.dbworker import get_df_users, get_df_history, init_db, create_db
from datetime import datetime
import gspread
import pygsheets
from create_bot import GSERVICEACCOUNTFILE, SHEETID_PARAM
from logger.logger import logger

# Google Sheets setup
google_drive = None
#init_db()
#asyncio.run(create_db())


def creat_new_google_sheets(name):
    try:
        gc = pygsheets.authorize(service_file=GSERVICEACCOUNTFILE)
        sh = gc.create(name)
        sh.add_worksheet('Пользователи')
        sh.add_worksheet('Оценки')
    except Exception as e:
        print(f'creat_new_google_sheets: {e} ')
    return sh.url


def share_google_sheets(email_address):
    try:
        gc = pygsheets.authorize(service_file=GSERVICEACCOUNTFILE)
        sh = gc.open_by_url(f'https://docs.google.com/spreadsheets/d/{SHEETID_PARAM}')
        sh.share(email_address, role='writer', type='anyone')
        logger.info(f'share_google_sheets: Уcпешно!')
    except Exception as e:
        logger.error(f'share_google_sheets: {e}')


def save_data_to_google_sheets(sheet_name, data):
    #print(f'save_data_to_google_sheets: Полный путь к файлу:{os.path.abspath(GSERVICEACCOUNTFILE)}')
    # if os.path.isfile(GSERVICEACCOUNTFILE):
    #     print(f"File exists {os.path.abspath(GSERVICEACCOUNTFILE)}")
    # else:
    #     print(f"File does not exist {os.path.abspath(GSERVICEACCOUNTFILE)}")

    try:
        gc = gspread.service_account(filename=GSERVICEACCOUNTFILE)  # Авторизуемся в Google Sheets с помощью файла учетных данных GSERVICEACCOUNTFILE
        spreadsheet = gc.open_by_key(SHEETID_PARAM)                 # Открываем таблицу Google Sheets по ключу SHEETID_PARAM
        worksheet = spreadsheet.worksheet(sheet_name)               # Получаем лист таблицы по имени sheet_name
        worksheet.append_row(data)                                  # Добавляем строку данных в конец листа
    except Exception as e:
        logger.error(f'save_data_to_google_sheets: {e}')


def set_report_into_gsh():
    # print(f'set_report_into_gsh: Полный путь к файлу:{os.path.abspath(GSERVICEACCOUNTFILE)}')
    # if os.path.isfile(GSERVICEACCOUNTFILE):
    #     print(f"File exists {os.path.abspath(GSERVICEACCOUNTFILE)}")
    # else:
    #     print(f"File does not exist {os.path.abspath(GSERVICEACCOUNTFILE)}")

    try:
        gc = pygsheets.authorize(service_file=GSERVICEACCOUNTFILE)  # Авторизуемся в Google Sheets с помощью файла учетных данных GSERVICEACCOUNTFILE
        sh = gc.open_by_key(SHEETID_PARAM)                          # Открываем таблицу Google Sheets по ключу SHEETID_PARAM
        # Заголовки столбцов
        columns_users = [                                           # Создаем список columns_users с заголовками столбцов таблицы "Пользователи"
            'user_id', 'e_mail', 'first_name', 'last_name', 'username', 'last_interaction', 'num_queries',
            'last_dialog', 'last_question', 'last_answer'
        ]

        columns_history = [                                         # Создаем список columns_history с заголовками столбцов таблицы "Оценки"
            'user_id', 'score_name', 'score_text', 'score_chunks', 'score', 'num_token', 'date_estimate',
            'time_duration'
        ]

        sheet_name = ['Пользователи', 'Оценки']                     # Создаем список sheet_name с названиями листов таблицы

        df_users = get_df_users()[columns_users]                    # Получаем DataFrame df_users и выбираем только нужные столбцы columns_users
        df_users['num_queries'] = df_users['num_queries'].astype(int)   # Преобразовываем столбец num_queries в целочисленный тип данных
        # df_users = df_users.sort_values(by='last_interaction', ascending=True)
        df_score = get_df_history()[columns_history]                # Получаем DataFrame df_score и выбираем только нужные столбцы columns_history
        df_score['time_duration'] = df_score['time_duration'].astype(int)
        wks_write = sh.worksheet_by_title(sheet_name[0])            # Получаем лист таблицы по имени sheet_name[0]
        wks_write.set_dataframe(df_users, (1, 1), encoding='utf-8', fit=True)   # Записываем DataFrame df_users в лист таблицы
        wks_write = sh.worksheet_by_title(sheet_name[1])
        wks_write.set_dataframe(df_score, (1, 1), encoding='utf-8', fit=True)
    except Exception as e:
        logger.error(f'set_report_into_gsh: {e}')


def set_users_into_gsh():
    """
    Добавление нового пользователя в таблицу Google
    :return:
    """
    #print(f'1. set_users_into_gsh: Полный путь к файлу "{GSERVICEACCOUNTFILE}": {os.path.abspath(GSERVICEACCOUNTFILE)}\n {SHEETID_PARAM =}')
    # if os.path.isfile(GSERVICEACCOUNTFILE):
    #     print(f"File exists {os.path.abspath(GSERVICEACCOUNTFILE)}")
    # else:
    #     print(f"File does not exist {os.path.abspath(GSERVICEACCOUNTFILE)}")

    try:
        gc = pygsheets.authorize(service_file=GSERVICEACCOUNTFILE)
        sh = gc.open_by_key(SHEETID_PARAM)
        # Заголовки столбцов
        columns_users = [
            'user_id', 'e_mail', 'first_name', 'last_name', 'username', 'last_interaction', 'num_queries'
        ]
        df_users = get_df_users()[columns_users]
        df_users['num_queries'] = df_users['num_queries'].astype(int)
        wks_write = sh.worksheet_by_title('Пользователи')
        wks_write.set_dataframe(df_users, (1, 1), encoding='utf-8', fit=True)
    except Exception as e:
        logger.error(f'set_users_into_gsh: {e}')


def get_report():
    """
    Формируем отчет в электронную таблицу XLS
    :return:
    """

    # Заголовки столбцов
    columns_users = [
        'user_id', 'e_mail', 'first_name', 'last_name', 'username', 'last_interaction', 'num_queries'
    ]

    columns_history = [
        'user_id', 'score_name', 'score_text', 'score', 'score_chunck', 'num_token', 'date_estimate', 'time_duration'
    ]

    sheet_name = ['Пользователи', 'Оценки']
    sheet_col_width = [
        {'A:A': 12, 'B:B': 20, 'C:C': 20, 'D:D': 20, 'E:E': 30, 'F:F': 20, 'G:G': 20},
        {'A:A': 20, 'B:B': 14, 'C:C': 80, 'D:D': 12, 'E:E': 20, 'F:F': 20, 'G:G': 20}
        ]

    df_users = get_df_users()[columns_users]
    df_score = get_df_history()[columns_history]
    name_report = f'report_Bot_Agent5_01_{datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}.xlsx'
    with pd.ExcelWriter(name_report) as writer:
        workbook = writer.book
        df_users.to_excel(writer, sheet_name=sheet_name[0], index=False)
        df_score.to_excel(writer, sheet_name=sheet_name[1], index=False)
        cell_format = workbook.add_format({'align': 'left', 'text_wrap': 'true'})
        for i, sh_status in enumerate(sheet_name):
            sheet = writer.sheets[sh_status]
            for key in sheet_col_width[i].keys():
                sheet.set_column(str(key), int(sheet_col_width[i][key]), cell_format)
    return name_report


if __name__ == '__main__':

    # url_sh = creat_new_google_sheets('agent500')
    # print(f'{url_sh =}')
    # TODO: выдача прав работает некорректно: после того, как создали новую таблицу ее SHEETID_PARAM сначала надо внести в CONFIF, а уже затем вторым запуском расшаривать
    share_google_sheets('') # выдача права на редактривание каждому у кого есть ссылка

    #get_report()
    #set_users_into_gsh()
    #pass