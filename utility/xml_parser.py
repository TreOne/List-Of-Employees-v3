from utility.employees import Employee, Employees
from utility.organization import Organization
from utility.resource_path import resource_path
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
        self.__warnings = list()

    def __reset_state(self):
        self.__xml_filename = None
        self.__root = None
        self.__employees = Employees()
        self.__organization = Organization()
        self.__errors = list()
        self.__warnings = list()

    def get_organization(self):
        return self.__organization

    def get_employees(self):
        return self.__employees

    def get_errors(self):
        return self.__errors

    def load_file(self, filename):
        """Разбирает XML файл и заполняет данными список сотрудников и данные об организации"""
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

        # Режем хвосты у тегов и очищаем лишние пробелы (они могут помешать корректной работе парсера)
        self.__clear_xml()
        # Переносим содержимое тега <job> в <employee> для удобного парсинга
        self.__soft_remove_job_tags()

        # Заполняем модель данными
        self.__fill_organization()
        self.__fill_employees()

        return True

    @staticmethod
    def save_to_file(filename, organization, employees):
        """Сохраняет данные в XML файл"""
        root = etree.Element('register')

        # Дата создания документа
        date = etree.SubElement(root, 'date')
        now = datetime.datetime.now()
        date.text = now.strftime("%Y-%m-%d")

        # Заполняем тег <organization>
        organization_node = etree.SubElement(root, 'organization')
        for field in Organization.ALL_FIELDS:
            node = etree.SubElement(organization_node, field)
            node.text = organization[field]

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
                if field not in Employee.LIST_FIELDS:
                    node = etree.SubElement(job_node, field)
                    node.text = employee[field]
                else:
                    if len(employee[field]) > 0:
                        hazard_node = etree.SubElement(job_node, field)
                        for hazard in employee[field]:
                            code = etree.SubElement(hazard_node, 'code')
                            code.text = hazard

        save_tree = etree.ElementTree(root)
        save_tree.write(filename, pretty_print=True, encoding="utf-8", xml_declaration=True)
        return True

    def __fill_organization(self):
        """Заполняет информацией поля организации."""
        organization = self.__root.find('organization')
        # Если нет тега <organization>, то заполняем поля пустыми значениями.
        if organization is None:
            self.__warnings.append('WARNING: В XML файле отсутствует тег <organization>.')
            for field in self.__organization.keys():
                self.__organization[field] = ''
            return
        # Заполняем найденные поля значениями, а отсутствующие пустыми строками
        for field in Organization.ALL_FIELDS:
            try:
                self.__organization[field] = organization.find(field).text
            except AttributeError:
                self.__organization[field] = ''
                self.__warnings.append('WARNING: Не найден тег <' + field + '> в разделе <organization>.')

    def __fill_employees(self):
        """Заполняет информацией поля сотрудника."""
        employees_count = len(self.__root.findall('employee'))
        # Если не найдены сотрудники в XML файле
        if employees_count == 0:
            self.__warnings.append('WARNING: В XML файле не обнаружен ни один сотрудник.')
            return
        # Перебираем найденных сотрудников
        for i, xml_employee in enumerate(self.__root.iter("employee")):

            # Создаем нового острудника и заполняем его поля
            new_employee = Employee()

            for field in Employee.ALL_FIELDS:
                # Если поле не обнаружено
                if xml_employee.find(field) is None:
                    self.__warnings.append('WARNING: У сотрудника {} (id:{}) не обнаружен тег <{}>'
                                           .format(new_employee['full_name'], str(i), field))

                # Если это не список, то просто записываем значение поля
                elif field not in Employee.LIST_FIELDS:
                    new_employee[field] = xml_employee.find(field).text

                # Если это список вредностей то перебираем его
                else:
                    hazards_count = len(xml_employee.findall(field + '/code'))
                    # Если в списке нет вредносте, то пропускаем его
                    if hazards_count == 0:
                        continue
                    for hazard in xml_employee.iterfind(field + '/code'):
                        # Проверяем, что в теге вредности есть текст
                        if hazard.text is None:
                            self.__warnings.append('WARNING: Пустой тег <code> у сотрудника {} (id:{})'
                                                   .format(new_employee['full_name'], str(i)))
                            continue
                        # Если все в порядке, записываем вредность
                        new_employee[field].append(hazard.text)

            self.__employees.add(new_employee)

    def __soft_remove_job_tags(self):
        """Удаляет тег <job>, перенося его детей в его родителя - <employee>."""
        # Перебираем найденных сотрудников
        for xml_employee in self.__root.iter("employee"):
            job = xml_employee.find('job')
            # Если отсутствует тег <job> то переходим к следующему сотруднику
            if job is None:
                continue
            for child in job:
                xml_employee.append(child)
            xml_employee.remove(job)

    def __clear_xml(self):
        """Удаляет хвосты и лишние пробелы в тексте у всех элементов в xml файле,
         так как наша схема не предполагает их наличие."""
        for element in self.__root.iter("*"):
            element.tail = None
            if element.text is not None and not element.text.strip():
                element.text = None

    def validate(self):
        self.__errors = list()
        if self.__xml_filename is None:
            self.__errors.append("ERROR: XML файл еще не загружен.")
            return False
        try:
            schema_filename = resource_path('resources/xml_schema.xsd')
            schema = etree.XMLSchema(file=schema_filename)
            xml_file = etree.ElementTree(file=self.__xml_filename)
            schema.assert_(xml_file)
            return True

        except etree.XMLSyntaxError as err:
            self.__errors.append("ERROR: Ошибка разбора XML файла:{0}".format(err))
            return False

        except AssertionError as err:
            self.__errors.append("ERROR: Неправильный формат файла валидации XML: {0}".format(err))
            return False

        except ValueError as err:
            self.__errors.append("ERROR: Не правильный формат XML файла: {0}".format(err))
            return False

        except OSError:
            self.__errors.append("ERROR: Ошибка чтения файла '{0}'".format(self.__xml_filename))
            return False

    def _log_tree(self):
        """Создает "отпечаток" текущего состояния данных. Использовать для отладки."""
        tree = etree.ElementTree(self.__root)
        tree.write('tests/xml_parser_data.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")
