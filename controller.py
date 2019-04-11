from view.mw_view import MWView
#from utility.AddressHelper import AddressHelper
from PyQt5.QtWidgets import QCompleter, QTableWidgetItem, QSizePolicy, QHBoxLayout, QLabel, QSpacerItem, QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel, Qt
#from View.OFView import OFView  # Представление для редактирования данных организации
#from View.HFView import HFView  # Представление для редактирования списков вредностей
from datetime import datetime
import re
#from Utility.DocxCreator import DocxCreator


class Controller:

    def __init__(self, model):

        # Модель и Представление
        self.model = model
        self.view = MWView(controller=self, autoload_ui=True)

        self.view.show()
