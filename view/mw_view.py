from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QShortcut, QMessageBox
from utility.docx_creator import DocxCreator
from utility.employees import Employee, Employees
from model import EmployeesListModel
import utility.resources
from utility.organization import Organization
from utility.xml_parser import XMLParser
from view.of_view import OFView
from view.ui.main_window import Ui_MainWindow
from utility.resource_path import resource_path
from utility.settings import Settings
from model import EmployeesSortModel
from utility.delegates import InLineEditDelegate, GenderSelectionDelegate, BirthDateSelectionDelegate, \
    ExperienceSelectionDelegate, HazardsSelectionDelegate
from datetime import datetime
import os


class MWView(QtWidgets.QMainWindow):
    """
    Класс MWView отвечает за визуальное представление главного окна.

    (Заметки для разработчика)
        Для импорта ресурсов:
            pyrcc5 .pyqt5/resources/resources.qrc -o utility/resources.py
        Для импорта UI в PY:
            pyuic5 -x .pyqt5/main_window.ui -o view/ui/main_window.py
    """

    def __init__(self, autoload_ui=False):

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

        self.model = EmployeesListModel(Employees())
        self.organization = Organization()

        self.filename = None
        self.last_path = None
        self.data_is_saved = True
        self.app_settings = Settings()

        # Стартовая инициализация внешнего вида / данных
        self.update_window_title()
        self.fill_organization_fields()

        # Список чекбоксов для отображения/скрытия колонок таблицы
        self.HIDE_COLUMN_CHECKBOXES = [self.ui.hide_col_family_name, self.ui.hide_col_first_name,
                                       self.ui.hide_col_patronymic, self.ui.hide_col_sex,
                                       self.ui.hide_col_birth_date, self.ui.hide_col_address_free_form,
                                       self.ui.hide_col_experience, self.ui.hide_col_specialty,
                                       self.ui.hide_col_hazard_types, self.ui.hide_col_hazard_factors]

        # Подключаем модель к главной таблице
        self.proxy_model = EmployeesSortModel()
        self.proxy_model.setSourceModel(self.model)
        self.ui.employees_table.setModel(self.proxy_model)

        # Создаем делегатов для редактирования данных модели
        in_line_edit_delegate = InLineEditDelegate(self, self.model)
        gender_selection_delegate = GenderSelectionDelegate(self)
        birth_date_selection_delegate = BirthDateSelectionDelegate(self)
        experience_selection_delegate = ExperienceSelectionDelegate(self)
        hazards_selection_delegate = HazardsSelectionDelegate(self)

        # Подключаем делегатов к таблице
        self.ui.employees_table.setItemDelegateForColumn(0, in_line_edit_delegate)  # Фамилия
        self.ui.employees_table.setItemDelegateForColumn(1, in_line_edit_delegate)  # Имя
        self.ui.employees_table.setItemDelegateForColumn(2, in_line_edit_delegate)  # Отчество
        self.ui.employees_table.setItemDelegateForColumn(3, gender_selection_delegate)  # Пол
        self.ui.employees_table.setItemDelegateForColumn(4, birth_date_selection_delegate)  # Дата рождения
        self.ui.employees_table.setItemDelegateForColumn(6, experience_selection_delegate)  # Стаж
        self.ui.employees_table.setItemDelegateForColumn(5, in_line_edit_delegate)  # Адрес
        self.ui.employees_table.setItemDelegateForColumn(7, in_line_edit_delegate)  # Должность
        self.ui.employees_table.setItemDelegateForColumn(8, hazards_selection_delegate)  # Типы вредности
        self.ui.employees_table.setItemDelegateForColumn(9, hazards_selection_delegate)  # Факторы вредности

        # Выравниваем колонки таблицы
        self.adjust_column_width()

        # Подключаем контекстное меню к таблице
        self.ui.employees_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.employees_table.customContextMenuRequested.connect(self.context_menu)

        # Подключаем сигналы
        self.ui.add_employee_btn.clicked.connect(self.proxy_model.insertRow)
        self.ui.remove_employee_btn.clicked.connect(self.remove_rows)
        self.ui.menu_about.triggered.connect(self.open_about_window)
        self.ui.organization_edit_btn.clicked.connect(self.organization_edit_btn_clicked)
        self.ui.menu_new_file.triggered.connect(self.menu_new_file_clicked)
        self.ui.menu_open.triggered.connect(self.menu_open_clicked)
        self.ui.menu_save.triggered.connect(self.menu_save_file_clicked)
        self.ui.menu_save_as.triggered.connect(self.menu_save_file_as_clicked)
        self.ui.menu_export_word.triggered.connect(self.menu_export_word_clicked)
        self.model.dataChanged.connect(self.data_changed)
        self.model.rowsAddRemove.connect(self.data_changed)

        # Горячие клавиши
        QShortcut(QKeySequence(Qt.Key_F1), self, self.proxy_model.insertRow)
        QShortcut(QKeySequence(Qt.Key_Delete), self, self.remove_rows)
        QShortcut(QKeySequence.New, self, self.menu_new_file_clicked)
        QShortcut(QKeySequence.Open, self, self.menu_open_clicked)
        QShortcut(QKeySequence.Save, self, self.menu_save_file_clicked)
        QShortcut(QKeySequence.SaveAs, self, self.menu_save_file_as_clicked)

        # Подключаем сигналы к контроллеру
        for column_name in Employee.ALL_FIELDS:
            # Ищем чекбокс, отвечающий за колонку
            hide_checkbox = getattr(self.ui, 'hide_col_' + column_name)
            hide_checkbox.stateChanged.connect(self.hide_checkbox_clicked)

        self.refresh_column_views()
        self.showMaximized()

    #     edit_key = QShortcut(QKeySequence(Qt.Key_Return), self.ui.employees_table)
    #     edit_key.activated.connect(self.item_edit)
    #
    # def item_edit(self):
    #     """Переводим активную ячейку в режим редактирования"""
    #     if self.ui.employees_table.selectedIndexes():
    #         edited_cell_index = self.ui.employees_table.selectedIndexes()[0]
    #         self.ui.employees_table.edit(edited_cell_index)

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

    def show_column(self, column):
        if column in Employee.ALL_FIELDS:
            hide_checkbox = getattr(self.ui, 'hide_col_' + column)
            self.ui.employees_table.showColumn(Employee.ALL_FIELDS.index(column))
            hide_checkbox.setChecked(True)

    def hide_column(self, column):
        if column in Employee.ALL_FIELDS:
            hide_checkbox = getattr(self.ui, 'hide_col_' + column)
            self.ui.employees_table.hideColumn(Employee.ALL_FIELDS.index(column))
            hide_checkbox.setChecked(False)

    def context_menu(self):
        menu = QtWidgets.QMenu()

        add_data = menu.addAction("Добавить сотрудника")
        add_data.setIcon(QtGui.QIcon(":/icons/add_user.svg"))
        add_data.triggered.connect(self.proxy_model.insertRow)

        remove_data = menu.addAction("Удалить сотрудника")
        remove_data.setIcon(QtGui.QIcon(":/icons/rem_user.svg"))
        remove_data.triggered.connect(self.remove_rows)

        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def remove_rows(self):
        selected_indexes = self.ui.employees_table.selectedIndexes()
        if selected_indexes:
            answer = QMessageBox.question(self, 'Удалить сотрудника',
                                          "Вы действительно хотите удалить сотрудника?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if answer == QMessageBox.No:
                return
            self.proxy_model.removeRows(selected_indexes)
        else:
            QMessageBox.critical(self, 'Удаление невозможно!',
                                 "Не выбран сотрудник для удаления.",
                                 QMessageBox.Close, QMessageBox.Close)

    def open_about_window(self):
        version = self.app_settings.get('system', 'version')
        QMessageBox.about(self, 'О СписокСотрудников v.{}'.format(version),
                          'Разработано ООО "Системная Интеграция"\n'
                          'официальный партнер компании «САМСОН Групп»\n'
                          'в Великом Новгороде\n\n'
                          'Версия {}\n'
                          'Copyright © 2019 ООО"Системная Интеграция"\n'
                          'Распространяется под лицензией GNU GPLv.3 или выше\n'
                          'Email техподдержки: samson@itnov.ru'.format(version))

    def fill_organization_fields(self):
        for field in Organization.ALL_FIELDS:
            ui_field = getattr(self.ui, field)
            if self.organization[field] == '':
                ui_field.setText('<НЕ ЗАПОЛНЕНО>')
            else:
                ui_field.setText(self.organization[field])

    def organization_edit_btn_clicked(self):
        organization_data = self.organization
        organization_edit_dialog = OFView(organization_data=organization_data, parent=self)
        organization_edit_dialog.show()

    def menu_new_file_clicked(self):
        if not self.data_is_saved:
            answer = QMessageBox.question(self, 'Изменения еще не сохранены!',
                                          "Вы хотите сохранить изменения?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if answer == QMessageBox.Yes:
                if not self.save_file():
                    self.menu_save_file_as_clicked()
                    return
        self.clear_data()
        self.ui.menu_save.setEnabled(True)
        self.ui.menu_save_as.setEnabled(True)
        self.ui.menu_export_word.setEnabled(True)

    def menu_open_clicked(self):
        if not self.data_is_saved:
            answer = QMessageBox.question(self, 'Изменения еще не сохранены!',
                                          "Вы хотите сохранить изменения?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if answer == QMessageBox.Yes:
                if not self.save_file():
                    self.menu_save_file_as_clicked()
                    return
        # Если локальная переменная пуста, то открываем рабочий каталог по умолчанию.
        # Если в локальной переменной есть путь, то открываем эту директорию,
        path = os.getenv('HOME') if self.last_path is None else self.last_path
        filename = QtWidgets.QFileDialog.getOpenFileName(self, caption='Открыть файл', directory=path,
                                                         filter='XML Files (*.xml *.XML)')[0]
        self.load_file(filename)
        self.ui.menu_save.setEnabled(True)
        self.ui.menu_save_as.setEnabled(True)
        self.ui.menu_export_word.setEnabled(True)

    def menu_save_file_clicked(self):
        if not self.save_file():
            self.menu_save_file_as_clicked()

    def menu_save_file_as_clicked(self):
        now = datetime.now()
        date = now.strftime("%d.%m.%Y")
        path = os.getenv('HOME') if self.last_path is None else self.last_path
        filename = QtWidgets.QFileDialog.getSaveFileName(self, options='/Список сотрудников ({date})'.format(date=date),
                                                         caption='Сохранить файл', directory=path,
                                                         filter='XML Files (*.xml *.XML)')[0]
        self.save_file(filename)

    def menu_export_word_clicked(self):
        now = datetime.now()
        date = now.strftime("%d.%m.%Y")
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить файл',
                                                         '/Список сотрудников ({date})'.format(date=date),
                                                         filter='Word 2007 (.docx)|*.docx')[0]
        if filename != '':
            docx = DocxCreator()
            docx.create_file(self.organization, self.model.employees)
            try:
                docx.save_file(filename)
            except PermissionError:
                QMessageBox.critical(self, 'Сохранение невозможно!',
                                     "Не получилось сохранить файл."
                                     " Возможно у вас нет прав на редактирование этого файла"
                                     " или файл открыт в другой программе.",
                                     QMessageBox.Close, QMessageBox.Close)
            self.last_path = os.path.split(os.path.normpath(filename))[0]

    @pyqtSlot()
    def data_changed(self):
        """Слот для фиксирования изменений в данных"""
        self.data_is_saved = False
        self.update_window_title()
        self.ui.menu_save.setEnabled(True)
        self.ui.menu_save_as.setEnabled(True)
        self.ui.menu_export_word.setEnabled(True)

    def refresh_column_views(self):
        # Скрываем отмеченные в настройках колонки и отображаем остальные
        columns_to_hide = self.app_settings.get('appearance', 'sections_to_hide')
        columns_to_hide = set(columns_to_hide.split(', '))
        for column in Employee.ALL_FIELDS:
            if column in columns_to_hide:
                self.hide_column(column=column)
            else:
                self.show_column(column=column)

    def hide_checkbox_clicked(self):
        column_name = self.sender().objectName().replace('hide_col_', '')
        columns_to_hide = self.app_settings.get('appearance', 'sections_to_hide')
        if columns_to_hide == "":
            columns_to_hide = list()
        else:
            columns_to_hide = columns_to_hide.split(', ')
        if self.sender().isChecked():
            columns_to_hide.remove(column_name)
        else:
            columns_to_hide.append(column_name)
        self.app_settings.set('appearance', 'sections_to_hide', ", ".join(columns_to_hide))
        self.refresh_column_views()

    def clear_data(self):
        """Обнуляет состояние модели"""
        self.organization = Organization()
        self.fill_organization_fields()

        self.model = EmployeesListModel(Employees())
        self.proxy_model.setSourceModel(self.model)
        self.ui.employees_table.setModel(self.proxy_model)
        self.model.dataChanged.connect(self.data_changed)
        self.model.rowsAddRemove.connect(self.data_changed)

        self.filename = None
        self.data_is_saved = True
        self.update_window_title()

    def update_window_title(self):
        """Обновляет заголовок программы"""
        version = self.app_settings.get('system', 'version')
        tail = '' if self.data_is_saved else ' ●'
        self.setWindowTitle('СписокСотрудников (версия {}){}'.format(version, tail))

    def load_file(self, filename):
        """Загружает файл из указанного пути"""
        if filename == '':
            return

        xml_parser = XMLParser()
        if xml_parser.load_file(filename):
            if not xml_parser.validate():
                QMessageBox.critical(self, 'XML файл имеет ошибки!',
                                     '\n'.join(xml_parser.get_errors()),
                                     QMessageBox.Close, QMessageBox.Close)
            self.clear_data()
            self.filename = os.path.normpath(filename)
            self.last_path = os.path.split(filename)[0]
            self.organization = xml_parser.get_organization()
            self.fill_organization_fields()
            list_of_employees = xml_parser.get_employees()
            self.model = EmployeesListModel(list_of_employees)
            self.proxy_model.setSourceModel(self.model)
            self.ui.employees_table.setModel(self.proxy_model)
            self.model.dataChanged.connect(self.data_changed)
            self.model.rowsAddRemove.connect(self.data_changed)
        else:
            QMessageBox.critical(self, 'Ошибки при открытии файла!',
                                 '\n'.join(xml_parser.get_errors()),
                                 QMessageBox.Close, QMessageBox.Close)

    def save_file(self, filename=None):
        """Сохраняет файл"""
        if filename == '':
            return False

        filename = filename if filename is not None else self.filename
        if filename is None:
            return False

        xml_parser = XMLParser()
        if xml_parser.save_to_file(filename, self.organization, self.model.employees):
            self.data_is_saved = True
            self.update_window_title()
            self.filename = os.path.normpath(filename)
            self.last_path = os.path.split(filename)[0]
            return True
        else:
            return False
