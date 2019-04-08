from __future__ import annotations


class Employee:
    """
    Класс Employee представляет собой модель острудника.
    Получить список полей класса: Employee.ALL_FIELDS
    Получить список полей представляющих собой списки: Employee.LIST_FIELDS (обработка списков обычно отличается)
    При записей значений, списки клонируются, чтобы избежать проблем с изменением значений по ссылке.
    Так же класс является итерабельным, что обозначает, что вы можете перебирать все поля класса вот так:
    emp = Employee()
    for field_name, field_value in emp:
        setattr(emp, field_name, field_value + ' изменение')
    """

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
        if key in Employee.LIST_FIELDS:
            self.__dict__[key] = value.copy()
        else:
            self.__dict__[key] = value

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
    Типы вредностей: {}
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
        """Возвращает глубокую копию объекта сотрудника"""
        return Employee(self)


class Employees:
    """
    Класс Employees представляет собой словарь сотрудников с ключами в виде книуальных ID.
    Класс позволяет удобно управлять добавлением, изменением, поиском и удалением сотрудников.
    В классе содержатся копии констант из агрегируемого класса Employee, длы удобства использования.
    """

    PERSON_FIELDS = Employee.PERSON_FIELDS
    JOB_FIELDS = Employee.JOB_FIELDS
    ALL_FIELDS = Employee.ALL_FIELDS
    LIST_FIELDS = Employee.LIST_FIELDS

    def __init__(self):
        self.__list_of_employees = dict()
        self.__max_id = -1

    def __len__(self):
        return len(self.__list_of_employees)

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

    def get_employee(self, emp_id: int) -> Employee:
        """Получить сотрудника по id"""
        return self.__list_of_employees.get(emp_id, None)

    def get_employees(self) -> dict[Employee]:
        """Получить список всех сотрудников"""
        return self.__list_of_employees

    def rem_employee(self, emp_id: int) -> None:
        """Удалить сотрудника по id"""
        self.__list_of_employees.pop(emp_id, None)

    def add_empty_employee(self) -> Employee:
        """Добавить пустого сотрудника"""
        new_id = self._get_new_id()
        new_employee = Employee()
        self.__list_of_employees[new_id] = new_employee
        return new_employee

    def add_employee(self, employee: Employee) -> [int, Employee]:
        """Добавить сотрудника"""
        new_id = self._get_new_id()
        self.__list_of_employees[new_id] = employee.clone()
        return new_id, self.__list_of_employees[new_id]

    def _get_new_id(self) -> int:
        """Получить уникальный ID для сотрудника"""
        self.__max_id += 1
        return self.__max_id

