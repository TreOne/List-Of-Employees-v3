from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QShortcut
from view.ui.main_window import Ui_MainWindow
import datetime
#from Utility.file_paths import resource_path


class MWView(QtWidgets.QMainWindow):
    """
    Класс MWView отвечает за визуальное представление главного окна.
    """

    def __init__(self, controller):

        self.controller = controller

        # Подключаем Представление
        flags = Qt.WindowFlags()
        super(MWView, self).__init__(parent=None, flags=flags)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.employees_table.setModel(controller.model)
