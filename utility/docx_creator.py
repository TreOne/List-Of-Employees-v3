from docxtpl import DocxTemplate
from utility.employees import Employee
from utility.resource_path import resource_path
from datetime import datetime


class DocxCreator:
    def __init__(self):
        self.doc = DocxTemplate(resource_path('./resources/template_print_list.docx'))

    def create_file(self, organization, employees):
        employees = employees.copy()
        organization = organization.copy()
        list_for_print = dict()

        address = organization['org_address']
        max_length = 50
        # TODO: Плохая проверка на пустой адресс AttributeError: 'NoneType' object has no attribute 'find'
        if len(address) > 50:
            try:
                split_char = address.find(' ', max_length)
                org_address_line_1 = address[:split_char]
                org_address_line_2 = address[split_char:]
            except AttributeError:
                org_address_line_1 = ''
                org_address_line_2 = ''
        else:
            org_address_line_1 = address
            org_address_line_2 = ''

        now = datetime.now()
        date = now.strftime("%d.%m.%Y")
        for i, employee in enumerate(employees.values()):
            list_for_print[i] = dict()
            list_for_print[i]['i'] = i + 1
            for field in Employee.ALL_FIELDS:
                if field == 'birth_date':
                    birth_date = datetime.strptime(employee['birth_date'], '%Y-%m-%d')
                    list_for_print[i]['birth_date'] = birth_date.strftime("%d.%m.%Y")
                    continue
                if field in Employee.LIST_FIELDS:
                    list_for_print[i][field] = " / ".join(employee[field])
                else:
                    list_for_print[i][field] = employee[field]

        context = {'head_full_name': organization['head_full_name'],
                   'org_name': organization['org_name'],
                   'org_address_line_1': org_address_line_1,
                   'org_address_line_2': org_address_line_2,
                   'date': date,
                   'year': now.year,
                   'representative_position': organization['representative_position'],
                   'representative_full_name': organization['representative_full_name'],
                   'employees': list_for_print.values()}
        self.doc.render(context)

    def save_file(self, filename):
        self.doc.save(filename)
