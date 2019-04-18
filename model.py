import math
from datetime import datetime
from PyQt5.QtCore import QVariant, pyqtSignal
from utility.employees import Employee, Validate
from utility.words import smart_ending
from PyQt5 import QtCore
from PyQt5 import QtGui


class EmployeesListModel(QtCore.QAbstractTableModel):
    SortRole = QtCore.Qt.UserRole + 1
    rowsAddRemove = pyqtSignal()

    def __init__(self, list_of_employees):
        QtCore.QAbstractTableModel.__init__(self)
        self.employees = list_of_employees

    def flags(self, index):
        if not index.isValid():
            return QVariant()
        column = index.column()
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
                if self.employees[emp_id]['birth_date'] == '':
                    return ''
                birth_date = datetime.strptime(self.employees[emp_id]['birth_date'], '%Y-%m-%d')
                age = datetime.now() - birth_date
                age = math.trunc(age.days / 365)
                age = "{} {}".format(age, smart_ending(age, 'год', 'года', 'лет'))
                return "{} ({})".format(birth_date.strftime("%d.%m.%Y"), age)

            if field_name == 'experience':
                if self.employees[emp_id]['experience'] == '':
                    return ''
                experience = self.employees[emp_id]['experience']
                return experience + smart_ending(int(experience), ' год', ' года', ' лет')

            if field_name in Employee.LIST_FIELDS:
                return " / ".join(self.employees[emp_id][field_name])

            return self.employees[emp_id][field_name]

        # Фон при ошибке в поле сотрудника
        if role == QtCore.Qt.BackgroundRole:
            validator = self.employees[emp_id].field_validation(field_name)
            if validator.result == Validate.INVALID:
                color = QtGui.QColor.fromRgbF(1, 0, 0, 0.1)
                brush = QtGui.QBrush(color)
                return brush
            if validator.result == Validate.WARNING:
                color = QtGui.QColor.fromRgbF(1, 1, 0, 0.1)
                brush = QtGui.QBrush(color)
                return brush

        # Подсказка при ошибке в поле сотрудника
        if role == QtCore.Qt.ToolTipRole:
            validator = self.employees[emp_id].field_validation(field_name)
            if validator.result != Validate.VALID:
                return validator.text

        # Сортировка
        if role == EmployeesListModel.SortRole:
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

        # Редактирование
        if role == QtCore.Qt.EditRole:
            if field_name == 'birth_date':
                if self.employees[emp_id]['birth_date'] == '':
                    return QtCore.QDate.fromString('1900-01-01', 'yyyy-MM-dd')
                str_birth_date = self.employees[emp_id]['birth_date']
                return QtCore.QDate.fromString(str_birth_date, 'yyyy-MM-dd')

            if field_name == 'experience':
                if self.employees[emp_id]['experience'] == '':
                    return 0
                experience = self.employees[emp_id]['experience']
                return int(experience)

            if field_name == 'sex':
                if self.employees[emp_id]['sex'] == '':
                    return 'Мужской'

            if field_name in Employee.LIST_FIELDS:
                return self.employees[emp_id][field_name]

            return index.data(role=QtCore.Qt.DisplayRole)

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
        if field_name in self.employees.get_completer_fields():
            self.employees.refresh_completer(field_name)
        self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole,))
        return True

    def insertRow(self):
        row_pos = self.rowCount()
        self.beginInsertRows(QtCore.QModelIndex(), row_pos, row_pos)
        self.employees.add()
        self.endInsertRows()
        self.rowsAddRemove.emit()
        return True

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        emp_id = tuple(self.employees.keys())[row]
        self.beginRemoveRows(parent, row, row)
        self.employees.pop(emp_id)
        self.endRemoveRows()
        self.rowsAddRemove.emit()
        return True

    def get_completer(self, completer_field):
        return self.employees.get_completer(completer_field)


class EmployeesSortModel(QtCore.QSortFilterProxyModel):

    def lessThan(self, left, right):
        """Сортирует данные столбцов в таблице сотрудников"""
        lvalue = left.data(role=EmployeesListModel.SortRole)
        rvalue = right.data(role=EmployeesListModel.SortRole)
        return lvalue < rvalue

    def insertRow(self):
        return self.sourceModel().insertRow()

    def removeRows(self, selected_indexes):
        # При удалении сразу нескольких сотрудников возникают проблемы с переиндексацией
        proxy_index = selected_indexes[0]
        source_index = self.mapToSource(proxy_index)
        self.sourceModel().removeRow(source_index.row(), source_index.parent())
