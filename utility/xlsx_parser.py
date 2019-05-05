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
        # TODO: Реализовать парсер по примеру из self.get_data_from_xlsx()

        return True

    def get_data_from_xlsx(self, filename=''):
        wb = load_workbook(filename)
        first_sheet_name = wb.sheetnames[0]
        ws = wb[first_sheet_name]
        lines = list()
        names = list()
        birthdays = list()
        policy_regex = r"(\d+-\d+)-(\d+)"
        policy_series = list()
        policy_numbers = list()
        policy_start = list()
        policy_end = list()
        errors = list()

        # Добавляем имена и даты рождений в списки
        for cell in ws['C']:
            if cell.value is None:
                errors.append('ERROR: В ячейке [' + cell.coordinate + '] не заполненно Имя!')
            names.append(cell.value)
            lines.append(cell.row + 1)
        for cell in ws['D']:
            if cell.value is None:
                errors.append('ERROR: В ячейке [' + cell.coordinate + '] не заполненна Дата Рождения!')
            birthdays.append(cell.value)
        for cell in ws['B']:
            if cell.value is None:
                errors.append('ERROR: В ячейке [' + cell.coordinate + '] не заполненн Полис!')
                continue
            policy_data = re.search(policy_regex, cell.value)
            if policy_data is not None and len(policy_data.groups()) == 2:
                policy_series.append(policy_data.group(1))
                policy_numbers.append(policy_data.group(2))
            else:
                policy_series.append(None)
                policy_numbers.append(None)
        for cell in ws['H']:
            if cell.value is None:
                errors.append('ERROR: В ячейке [' + cell.coordinate + '] не заполненна Дата Начала!')
            policy_start.append(cell.value)
        for cell in ws['I']:
            if cell.value is None:
                errors.append('ERROR: В ячейке [' + cell.coordinate + '] не заполненна Дата Окончания!')
            policy_end.append(cell.value)

        # Удаляем заголовки колонок и собираем 4 списка в один
        names.pop(0)
        birthdays.pop(0)
        policy_series.pop(0)
        policy_numbers.pop(0)
        policy_start.pop(0)
        policy_end.pop(0)
        clients = list(zip(names, birthdays, policy_series, policy_numbers, lines, policy_start, policy_end))

        return clients
