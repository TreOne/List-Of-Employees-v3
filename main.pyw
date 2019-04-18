import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTranslator
from PyQt5 import QtGui
from PyQt5 import QtCore
from utility.organization import Organization
from utility.employees import Employee, Employees
from utility.xml_parser import XMLParser
from model import EmployeesListModel as Model
from utility.resource_path import resource_path
from utility.settings import Settings
from view.mw_view import MWView


def prepare_app(app_var):
    app_settings = Settings()

    # Внешний вид приложения
    theme_style = app_settings.get('appearance', 'theme_style')  # default/fusion
    if theme_style == 'fusion':
        app_var.setStyle('Fusion')

    # Руссификация интерфейса QT
    translator = QTranslator(app_var)
    translator.load(resource_path('resources/qtbase_ru.qm'))
    app_var.installTranslator(translator)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    # Настройки внешнего вида, руссификация интерфейса и пр.
    prepare_app(app)

    # Парсинг XML в Employees и Organization
    xml_parser = XMLParser()
    xml_parser.load_file(resource_path('tests/demo_data.xml'))
    print('\n'.join(xml_parser.get_errors()))
    xml_parser.validate()
    print('\n'.join(xml_parser.get_errors()))
    list_of_employees = xml_parser.get_employees()
    organization = xml_parser.get_organization()

    # organization = xml_parser.get_organization()
    # organization.show()

    # xml_parser.load_file('tests/test_list_of_employees.xml')

    # print(list_of_employees)
    # print(new_list_of_employees)
    # print(employee['full_name'])
    #
    # for k, v in employee.genders():
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
    # for emp_id, employee in list_of_employees.genders():
    #     print('{} -> {}'.format(emp_id, employee))

    # null_employees = Employees()
    # for k, v in null_employees:
    #     print('{} -> {}'.format(k, v))

    MWView(model=Model(list_of_employees), organization=organization, autoload_ui=True)
    sys.exit(app.exec_())
