from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QShortcut
from view.ui.main_window import Ui_MainWindow
import datetime
from utility.resource_path import resource_path
from utility import resources


class MWView(QtWidgets.QMainWindow):
    """
    Класс MWView отвечает за визуальное представление главного окна.
    Для импорта ресурсов (заметка для разработчика):
    pyrcc5 -o utility/resources.py .pyqt5/resources/resources.qrc
    """

    def __init__(self, controller, autoload_ui=False):

        self.controller = controller

        # Подключаем Представление
        flags = Qt.WindowFlags()
        super(MWView, self).__init__(parent=None, flags=flags)

        # Подключаем UI
        if autoload_ui:
            self.ui = uic.loadUi(resource_path('.pyqt5/main_window.ui'), self)
        else:
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

        self.ui.employees_table.setModel(controller.model)
