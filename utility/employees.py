from __future__ import annotations


class Validate:
    VALID = 0
    WARNING = 1
    INVALID = 2

    def __init__(self, result, text):
        self.result = result
        self.text = text


class Employee:
    """
    Класс Employee представляет собой модель острудника.
    Класс поддерживает item assignment, что значит, что он ведет себя по принципу словаря:
        employee['family_name'] = 'Иванов'
    Класс поддерживает словарные методы keys(), values(), genders().
    Класс поддерживает особое поле full_name которое работает автоматически (с него возможно только чтение).
    Получить список полей представляющих собой списки: Employee.LIST_FIELDS (обработка списков обычно отличается).
    При записей значений, списки клонируются, чтобы избежать проблем с изменением значений по ссылке.
    """

    PERSON_FIELDS = ('family_name', 'first_name', 'patronymic', 'sex', 'birth_date', 'address_free_form')
    JOB_FIELDS = ('experience', 'specialty', 'hazard_types', 'hazard_factors')
    ALL_FIELDS = PERSON_FIELDS + JOB_FIELDS
    LIST_FIELDS = 'hazard_types', 'hazard_factors'

    @staticmethod
    def translate(eng_field):
        """Позволяет ресифицировать название поля."""
        all_fields_rus = {'family_name': 'Фамилия',
                          'first_name': 'Имя',
                          'patronymic': 'Отчество',
                          'sex': 'Пол',
                          'birth_date': 'Дата рождения',
                          'address_free_form': 'Адрес проживания',
                          'experience': 'Стаж',
                          'specialty': 'Должность',
                          'hazard_types': 'Типы вредностей',
                          'hazard_factors': 'Факторы вредностей'}

        return all_fields_rus[eng_field]

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
            full_name = ' '.join((self['family_name'],
                                  self['first_name'],
                                  self['patronymic']))
            return full_name.strip()
        return self.__dict__[key] if self.__dict__[key] is not None else ''

    def __repr__(self):
        return 'Employee({})'.format(self['full_name'])

    def __str__(self):
        return self['full_name']

    def field_validation(self, field_name):
        """Проверка валидности поля сотрудника"""
        # PERSON_FIELDS = ('family_name', 'first_name', 'patronymic', 'sex', 'birth_date', 'address_free_form')
        # JOB_FIELDS = ('experience', 'specialty', 'hazard_types', 'hazard_factors')

        rus_name = Employee.translate(field_name)

        # Проверяем название поля
        if field_name not in Employee.ALL_FIELDS:
            return Validate(Validate.INVALID, "Неправильное название поля сотрудника: '{}'".format(rus_name))

        # Эти поля не должны быть пустыми
        if field_name in ('family_name', 'first_name', 'sex', 'birth_date', 'experience', 'specialty'):
            if self[field_name] == '':
                return Validate(Validate.INVALID, "Поле '{}' должно быть обязательно заполнено!".format(rus_name))

        # У человека может не быть отчества, но это подозрительно
        if field_name == 'patronymic':
            if self[field_name] == '':
                return Validate(Validate.WARNING, "Если у сотрудника есть отчество,"
                                                  " оно должно быть обязательно указано.".format(rus_name))

        return Validate(Validate.VALID, "Неправильное название поля сотрудника: '{}'".format(rus_name))

    def show(self):
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
        print(string)

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
    Класс поддерживает словарные методы keys(), values(), genders().
    Для добавления новых сотрудников add(self, employee=None) -> [int, Employee].
    """

    PERSON_FIELDS = Employee.PERSON_FIELDS
    JOB_FIELDS = Employee.JOB_FIELDS
    ALL_FIELDS = Employee.ALL_FIELDS
    LIST_FIELDS = Employee.LIST_FIELDS

    def __init__(self):
        self.__list_of_employees = dict()
        self.__max_id = -1
        self.__completer_fields = ('family_name', 'first_name', 'patronymic', 'specialty')
        self.__completer_hints = dict()
        # Инициализируем множества значений
        for completer_field in self.__completer_fields:
            self.__completer_hints[completer_field] = set()

    def __len__(self):
        return len(self.__list_of_employees)

    def __str__(self):
        result = ''
        for emp_id, employee in self.items():
            result += '[{}] {}\n'.format(emp_id, employee)
        return result

    def __setitem__(self, emp_id, employee):
        self.__list_of_employees.__setitem__(emp_id, employee)

    def __getitem__(self, emp_id):
        return self.__list_of_employees[emp_id]

    def get_employees(self) -> dict[Employee]:
        """Получить список всех сотрудников"""
        return self.__list_of_employees

    def get_completer(self, completer_field):
        try:
            return self.__completer_hints[completer_field]
        except KeyError:
            return set()

    def get_completer_fields(self):
        return self.__completer_fields

    def refresh_completer(self, field=None):
        if field is None:
            for field in self.__completer_fields:
                self.__completer_hints[field].clear()
                for employee in self.__list_of_employees:
                    self.__completer_hints[field].add(employee[field])
        else:
            self.__completer_hints[field].clear()
            for employee in self.__list_of_employees.values():
                self.__completer_hints[field].add(employee[field])

    def pop(self, emp_id: int) -> Employee:
        """Удалить сотрудника по id"""
        return self.__list_of_employees.pop(emp_id)

    def add(self, employee=None) -> [int, Employee]:
        """Добавляет пустого сотрудника или заносит переданного сотрудника, как нового."""
        new_id = self._get_new_id()
        if employee is None:
            self.__list_of_employees[new_id] = Employee()
        else:
            self.__list_of_employees[new_id] = employee
            for completer_field in self.__completer_fields:
                new_value = self.__list_of_employees[new_id][completer_field]
                self.__completer_hints[completer_field].add(new_value)

        return new_id, self.__list_of_employees[new_id]

    def copy(self):
        """Возвращает глубокую копию списка сотрудников"""
        new_list = Employees()
        for emp_id, employee in self.items():
            new_list[emp_id] = employee.copy()
        return new_list

    def show(self):
        """Выводит подробный список данных о сотруднике"""
        for employee in self.values():
            employee.show()

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
