import logging.handlers
import os
from logger.notifications import NotificationHandler
from config import LOG_PATH, ROOT_DIR, LOGGING_SERVICE


class Logger:
    Logger = None
    NotificationHandler = None

    def __init__(self, logging_service=LOGGING_SERVICE, enable_notifications=True):
        '''
        конструктор класса, который инициализирует логгер и настройки логирования.
        '''

        # Logger setup:
        self.Logger = logging.getLogger(
            f"{logging_service}_logger")  # создание объекта логгера с именем "{logging_service}_logger"
        self.Logger.setLevel(logging.DEBUG)  # установка уровня логирования на DEBUG
        self.Logger.propagate = False  # отключение передачи сообщений логгера родительским логгерам
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s")  # создание объекта форматирования логов
        log_path = os.path.join(ROOT_DIR, LOG_PATH)
        log_file = f"{log_path}/{logging_service}.log"
        fh = logging.FileHandler(
            log_file, encoding='utf-8')  # создание объекта обработчика файла, который записывает логи в файл с именем "{logging_service}.log"
        fh.setLevel(logging.DEBUG)  # установка уровня логирования на DEBUG
        fh.setFormatter(formatter)  # установка форматирования для обработчика файла
        self.Logger.addHandler(fh)  # добавление обработчика файла в логгер

        # logging to console:
        ch = logging.StreamHandler()  # создание объекта обработчика потока, который записывает логи в консоль
        ch.setLevel(logging.INFO)  # установка уровня логирования на INFO
        ch.setFormatter(formatter)  # установка форматирования для обработчика потока
        self.Logger.addHandler(ch)  # добавление обработчика потока в логгер

        # notification handler
        # создание объекта обработчика уведомлений с помощью класса NotificationHandler (из файла notification.py):
        self.NotificationHandler = NotificationHandler(enable_notifications)

    def log(self, message, level="info", notification=True):
        if level == "info":
            self.Logger.info(message)
        elif level == "warning":
            self.Logger.warning(message)
        elif level == "error":
            self.Logger.error(message)
        elif level == "debug":
            self.Logger.debug(message)
        elif level == "exception":
            self.Logger.exception(message)

        if notification and self.NotificationHandler.enabled:
            self.NotificationHandler.send_notification(str(message))

    def info(self, message, notification=True):
        self.log(message, "info", notification)

    def warning(self, message, notification=True):
        self.log(message, "warning", notification)

    def error(self, message, notification=True):
        self.log(message, "error", notification)

    def debug(self, message, notification=False):
        self.log(message, "debug", notification)

    def exception(self, message, notification=True):
        self.log(message, "exception", notification)


logger = Logger(enable_notifications=False)
logger.info("Start logging")
