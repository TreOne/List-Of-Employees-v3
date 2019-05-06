from utility.employees import Employee, Employees
from utility.resource_path import resource_path
from openpyxl import load_workbook
from collections import Counter
import re


class XLSXParser:
    """
    Класс XLSXParser служит для импорта XLSX файлов.
    """

    def __init__(self):
        self.__xlsx_filename = None
        self.__employees = Employees()
        self.__errors = list()
        self.__warnings = list()

    def __reset_state(self):
        self.__xlsx_filename = None
        self.__employees = Employees()
        self.__errors = list()
        self.__warnings = list()

    def get_employees(self):
        return self.__employees

    def get_errors(self):
        return self.__errors

    def get_warnings(self):
        return self.__warnings

    def load_file(self, filename):
        """Разбирает XLSX файл и заполняет данными список сотрудников"""
        self.__reset_state()

        # Пробуем открыть файл
        try:
            wb = load_workbook(filename)
            first_sheet_name = wb.sheetnames[0]
            ws = wb[first_sheet_name]
        except OSError:
            self.__errors.append('ERROR: XLSX файл по пути "' + filename + '" не найден.')
            return False
        self.__xlsx_filename = filename

        excel_employees = ws.rows

        for excel_employee in excel_employees:
            # Пропускаем шапку таблицы
            if excel_employee[0].row == 1:
                continue
            employee = self.employee_from_row(excel_employee)
            self.__employees.add(employee)
        return True

    def employee_from_row(self, excel_row):
        new_employee = Employee()
        employee_full_name = " ".join((str(excel_row[0].value), str(excel_row[1].value), str(excel_row[2].value)))
        for field in Employee.ALL_FIELDS:
            field_id = Employee.ALL_FIELDS.index(field)

            # Проверка форматов ячеек
            if str(type(excel_row[field_id].value)) != str(type(None)):
                if field == 'birth_date':
                    if str(type(excel_row[field_id].value)) != "<class 'datetime.datetime'>":
                        self.__warnings.append("WARNING: Формат ячейки 'Дата рождения' сотрудника {} не является датой."
                                               " Пожалуйста, проверьте формат ячейки. Она должа иметь формат 'Дата'."
                                               .format(employee_full_name))
                        excel_row[field_id].value = None
                elif field == 'experience':
                    if str(type(excel_row[field_id].value)) != "<class 'int'>":
                        self.__warnings.append("WARNING: Формат ячейки 'Стаж' сотрудника {} не является числом. "
                                               "Пожалуйста, проверьте формат ячейки. Она должа иметь формат 'Числовой'."
                                               .format(employee_full_name))
                        excel_row[field_id].value = ''
                else:
                    if str(type(excel_row[field_id].value)) != "<class 'str'>":
                        self.__warnings.append("WARNING: Формат ячейки '{}' сотрудника {} не является текстовым. "
                                               "Пожалуйста, проверьте формат ячейки. Она должа иметь формат 'Текст'."
                                               .format(Employee.translate(field), employee_full_name))
                        excel_row[field_id].value = ''

            # аие полей сотрудника
            if field in Employee.LIST_FIELDS:
                if excel_row[field_id].value is None:
                    value = list()
                else:
                    value = str(excel_row[field_id].value).split(',')
                    value = list(map(str.strip, value))
            else:
                value = '' if excel_row[field_id].value is None else excel_row[field_id].value

            if field in Employee.LIST_FIELDS:
                new_employee[field] = value
            elif field == 'birth_date':
                if value != '':
                    value = value.strftime("%Y-%m-%d")
                new_employee[field] = value
            elif field == 'sex':
                if value in ('Мужской', 'Женский', ''):
                    new_employee[field] = value
                else:
                    self.__warnings.append("WARNING: Ячейка 'Пол' сотрудника {} заполнена неправильно. "
                                           "Пожалуйста, проверьте текст ячейки. "
                                           "Она должа содержать одно из двух значений: 'Мужской' или 'Женский'."
                                           .format(employee_full_name))
                    new_employee[field] = ''
            else:
                new_employee[field] = str(value)
        return new_employee
