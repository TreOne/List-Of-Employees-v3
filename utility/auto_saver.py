import os
import threading
import time
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction
from utility.xml_parser import XMLParser

dir_name = 'СписокСотрудников'
local_data = os.getenv('LOCALAPPDATA')
path = os.path.join(local_data, dir_name)


class AutoSaver:
    def __init__(self, organization=None, employees=None):
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
            self.update_menu()

    def update_data(self, organization, employees):
        self.organization = organization
        self.employees = employees

    def set_menu_for_update(self, recent_file_menu):
        """Задает меню которое надо заполнять, при добавлении новых файлов."""
        self.recent_file_menu = recent_file_menu
        self.update_menu()

    def set_load_action(self, load_action):
        """Задает действие, которое надо выполнить, при выборе пункта меню автозагрузки."""
        self.load_action = load_action
        self.update_menu()

    def __get_saves_list(self):
        saves = dict()
        files = os.listdir(path)
        files.sort(reverse=True)
        for i, file in enumerate(files):
            menu_name = "Сохранено {date} в {hour}:{minute}".format(date=file[15:25],
                                                                    hour=file[27:29],
                                                                    minute=file[30:32])
            saves[i] = (menu_name, os.path.join(path, file))
        return saves

    def update_menu(self):
        # TODO: Функция не работает
        if self.recent_file_menu is not None and self.load_action is not None:
            self.recent_file_menu.clear()
            for menu_name, menu_path in self.__get_saves_list().values():
                load_autosave_action = QAction(menu_name, self.recent_file_menu)
                # load_autosave_action.triggered.connect(lambda: self.load_action(menu_path))
                func = lambda: print(menu_path)
                load_autosave_action.triggered.connect(func)
                print(load_autosave_action, menu_path)
                self.recent_file_menu.addAction(load_autosave_action)

# class RecentFilesMenuModel(QStringListModel):
#
#     def __init__(self, parent=None):
#         super(RecentFilesMenuModel, self).__init__(parent)
#
#     def data(self, index, role=None):
#         if not index.isValid():
#             return
#
#         save_files = self.__get_saves_list()
#         title, filename = save_files[index.row()]
#         if role == Qt.DisplayRole:
#             return title
#
#     def rowCount(self, *args, **kwargs):
#         return len(self.files_list)
#
#     def __get_saves_list(self):
#         saves = dict()
#         files = os.listdir(path)
#         for i, file in enumerate(files):
#             menu_name = "Сохранено {date} в {hour}:{minute}".format(date=file[15:25],
#                                                                     hour=file[27:29],
#                                                                     minute=file[30:32])
#             saves[i] = (menu_name, os.path.join(path, file))
#         return saves
