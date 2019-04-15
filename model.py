from datetime import datetime
from utility.employees import Employee
from utility.words import smart_ending
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class EmployeesListModel(QtCore.QAbstractTableModel):
    SortRole = QtCore.Qt.UserRole + 1

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
                str_birth_date = self.employees[emp_id]['birth_date']
                return QtCore.QDate.fromString(str_birth_date, 'yyyy-MM-dd')
            if field_name == 'experience':
                experience = self.employees[emp_id]['experience']
                return int(experience)
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
        self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole,))
        return True


class EmployeesSortModel(QtCore.QSortFilterProxyModel):

    def lessThan(self, left, right):
        """Сортирует данные столбцов в таблице сотрудников"""
        lvalue = left.data(role=EmployeesListModel.SortRole)
        rvalue = right.data(role=EmployeesListModel.SortRole)
        return lvalue < rvalue
