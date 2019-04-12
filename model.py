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

    def flags(self, q_model_index):
        row = q_model_index.row()
        column = q_model_index.column()
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
        if qt_orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            field_name = Employee.ALL_FIELDS[section]
            return Employee.translate(field_name)
        if qt_orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return section + 1

    def data(self, q_model_index, role=None):
        row = q_model_index.row()
        column = q_model_index.column()
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

    def setData(self, q_model_index, value, role=QtCore.Qt.EditRole):
        row = q_model_index.row()
        column = q_model_index.column()
        field_name = Employee.ALL_FIELDS[column]
        emp_id = tuple(self.employees.keys())[row]
        self.employees[emp_id][field_name] = value
        self.dataChanged.emit(q_model_index, q_model_index, (QtCore.Qt.DisplayRole, ))
        return True

