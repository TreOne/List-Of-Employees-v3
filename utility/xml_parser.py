from utility.employees import Employee, Employees
from utility.organization import Organization
from lxml import etree
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

    def get_errors(self):
        return self.__errors

    def load_file(self, filename):
        self.__reset_state()

        # Пробуем открыть файл
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.ElementTree(file=filename, parser=parser)
        except OSError:
            self.__errors.append('ERROR: XML файл по пути "' + filename + '" не найден.')
            return False
        except etree.XMLSyntaxError:
            self.__errors.append('ERROR: Не возможно разобрать файл по пути "' + filename + '".')
            return False
        self.__xml_filename = filename

        # Корень древа - register?
        if tree.getroot().tag != 'register':
            self.__errors.append('ERROR: Не обнаружен тег <register> в XML файле.')
            return False
        self.__root = tree.getroot()

        # Заполняем модель данными
        self.__fill_organization()
        self.__fill_employees()

        # Очищаем лишние пробелы
        for element in self.__root.iter("*"):
            if element.text is not None and not element.text.strip():
                element.text = None

        # Переносим содержимое тега <job> в <employee> для удобного парсинга
        self.__soft_remove_job_tags()
        return True

    def save_to_file(self, filename, organization, employees):
        # TODO: Доделать
        if filename is None:
            print('ERROR: Не указано место сохранения файла.')
            return False
        root = etree.Element('register')

        # Дата создания документа
        date = etree.SubElement(root, 'date')
        now = datetime.datetime.now()
        date.text = now.strftime("%d.%m.%Y")

        # Заполняем тег <organization>
        organization_node = etree.SubElement(root, 'organization')
        for field in Organization.ALL_FIELDS:
            node = etree.SubElement(organization_node, field)
            node.text = organization.get(field, '')

        # Заполняем данные сотрудников
        for employee in employees.values():
            employee_node = etree.SubElement(root, 'employee')
            # Заполняем корневой тег <employee> сотрудника
            for field in Employee.PERSON_FIELDS:
                node = etree.SubElement(employee_node, field)
                node.text = employee[field]
            # Заполняем тег <job> сотрудника
            job_node = etree.SubElement(employee_node, 'job')
            for field in Employee.JOB_FIELDS:
                if field not in ('hazard_types', 'hazard_factors'):
                    node = etree.SubElement(job_node, field)
                    node.text = employee[field]
                else:
                    hazard_node = etree.SubElement(job_node, field)
                    for hazard in employee[field]:
                        code = etree.SubElement(hazard_node, 'code')
                        code.text = hazard

        save_tree = etree.ElementTree(root)
        save_tree.write(filename, pretty_print=True, encoding="utf-8", xml_declaration=True)
        return True

    def __fill_organization(self):
        """Заполняет информацией поля организации"""
        organization = self.__root.find('organization')
        # Если нет тега <organization>, то заполняем поля пустыми значениями.
        if organization is None:
            self.__errors.append('WARNING: В XML файле отсутствует тег <organization>.')
            for field in self.__organization.keys():
                self.__organization[field] = ''
            return
        # Заполняем найденные поля значениями, а отсутствующие пустыми строками
        for field in Organization.ALL_FIELDS:
            try:
                self.__organization[field] = organization.find(field).text
            except AttributeError:
                self.__organization[field] = ''
                self.__errors.append('WARNING: Не найден тег <' + field + '> в разделе <organization>.')

    def __fill_employees(self):
        """Заполняет информацией поля организации"""
        # TODO: Пеработать метод с учетом мягкого удаления job
        employees_count = len(self.__root.findall('employee'))
        # Если не найдены сотрудники в XML файле
        if employees_count == 0:
            self.__errors.append('WARNING: В XML файле не обнаружен ни один сотрудник.')
            return
        # Перебираем найденных сотрудников
        for i, xml_employee in enumerate(self.__root.iter("employee")):

            # Создаем нового острудника и заполняем его поля
            new_employee = Employee()

            for field in Employee.PERSON_FIELDS:
                if xml_employee.find(field) is None or xml_employee.find(field).text is None:
                    self.__errors.append('WARNING: У сотрудника {} (id:{}) пропущен тег <{}>'
                                         .format(new_employee['full_name'], str(i), field))
                else:
                    new_employee[field] = xml_employee.find(field).text

            # Заполняем поля из тега <job>
            job = xml_employee.find('job')

            # Если не отсутствует тег <job> то переходим к следующему сотруднику
            if job is None:
                self.__errors.append('WARNING: У сотрудника {} (id:{}) пропущен тег <job>'
                                     .format(new_employee['full_name'], str(i)))
                continue

            # Перебираем поля связанные с работой
            for field in Employee.JOB_FIELDS:
                # Если поле не обнаружено
                if job.find(field) is None:
                    self.__errors.append('WARNING: У сотрудника {} (id:{}) не обнаружен тег <{}>'
                                         .format(new_employee['full_name'], str(i), field))

                # Если это не список, то просто записываем значение поля
                elif field not in Employee.LIST_FIELDS:
                    new_employee[field] = job.find(field).text

                # Если это список вредностей то перебираем его
                else:
                    hazards_count = len(job.findall(field + '/code'))
                    # Если в списке нет вредносте, то пропускаем его
                    if hazards_count == 0:
                        continue
                    for hazard in xml_employee.iterfind('job/' + field + '/code'):
                        # Проверяем, что в теге вредности есть текст
                        if hazard.text is None:
                            self.__errors.append('WARNING: Пустой тег <code> у сотрудника {} (id:{})'
                                                 .format(new_employee['full_name'], str(i)))
                            continue
                        # Если все в порядке, записываем вредность
                        new_employee[field].append(hazard.text)

            self.__employees.add(new_employee)

    def __soft_remove_job_tags(self):
        """Удаляет тег <job>, перенося его детей в его родителя - <employee>"""
        # Перебираем найденных сотрудников
        for xml_employee in self.__root.iter("employee"):
            job = xml_employee.find('job')
            # Если не отсутствует тег <job> то переходим к следующему сотруднику
            if job is None:
                continue
            for child in job:
                xml_employee.append(child)
            xml_employee.remove(job)

    def log_tree(self):
        tree = etree.ElementTree(self.__root)
        tree.write('tests/xml_parser_data.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")
