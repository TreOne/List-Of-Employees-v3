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
        for k, v in employee:
            new_employee.set_attr(k, v)


class Employee:
    ORGANIZATION_FIELDS = ('org_name', 'inn', 'ogrn', 'org_address',
                           'head_full_name', 'representative_full_name', 'representative_position')
    PERSON_FIELDS = ('family_name', 'first_name', 'patronymic', 'sex', 'birth_date', 'address_free_form')
    JOB_FIELDS = ('experience', 'specialty', 'hazard_types', 'hazard_factors')
    ALL_FIELDS = PERSON_FIELDS + JOB_FIELDS

    def __init__(self, original=None):
        self.fields = dict()
        for field_name in Employee.ALL_FIELDS:
            if field_name in ('hazard_types', 'hazard_factors'):
                self.fields[field_name] = list() if original is None else original.attr(field_name).copy()
            else:
                self.fields[field_name] = '' if original is None else original.attr(field_name)

    def __getattr__(self, attr_name):
        if attr_name in Employee.ALL_FIELDS:
            if attr_name == 'full_name':
                full_name = ' '.join((self.fields['family_name'], self.fields['first_name'], self.fields['patronymic']))
                return full_name.strip()
            return self.fields[attr_name]
        else:
            raise AttributeError(attr_name)

    # TODO: Решить проблемму с атрибутами класса Employee
    def set_attr(self, field_name, value):
        if field_name in self.fields:
            if field_name in ('hazard_types', 'hazard_factors'):
                self.fields[field_name] = value.copy()
            else:
                self.fields[field_name] = value
        else:
            raise KeyError

    def attr(self, field_name):
        if field_name == 'full_name':
            full_name = ' '.join((self.fields['family_name'], self.fields['first_name'], self.fields['patronymic']))
            return full_name.strip()
        return self.fields[field_name]

    def clone(self):
        return Employee(self)
