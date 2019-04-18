import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTranslator
from PyQt5 import QtGui
from PyQt5 import QtCore
from utility.organization import Organization
from utility.employees import Employee, Employees
from utility.xml_parser import XMLParser
from model import EmployeesListModel as Model
from controller import Controller
from utility.resource_path import resource_path
from utility.settings import Settings


def prepare_app(app_var):
    app_settings = Settings()

    # Внешний вид приложения
    theme_style = app_settings.get('appearance', 'theme_style')  # default/fusion/fusion_dark
    if theme_style == 'fusion':
        app_var.setStyle('Fusion')
    elif theme_style == 'fusion_dark':
        app_var.setStyle('Fusion')
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
        palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(53, 53, 53).lighter())
        app_var.setPalette(palette)

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

    Controller(Model(list_of_employees), organization)
    sys.exit(app.exec_())
