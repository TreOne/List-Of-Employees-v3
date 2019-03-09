from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class EmployeesListModel(QtCore.QAbstractTableModel):
    def __init__(self, list_of_employees):
        QtCore.QAbstractTableModel.__init__(self)
        self.employees = list_of_employees
        self.columns = ['ID', 'ФИО', 'Дата рождения']

    def flags(self, q_model_index):
        if q_model_index.column() >= 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def rowCount(self, *args, **kwargs):
        return len(self.employees.keys())

    def columnCount(self, *args, **kwargs):
        return len(self.columns)

    def headerData(self, section, qt_orientation, role=QtCore.Qt.DisplayRole):
        if qt_orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.columns[section]
        if qt_orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return section + 1

    def data(self, q_model_index, role=None):
        row = q_model_index.row()
        column = q_model_index.column()

        if role == QtCore.Qt.DisplayRole:
            return str(row) + str(column)

    def setData(self, q_model_index, value, role=QtCore.Qt.EditRole):
        row = q_model_index.row()
        column = q_model_index.column()
        self.dataChanged.emit(q_model_index, q_model_index, (QtCore.Qt.DisplayRole, ))
        return True

