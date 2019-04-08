import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator
from utility.orfanization import Organization
from utility.employees import Employee, Employees
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
    list_of_employees.rem_employee(2)
    employee = list_of_employees.add_empty_employee()
    employee.family_name = 'Иванов'
    employee.first_name = 'Иван'
    # employee.patronymic = 'Иванович'
    employee.hazard_types = ['1', '2', '3']

    print(employee)

    # for k, v in employee:
    #     print('{} -> {}'.format(k, v))
    #
    # organization = Organization()
    # for field_name in organization.ALL_FIELDS:
    #     setattr(organization, field_name, 'Значение для поля: "{}"'.format(field_name))
    #
    # print(organization)
    #
    # for k, v in organization:
    #     print('{} -> {}'.format(k, v))

    for emp_id, employee in list_of_employees:
        print('{} -> {}'.format(emp_id, employee))

    Controller(Model(list_of_employees.get_employees()))
    sys.exit(app.exec_())
