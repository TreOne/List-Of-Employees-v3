import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator
from utility.employees import Employees
from model import EmployeesListModel as Model
from controller import Controller
from utility.resource_path import resource_path


if __name__ == '__main__':

    app = QApplication(sys.argv)
    translator = QTranslator(app)
    translator.load(resource_path('utility/qtbase_ru.qm'))
    app.installTranslator(translator)

    list_of_employees = Employees()
    list_of_employees.add_empty_employee()
    list_of_employees.add_empty_employee()
    list_of_employees.add_empty_employee()
    employee = list_of_employees.add_empty_employee()
    employee.family_name = 'Иванов'
    employee.first_name = 'Иван'
    # employee.patronymic = 'Иванович'
    employee.hazard_types = ['1', '2', '3']

    # print(employee)

    Controller(Model(list_of_employees.get_employees()))
    sys.exit(app.exec_())
