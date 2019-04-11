import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTranslator
from utility.organization import Organization
from utility.employees import Employee, Employees
from utility.xml_parser import XMLParser
from model import EmployeesListModel as Model
from controller import Controller
from utility.resource_path import resource_path


if __name__ == '__main__':

    app = QApplication(sys.argv)
    translator = QTranslator(app)
    translator.load(resource_path('utility/qtbase_ru.qm'))
    app.installTranslator(translator)

    xml_parser = XMLParser()
    xml_parser.load_file(resource_path('tests/test_list_of_employees.xml'))
    for error in xml_parser.get_errors():
        print(error)

    list_of_employees = xml_parser.get_employees()
    organization = xml_parser.get_organization()

    # print(list_of_employees)

    # xml_parser._log_tree()
    xml_parser.validate()
    for error in xml_parser.get_errors():
        print(error)

    # organization = xml_parser.get_organization()
    # organization.show()

    # xml_parser.load_file('tests/test_list_of_employees.xml')

    # print(list_of_employees)
    # print(new_list_of_employees)
    # print(employee['full_name'])
    #
    # for k, v in employee.items():
    #     print('{} -> {}'.format(k, v))

    # organization = Organization()
    # for field_name in organization.keys():
    #     organization[field_name] = 'Значение для поля: "{}"'.format(field_name)
    #
    # organization.show()
    #
    # for k, v in organization:
    #     print('{} -> {}'.format(k, v))
    #
    # for emp_id, employee in list_of_employees.items():
    #     print('{} -> {}'.format(emp_id, employee))

    # null_employees = Employees()
    # for k, v in null_employees:
    #     print('{} -> {}'.format(k, v))

    Controller(Model(list_of_employees.get_employees()))
    sys.exit(app.exec_())
