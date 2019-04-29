import os
import threading
import time
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QAction
from utility.xml_parser import XMLParser

dir_name = 'СписокСотрудников'
local_data = os.getenv('LOCALAPPDATA')
path = os.path.join(local_data, dir_name)


class AutoSaver(QtCore.QObject):

    auto_save_finished = QtCore.pyqtSignal()

    def __init__(self, organization=None, employees=None):
        super().__init__()
        if organization is None or employees is None:
            return
        self.auto_save_time = 120
        self.organization = organization
        self.employees = employees
        self.parser = XMLParser()
        self.recent_file_menu = None
        self.load_action = None

        # Создаем каталог для хранения файлов сохранения в %LOCALAPPDATA%\СписокСотрудников
        if not os.path.exists(path):
            os.mkdir(path)

        # Запускаем демона для автосохранения
        t = threading.Thread(target=self.auto_save_file, name="Auto Save Daemon", daemon=True)
        t.start()

    def auto_save_file(self):
        while True:
            time.sleep(self.auto_save_time)

            # Удаляем старые сохранения (те что старше 9-го сохранения)
            files = os.listdir(path)
            old_files = files[0:-9]
            for file in old_files:
                os.remove(os.path.join(path, file))

            now = datetime.now()
            name = "Автосохранение {}.xml".format(now.strftime("%d.%m.%Y (%H.%M.%S)"))
            filename = os.path.join(path, name)
            self.parser.save_to_file(filename, self.organization, self.employees)
            self.auto_save_finished.emit()

    def update_data(self, organization, employees):
        self.organization = organization
        self.employees = employees

    @staticmethod
    def get_saves_list():
        saves = dict()
        files = os.listdir(path)
        files.sort(reverse=True)
        for i, file in enumerate(files):
            menu_name = "Сохранено {date} в {hour}:{minute}".format(date=file[15:25],
                                                                    hour=file[27:29],
                                                                    minute=file[30:32])
            saves[i] = (menu_name, os.path.join(path, file))
        return saves
