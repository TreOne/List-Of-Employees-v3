from PyQt5 import QtCore
from utility.employees import Employee
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class EmployeesListModel(QtCore.QAbstractTableModel):
    def __init__(self, list_of_employees):
        QtCore.QAbstractTableModel.__init__(self)
        self.employees = list_of_employees

    def flags(self, q_model_index):
        row = q_model_index.row()
        column = q_model_index.column()
        field_name = Employee.ALL_FIELDS[column]
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
            if field_name in Employee.LIST_FIELDS:
                return ", ".join(self.employees[emp_id][field_name])
            return self.employees[emp_id][field_name]

    def setData(self, q_model_index, value, role=QtCore.Qt.EditRole):
        row = q_model_index.row()
        column = q_model_index.column()
        field_name = Employee.ALL_FIELDS[column]
        emp_id = tuple(self.employees.keys())[row]
        self.employees[emp_id][field_name] = value
        self.dataChanged.emit(q_model_index, q_model_index, (QtCore.Qt.DisplayRole, ))
        return True

