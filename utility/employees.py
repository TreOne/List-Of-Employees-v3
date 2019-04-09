from __future__ import annotations


class Employee:
    """
    Класс Employee представляет собой модель острудника.
    Класс поддерживает item assignment, что значит, что он ведет себя по принципу словаря:
        employee['family_name'] = 'Иванов'
    Класс поддерживает словарные методы keys(), values(), items().
    Класс поддерживает особое поле full_name которое работает автоматически (с него возможно только чтение).
    Получить список полей представляющих собой списки: Employee.LIST_FIELDS (обработка списков обычно отличается).
    При записей значений, списки клонируются, чтобы избежать проблем с изменением значений по ссылке.
    """

    PERSON_FIELDS = ('family_name', 'first_name', 'patronymic', 'sex', 'birth_date', 'address_free_form')
    JOB_FIELDS = ('experience', 'specialty', 'hazard_types', 'hazard_factors')
    ALL_FIELDS = PERSON_FIELDS + JOB_FIELDS
    LIST_FIELDS = 'hazard_types', 'hazard_factors'

    def __init__(self, original=None):
        for key in Employee.ALL_FIELDS:
            if key in Employee.LIST_FIELDS:
                value = original[key].copy() if original is not None else list()
            else:
                value = original[key] if original is not None else ''
            self.__dict__[key] = value

    def __setitem__(self, key, value):
        if key not in Employee.ALL_FIELDS:
            raise KeyError(key)

        # Списочные элементы копируем по значению, а не по ссылке
        if key in Employee.LIST_FIELDS:
            self.__dict__[key] = value.copy()
        else:
            self.__dict__[key] = value

    def __getitem__(self, key):
        # Для удобства, автоматически создаем поле full_name
        if key == 'full_name':
            full_name = ' '.join((self.__dict__['family_name'],
                                  self.__dict__['first_name'],
                                  self.__dict__['patronymic']))
            return full_name.strip()
        return self.__dict__[key]

    def __repr__(self):
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
""".format(self['full_name'], self['sex'],
           self['birth_date'], self['address_free_form'],
           self['experience'], self['specialty'],
           self['hazard_types'], self['hazard_factors'])
        return string

    def __str__(self):
        return "Employee({})".format(self['full_name'])

    def copy(self):
        """Возвращает глубокую копию объекта сотрудника"""
        return Employee(self)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()


class Employees:
    """
    Класс Employees представляет собой словарь сотрудников с ключами в виде книуальных ID.
    Класс позволяет удобно управлять добавлением, изменением, поиском и удалением сотрудников.
    Класс поддерживает item assignment, что значит, что он ведет себя по принципу словаря:
        print( employees_list[1] )
    В классе содержатся копии констант из агрегируемого класса Employee, для удобства использования.
    Класс поддерживает словарные методы keys(), values(), items().
    Для добавления новых сотрудников add(self, employee=None) -> [int, Employee].
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

    def __str__(self):
        result = ''
        for emp_id, employee in self:
            result += '[{}] {}\n'.format(emp_id, employee)
        return result

    def __setitem__(self, emp_id, employee):
        self.__list_of_employees.__setitem__(emp_id, employee)

    def __getitem__(self, emp_id):
        return self.__list_of_employees[emp_id]

    def get_employees(self) -> dict[Employee]:
        """Получить список всех сотрудников"""
        return self.__list_of_employees

    def pop(self, emp_id: int) -> Employee:
        """Удалить сотрудника по id"""
        return self.__list_of_employees.pop(emp_id)

    def add(self, employee=None) -> [int, Employee]:
        """Добавить пустого сотрудника или занести переданного сотрудника, как нового."""
        new_id = self._get_new_id()
        self.__list_of_employees[new_id] = employee if employee is not None else Employee()
        return new_id, self.__list_of_employees[new_id]

    def copy(self):
        """Возвращает глубокую копию списка сотрудников"""
        new_list = Employees()
        for emp_id, employee in self.items():
            new_list[emp_id] = employee.copy()
        return new_list

    def keys(self):
        return self.__list_of_employees.keys()

    def values(self):
        return self.__list_of_employees.values()

    def items(self):
        return self.__list_of_employees.items()

    def _get_new_id(self) -> int:
        """Получить уникальный ID для сотрудника"""
        self.__max_id += 1
        return self.__max_id
