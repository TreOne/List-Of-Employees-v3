from datetime import datetime
from utility.employees import Employee
from utility.words import smart_ending
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class EmployeesListModel(QtCore.QAbstractTableModel):
    def __init__(self, list_of_employees):
        QtCore.QAbstractTableModel.__init__(self)
        self.employees = list_of_employees

    def flags(self, index):
        row = index.row()
        column = index.column()
        field_name = Employee.ALL_FIELDS[column]
        # TODO: раскомментировать
        # if field_name in Employee.LIST_FIELDS:
        #     return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        if column >= 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def rowCount(self, *args, **kwargs):
        return len(self.employees.keys())

    def columnCount(self, *args, **kwargs):
        return len(Employee.ALL_FIELDS)

    def headerData(self, section, qt_orientation, role=QtCore.Qt.DisplayRole):
        """Предоставляет данные о заголовках таблицы"""
        if qt_orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            field_name = Employee.ALL_FIELDS[section]
            return Employee.translate(field_name)
        if qt_orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return section + 1

    def data(self, index, role=None):
        """Предоставляет данные из модели в зависимости от роли"""
        if not index.isValid():
            return
        row = index.row()
        column = index.column()
        field_name = Employee.ALL_FIELDS[column]
        emp_id = tuple(self.employees.keys())[row]

        # Отображение
        if role == QtCore.Qt.DisplayRole:
            if field_name == 'birth_date':
                birth_date = datetime.strptime(self.employees[emp_id]['birth_date'], '%Y-%m-%d')
                return birth_date.strftime("%d.%m.%Y")

            if field_name == 'experience':
                experience = self.employees[emp_id]['experience']
                return experience + smart_ending(int(experience), ' год', ' года', ' лет')

            if field_name in Employee.LIST_FIELDS:
                return ", ".join(self.employees[emp_id][field_name])
                # return self.employees[emp_id][field_name]

            return self.employees[emp_id][field_name]

        # Сортировка
        if role == QtCore.Qt.UserRole:
            if field_name == 'birth_date':
                str_birth_date = self.employees[emp_id]['birth_date']
                birth_date = datetime.strptime(str_birth_date, "%Y-%m-%d")
                now = datetime.today()
                delta = now - birth_date
                return delta.days

            if field_name == 'experience':
                experience = self.employees[emp_id]['experience']
                return int(experience)

            if field_name in Employee.LIST_FIELDS:
                return len(self.employees[emp_id][field_name])

            return index.data(role=QtCore.Qt.DisplayRole).lower().replace('ё', 'е')

        # Иконка
        if role == QtCore.Qt.DecorationRole:
            if field_name == 'sex':
                gender = self.employees[emp_id]['sex']
                if gender == 'Мужской':
                    return QtGui.QIcon(':/icons/male.svg')
                elif gender == 'Женский':
                    return QtGui.QIcon(':/icons/female.svg')

        # Выравнивание
        if role == QtCore.Qt.TextAlignmentRole:
            align_to_center = ('sex', 'experience', 'birth_date')
            if field_name in align_to_center:
                return QtCore.Qt.AlignCenter

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """Записывает данные в модель"""
        if not index.isValid():
            return
        row = index.row()
        column = index.column()
        field_name = Employee.ALL_FIELDS[column]
        emp_id = tuple(self.employees.keys())[row]
        self.employees[emp_id][field_name] = value
        self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole,))
        return True


class EmployeesSortModel(QtCore.QSortFilterProxyModel):

    def lessThan(self, left, right):
        """Сортирует данные столбцов в таблице сотрудников"""
        lvalue = left.data(role=QtCore.Qt.UserRole)
        rvalue = right.data(role=QtCore.Qt.UserRole)
        return lvalue > rvalue


class EmployeesHazardsDelegate(QtWidgets.QStyledItemDelegate):
    """Тестовый делегат"""

    def __init__(self, parent=None):
        """Инициализация делегата"""
        print("Вызван метод init")
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        """Создание редактора"""
        print("Вызван метод createEditor")
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        """Передача данных в редактор"""
        print("Вызван метод setEditorData")
        return super().setEditorData(editor, index)

    # def setModelData(self, editor, model, index):
        # row = index.row()
        # column = index.column()
        # field_name = Employee.ALL_FIELDS[column]
        # emp_id = tuple(self.employees.keys())[row]
        #
        # if field_name in Employee.LIST_FIELDS:
        #     return len(self.employees[emp_id][field_name])
        #
        # data_int = editor.value()
        # data_var = QVariant(data_int)


        # model.setData(index, self.__generate_hazard_cell(editor.text()))
        # print(editor, model, index)


    @staticmethod
    def __generate_hazard_cell(hazard_codes):
        """Создает ряд скругленных ячеек вредностей для таблицы"""
        if type(hazard_codes) == str:
            hazard_codes = hazard_codes.split(',')
        hazards_layout = QtWidgets.QHBoxLayout()
        hazards_cell = QtWidgets.QWidget()
        hazards_cell.setLayout(hazards_layout)
        for hazard_code in hazard_codes:
            if hazard_code.endswith('.'):
                hazard_code = hazard_code[:-1]
            hazard_label = QtWidgets.QLabel(hazard_code)
            hazard_label.setStyleSheet('background-color: #fff; border-radius: 5px; padding: 2px;'
                                       'min-height: 15px; border: 1px solid;')
            hazards_layout.addWidget(hazard_label)
        h_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding)
        hazards_layout.addSpacerItem(h_spacer)
        return hazards_cell
