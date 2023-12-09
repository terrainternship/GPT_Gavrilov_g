import os
import queue
import threading
from os import path
import apprise
# Apprise - это библиотека для отправки уведомлений на различные сервисы уведомлений.
# Она позволяет отправлять уведомления на большое количество сервисов уведомлений,
# таких как Telegram, Discord, Slack, Amazon SNS, Gotify и многие другие
from config import APPRISE_CONFIG_PATH

#APPRISE_CONFIG_PATH = "settings/apprise.yml"


class NotificationHandler:
    def __init__(self, enabled=True):
        if enabled and path.exists(APPRISE_CONFIG_PATH):
            self.apobj = apprise.Apprise()      # Создам экземпляр класса apprise.Apprise (apprise_object)
            config = apprise.AppriseConfig()    # Создаем config (экземпляр класса apprise.AppriseConfig)
            config.add(APPRISE_CONFIG_PATH)     # добавляем в config наши настройки
            self.apobj.add(config)              # Настраиваем наш apobj в соответствии с config
            self.queue = queue.Queue()          # Создаем очередь queue.Queue
            self.start_worker()                 # Запускаем уведомления
            self.enabled = True                 # Устанавливаем флаг включения обработчика уведомлений
        else:
            self.enabled = False                # Устанавливаем флаг выключения обработчика уведомлений

    def start_worker(self):
        # Запускаем обработчик сообщений в отдельном потоке
        threading.Thread(target=self.process_queue, daemon=True).start()

    def process_queue(self):
        while True:
            message, attachments = self.queue.get()     # Получаем сообщение из очереди сообщений

            if attachments:
                self.apobj.notify(body=message, attach=attachments)     # Отправляем уведомление с вложениями
            else:
                self.apobj.notify(body=message)         # Отправляем уведомление без вложений
            self.queue.task_done()                      # Отмечаем сообщение как выполненное в очереди сообщений

    def send_notification(self, message, attachments=None):
        if self.enabled:
            self.queue.put((message, attachments or []))    # Добавляем сообщение в очередь сообщений для отправки

if __name__ == '__main__':
    print(f'{os.path.abspath(APPRISE_CONFIG_PATH)}')