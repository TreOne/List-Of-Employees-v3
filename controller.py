from utility.employees import Employee
from utility.settings import Settings
from view.mw_view import MWView
from PyQt5.QtCore import pyqtSlot
#from utility.AddressHelper import AddressHelper
from PyQt5.QtWidgets import QCompleter, QTableWidgetItem, QSizePolicy, QHBoxLayout, QLabel, QSpacerItem, QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel, Qt
#from View.OFView import OFView  # Представление для редактирования данных организации
#from View.HWView import HWView  # Представление для редактирования списков вредностей
from datetime import datetime
import re
#from Utility.DocxCreator import DocxCreator


class Controller:

    def __init__(self, model, organization):

        self.app_settings = Settings()
        self.organization = organization

        # Модель и Представление
        self.model = model
        self.view = MWView(controller=self, autoload_ui=True)
        self.refresh_column_views()

        self.view.showMaximized()

    def refresh_column_views(self):
        # Скрываем отмеченные в настройках колонки и отображаем остальные
        columns_to_hide = self.app_settings.get('appearance', 'sections_to_hide')
        columns_to_hide = columns_to_hide.split(', ')
        for column in Employee.ALL_FIELDS:
            if column in columns_to_hide:
                self.view.hide_column(column=column)
            else:
                self.view.show_column(column=column)

    def hide_checkbox_clicked(self, sender):
        column_name = sender.objectName().replace('hide_col_', '')
        columns_to_hide = self.app_settings.get('appearance', 'sections_to_hide')
        if columns_to_hide == "":
            columns_to_hide = list()
        else:
            columns_to_hide = columns_to_hide.split(', ')
        if sender.isChecked():
            columns_to_hide.remove(column_name)
        else:
            columns_to_hide.append(column_name)
        self.app_settings.set('appearance', 'sections_to_hide', ", ".join(columns_to_hide))
        self.refresh_column_views()
