from utility.employees import Employee, Employees
from utility.organization import Organization
from lxml import etree as et_xml
import datetime


class XMLParser:
    """
    Класс XMLParser служит для работы c XML файлами (открытие файла, разбор данных и сохранение изменений).
    """

    def __init__(self):
        self.__xml_filename = None
        self.__root = None
        self.__employees = Employees()
        self.__organization = Organization()
        self.__errors = list()

    def __reset_state(self):
        self.__xml_filename = None
        self.__root = None
        self.__employees = Employees()
        self.__organization = Organization()
        self.__errors = list()

    def get_organization(self):
        return self.__organization

    def get_employees(self):
        return self.__employees

    def load_file(self, filename):
        self.__reset_state()

        # Пробуем открыть файл
        try:
            tree = et_xml.ElementTree(file=filename)
            self.__xml_filename = ''
        except OSError:
            self.__errors.append('ERROR: XML файл по пути "' + self.__xml_filename + '" не найден.')
            return False

        # Корень древа - register?
        if tree.getroot().tag != 'register':
            print('ERROR: Не обнаружен тег <register> в XML файле. Выбран не тот файл?')
            return False
        else:
            self.__root = tree.getroot()

        self.__fill_organization()
        self.__fill_employees()
        return True

    def save_to_file(self, filename, organization, employees):
        if filename is None:
            print('ERROR: Не указано место сохранения файла.')
            return False
        root = et_xml.Element('register')

        # Дата создания документа
        date = et_xml.SubElement(root, 'date')
        now = datetime.datetime.now()
        date.text = now.strftime("%d.%m.%Y")

        # Заполняем тег <organization>
        organization_node = et_xml.SubElement(root, 'organization')
        for field in Organization.ALL_FIELDS:
            node = et_xml.SubElement(organization_node, field)
            node.text = organization.get(field, '')

        # Заполняем данные сотрудников
        for employee in employees.values():
            employee_node = et_xml.SubElement(root, 'employee')
            # Заполняем корневой тег <employee> сотрудника
            for field in Employee.PERSON_FIELDS:
                node = et_xml.SubElement(employee_node, field)
                node.text = employee[field]
            # Заполняем тег <job> сотрудника
            job_node = et_xml.SubElement(employee_node, 'job')
            for field in Employee.JOB_FIELDS:
                if field not in ('hazard_types', 'hazard_factors'):
                    node = et_xml.SubElement(job_node, field)
                    node.text = employee[field]
                else:
                    hazard_node = et_xml.SubElement(job_node, field)
                    for hazard in employee[field]:
                        code = et_xml.SubElement(hazard_node, 'code')
                        code.text = hazard

        save_tree = et_xml.ElementTree(root)
        save_tree.write(filename, pretty_print=True, encoding="utf-8", xml_declaration=True)
        return True

    def __fill_organization(self):
        organization = self.__root.find('organization')
        if organization is None:
            print('WARNING: В XML файле отсутствует тег <organization>.')
            for field in Organization.ALL_FIELDS:
                self.__organization[field] = ''
        else:
            for field in Organization.ALL_FIELDS:
                try:
                    self.__organization[field] = organization.find(field).text
                except AttributeError:
                    self.__organization[field] = ''
                    print('WARNING: Не найден тег <organization>/<' + field + '> в XML файле.')

    def __fill_employees(self):
        employees_count = len(self.__root.findall('employee'))
        if employees_count < 1:
            print('WARNING: В XML файле не обнаружен ни один сотрудник.')
            return

        for i, employee in enumerate(self.__root.iter("employee")):
            # Заполняем основные поля сотрудника
            add_employee = dict()
            for field in Employee.PERSON_FIELDS:
                if employee.find(field) is None or employee.find(field).text is None:
                    print('WARNING: У сотрудника ' + str(i) + ' не заполнено поле ' + field)
                    add_employee[field] = ''
                    if field == 'sex':
                        add_employee['sex'] = 'Не указан'
                else:
                    add_employee[field] = employee.find(field).text

            # Заполняем поля работы сотрудника
            job = employee.find('job')
            # Если у сотрудника отсутствует тег <job> то заполняем его пустыми полями
            if job is None:
                print('WARNING: У сотрудника ' + str(i) + ' пропущен тег <job>')
                for field in Employee.JOB_FIELDS:
                    if field in ('hazard_types', 'hazard_factors'):
                        add_employee[field] = list()
                    else:
                        add_employee[field] = ''
            else:
                # Иначе заполняем данными из файла
                for field in Employee.JOB_FIELDS:
                    if job.find(field) is None or job.find(field).text is None:
                        print('WARNING: У сотрудника ' + str(i) + ' не заполнено поле ' + field)
                        if field in ('hazard_types', 'hazard_factors'):
                            add_employee[field] = list()
                        else:
                            add_employee[field] = ''
                            continue
                    else:
                        if field not in ('hazard_types', 'hazard_factors'):
                            add_employee[field] = job.find(field).text
                        else:
                            # Если это список вредностей то перебираем его
                            hazards_count = len(job.findall(field + '/code'))
                            hazards = list()
                            if hazards_count > 0:
                                for hazard in employee.iterfind('job/' + field + '/code'):
                                    if hazard.text is not None:
                                        hazards.append(hazard.text)
                                    else:
                                        print('WARNING: Пустое поле "code" у сотрудника ' + str(i))
                            add_employee[field] = hazards

            self.__employees[i] = add_employee
