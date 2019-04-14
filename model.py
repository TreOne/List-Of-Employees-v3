from datetime import datetime
from PyQt5 import QtCore
from utility.employees import Employee
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import utility.resources
from utility.words import smart_ending


class EmployeesListModel(QtCore.QAbstractTableModel):
    def __init__(self, list_of_employees):
        QtCore.QAbstractTableModel.__init__(self)
        self.employees = list_of_employees

    def flags(self, index):
        row = index.row()
        column = index.column()
        field_name = Employee.ALL_FIELDS[column]
        # Отображаем иконку вместо текста в колонке "Пол"
        if field_name in Employee.LIST_FIELDS:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
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
        """Предоставляет данные из модели"""
        if not index.isValid():
            return
        row = index.row()
        column = index.column()
        field_name = Employee.ALL_FIELDS[column]
        emp_id = tuple(self.employees.keys())[row]

        if role == QtCore.Qt.DisplayRole:
            if field_name == 'birth_date':
                birth_date = datetime.strptime(self.employees[emp_id]['birth_date'], '%Y-%m-%d')
                return birth_date.strftime("%d.%m.%Y")

            if field_name == 'experience':
                experience = self.employees[emp_id]['experience']
                return experience + smart_ending(int(experience), ' год', ' года', ' лет')

            if field_name in Employee.LIST_FIELDS:
                return ", ".join(self.employees[emp_id][field_name])
            return self.employees[emp_id][field_name]

        if role == QtCore.Qt.DecorationRole:
            if field_name == "sex":
                gender = self.employees[emp_id]['sex']
                if gender == 'Мужской':
                    return QtGui.QIcon(':/icons/male.svg')
                elif gender == 'Женский':
                    return QtGui.QIcon(':/icons/female.svg')

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
    #
    # def sort(self, column, order=QtCore.Qt.AscendingOrder):
    #     """ Реализация сортировки столбцов """
    #     self.layoutAboutToBeChanged.emit()
    #     ascending = (order == QtCore.Qt.AscendingOrder)
    #     column_name = Employee.ALL_FIELDS[column]
    #     print(column_name)
    #
    #
    #
    #
    #     # self.changePersistentIndexList(oldIndexList, newIndexList)
    #     self.layoutChanged.emit()
    #     self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

        #
        #
        #
        # # Storing persistent indexes
        # self.layoutAboutToBeChanged.emit()
        # oldIndexList = self.persistentIndexList()
        # oldIds = self._dfDisplay.index.copy()
        #
        # # Sorting data
        # column = self._dfDisplay.columns[col]
        # ascending = (order == QtCore.Qt.AscendingOrder)
        # if column in self._sortBy:
        #     i = self._sortBy.index(column)
        #     self._sortBy.pop(i)
        #     self._sortDirection.pop(i)
        # self._sortBy.insert(0, column)
        # self._sortDirection.insert(0, ascending)
        # self.updateDisplay()
        #
        # # Updating persistent indexes
        # newIds = self._dfDisplay.index
        # newIndexList = []
        # for index in oldIndexList:
        #     id = oldIds[index.row()]
        #     newRow = newIds.get_loc(id)
        #     newIndexList.append(self.index(newRow, index.column(), index.parent()))
        # self.changePersistentIndexList(oldIndexList, newIndexList)
        # self.layoutChanged.emit()
        # self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())


class EmployeesSortModel(QtCore.QSortFilterProxyModel):

    def lessThan(self, left, right):
        # TODO: Доделать
        left_row = left.row()
        left_column = left.column()
        left_field_name = Employee.ALL_FIELDS[left_column]
        left_emp_id = tuple(self.employees.keys())[left_row]

        right_row = right.row()
        right_column = right.column()
        right_field_name = Employee.ALL_FIELDS[right_column]
        right_emp_id = tuple(self.employees.keys())[right_row]

        if left_field_name == 'experience' and right_field_name == 'experience':
            return int(self.employees[left_emp_id]['experience']) < int(self.employees[right_emp_id]['experience'])
        else:
            return QtCore.QAbstractTableModel.lessThan(left, right)
