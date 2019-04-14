from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QShortcut
from utility.employees import Employee
from view.ui.main_window import Ui_MainWindow
import datetime
from utility.resource_path import resource_path
from utility import resources
from utility.settings import Settings
from model import EmployeesSortModel


def _mute(method_to_mute):
    """Декоратор заглушающий сигналы от формы на время выполнения декорируемой функции"""
    def to_mute(self, *args, **kwargs):
        self.block_signals(True)
        method_to_mute(self, *args, **kwargs)
        self.block_signals(False)
    return to_mute


class MWView(QtWidgets.QMainWindow):
    """
    Класс MWView отвечает за визуальное представление главного окна.

    (Заметка для разработчика) Для импорта ресурсов:
    pyrcc5 -o utility/resources.py .pyqt5/resources/resources.qrc
    """

    def __init__(self, controller, autoload_ui=False):

        self.controller = controller

        # Подключаем Представление
        flags = Qt.WindowFlags()
        super(MWView, self).__init__(parent=None, flags=flags)

        # Подключаем UI
        # TODO: При релизе, переключить с динамической компиляции интерфейса на статическую.
        if autoload_ui:
            self.ui = uic.loadUi(resource_path('.pyqt5/main_window.ui'), self)
        else:
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

        # Список визуальных элементов формы
        self.FORM_FIELDS = [self.ui.family_name, self.ui.first_name,
                            self.ui.patronymic, self.ui.sex,
                            self.ui.birth_date, self.ui.address_free_form,
                            self.ui.experience, self.ui.specialty]

        # Список чекбоксов для отображения/скрытия колонок таблицы
        self.HIDE_COLUMN_CHECKBOXES = [self.ui.hide_col_family_name, self.ui.hide_col_first_name,
                                       self.ui.hide_col_patronymic, self.ui.hide_col_sex,
                                       self.ui.hide_col_birth_date, self.ui.hide_col_address_free_form,
                                       self.ui.hide_col_experience, self.ui.hide_col_specialty,
                                       self.ui.hide_col_hazard_types, self.ui.hide_col_hazard_factors]

        # Подключаем модель к главной таблице

        proxy_model = EmployeesSortModel()
        proxy_model.setSourceModel(controller.model)
        # proxyModel.setDynamicSortFilter(True)
        self.ui.employees_table.setModel(proxy_model)

        # self.ui.employees_table.setModel(controller.model)
        self.adjust_column_width()

        # Подключаем сигналы к контроллеру
        for column_name in Employee.ALL_FIELDS:
            # Ищем чекбокс, отвечающий за колонку
            hide_checkbox = getattr(self.ui, 'hide_col_' + column_name)
            hide_checkbox.stateChanged.connect(lambda: self.controller.hide_checkbox_clicked(self.sender()))

    def adjust_column_width(self):
        column_to_stretch = ('address_free_form', 'hazard_types', 'hazard_factors')
        header = self.ui.employees_table.horizontalHeader()
        for column in Employee.ALL_FIELDS:
            column_number = Employee.ALL_FIELDS.index(column)
            if column in column_to_stretch:
                header.setSectionResizeMode(column_number, QtWidgets.QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(column_number, QtWidgets.QHeaderView.ResizeToContents)

    def show_columns(self):
        for column_name in Employee.ALL_FIELDS:
            self.show_column(column_name)

    def hide_columns(self):
        for column_name in Employee.ALL_FIELDS:
            self.hide_column(column_name)

    @_mute
    def show_column(self, column):
        if column in Employee.ALL_FIELDS:
            hide_checkbox = getattr(self.ui, 'hide_col_' + column)
            self.ui.employees_table.showColumn(Employee.ALL_FIELDS.index(column))
            hide_checkbox.setChecked(True)

    @_mute
    def hide_column(self, column):
        if column in Employee.ALL_FIELDS:
            hide_checkbox = getattr(self.ui, 'hide_col_' + column)
            self.ui.employees_table.hideColumn(Employee.ALL_FIELDS.index(column))
            hide_checkbox.setChecked(False)

    def block_signals(self, boolean):
        """Заглущает или восстанавливает сигналы полей и чекбоксов"""
        for field in self.FORM_FIELDS:
            field.blockSignals(boolean)
        for checkbox in self.HIDE_COLUMN_CHECKBOXES:
            checkbox.blockSignals(boolean)
