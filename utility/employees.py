class Employees:
    def __init__(self):
        self.list_of_employees = dict()
        self.max_id = -1

    def __len__(self):
        return len(self.list_of_employees)

    def _get_new_id(self):
        self.max_id += 1
        return self.max_id

    def get_employee(self, emp_id: int):
        """Получить сотрудника по id"""
        return self.list_of_employees.get(emp_id, None)

    def get_employees(self):
        """Получить список всех сотрудников"""
        return self.list_of_employees

    def rem_employee(self, emp_id: int):
        """Удалить сотрудника по id"""
        self.list_of_employees.pop(emp_id, None)

    def add_empty_employee(self):
        """Добавить пустого сотрудника"""
        new_id = self._get_new_id()
        new_employee = Employee()
        self.list_of_employees[new_id] = new_employee
        return new_employee

    def add_employee(self, employee: dict):
        """Добавить сотрудника"""
        new_employee = self.add_empty_employee()
        for key, value in employee:
            setattr(new_employee, key, value)


class Employee:
    PERSON_FIELDS = ('family_name', 'first_name', 'patronymic', 'sex', 'birth_date', 'address_free_form')
    JOB_FIELDS = ('experience', 'specialty', 'hazard_types', 'hazard_factors')
    ALL_FIELDS = PERSON_FIELDS + JOB_FIELDS
    LIST_FIELDS = 'hazard_types', 'hazard_factors'

    def __init__(self, original=None):
        self.__dict__['fields'] = dict()
        for key in Employee.ALL_FIELDS:
            if key in Employee.LIST_FIELDS:
                value = getattr(original, key).copy() if original is not None else list()
            else:
                value = getattr(original, key) if original is not None else ''
            self.__dict__['fields'][key] = value

    def __getattr__(self, key):
        if key == 'full_name':
            full_name = ' '.join((self.family_name, self.first_name, self.patronymic))
            return full_name.strip()

        if key in Employee.ALL_FIELDS:
            return self.fields[key]
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key in Employee.ALL_FIELDS:
            if key in Employee.LIST_FIELDS:
                self.__dict__[key] = value.copy()
            else:
                self.__dict__[key] = value
        else:
            raise AttributeError(key)

    def __repr__(self):
        return "Employee({})".format(self.full_name)

    def __str__(self):
        string = """\
############################## СОТРУДНИК ##############################
    ФИО: '{}'
    Пол: '{}'
    Дата рождения: '{}'
    Адрес проживания: '{}'
    
    Стаж: '{}'
    Должность: '{}'
    Тивы вредностей: {}
    Факторы вредностей: {}
#######################################################################
""".format(self.full_name, self.sex, self.birth_date, self.address_free_form,
           self.experience, self.specialty, self.hazard_types, self.hazard_factors)
        return string

    def __iter__(self):
        self.iter_index = 0
        return self

    def __next__(self):
        if self.iter_index >= len(Employee.ALL_FIELDS):
            raise StopIteration
        key = Employee.ALL_FIELDS[self.iter_index]
        value = getattr(self, key)
        self.iter_index += 1
        return key, value

    def clone(self):
        return Employee(self)
