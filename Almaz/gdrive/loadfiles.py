from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import yaml

# Авторизация
# settings_file='c:/Data/Study/NU/Stag_202312/Data/client_secrets.json'
settings_file="config.yaml"
gauth = GoogleAuth(settings_file) # settings_file=settings_file
# gauth.settings['client_config_file']=settings_file
#gauth.LoadCredentialsFile(settings_file)
print(gauth.settings)

def save_yaml():
    yaml_file_path ="config.yaml"
    data = gauth.settings
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

import os
def list_dir():
    # cred_file = "mycreds.txt"
    # if os.path.exists(cred_file):
    #     gauth.LoadCredentialsFile(cred_file)
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()  # откроет окно браузера для аутентификации
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    # gauth.SaveCredentialsFile(cred_file)


    # Создание экземпляра GoogleDrive
    drive = GoogleDrive(gauth)

    # ID папки, которую вы хотите просмотреть
    # folder_id = '1tx5V_1G5AkSaVgC674NoczPcC9cDLoQN'
    folder_id ="1NZ4zzXDKuVUZVgMir99TBC9bmK4Eh3AD"
    # Получение списка файлов в папке
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

    # Вывод информации о файлах
    for file in file_list:
        print('Title: %s, ID: %s' % (file['title'], file['id']))

list_dir()
