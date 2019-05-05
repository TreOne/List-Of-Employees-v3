# coding=utf-8
from openpyxl import load_workbook
from collections import Counter
import re


def get_data_from_xlsx(filename=''):
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

    # Есть ли дубли (имя, д/р) в файле?
    for item, count in Counter(zip(names, birthdays)).items():
        if count > 1:
            errors.append('ERROR: Запись {name} ({b_date}) найдена в файле {count} раза!'.
                          format(name=item[0] if item[0] is not None else '[НЕ ЗАПОЛНЕННО]',
                                 b_date=item[1].strftime("%d.%m.%Y") if item[1] is not None else 'д/р отсутствует',
                                 count=count))

    # Есть ли дубли полисов в файле?
    for item, count in Counter(zip(policy_series, policy_numbers)).items():
        if count > 1:
            errors.append('ERROR: Полис с/н: {series}-{number} найден в файле {count} раза!'.
                          format(series=item[0] if item[0] is not None else '[НЕ ЗАПОЛНЕННО]',
                                 number=item[1] if item[1] is not None else '[НЕ ЗАПОЛНЕННО]',
                                 count=count))

    # Если есть ошибки в xls файле, то ничего не вносим в базу
    if len(errors) > 0:
        for error in errors:
            print(error)
        return None

    return clients


if __name__ == '__main__':
    get_data_from_xlsx(filename='xlsx/671.xlsx')
