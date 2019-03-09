import utility.enumerations as e


class Employees:
    def __init__(self):
        self.list_of_employees = dict()
        self.max_id = -1

    def num(self) -> int:
        return len(self.list_of_employees)

    def get_new_id(self):
        self.max_id += 1
        return self.max_id

    def get_employee(self, emp_id: int):
        return self.list_of_employees[emp_id]

    def rem_employee(self, emp_id: int):
        return self.list_of_employees.pop(emp_id)

    def get_employees(self):
        return self.list_of_employees

    def add_empty_employee(self) -> int:
        new_id = self.get_new_id()
        self.list_of_employees[new_id] = Employee()
        return new_id

    def add_employee(self, employee: dict):
        new_id = self.add_empty_employee()
        new_employee = self.get_employee(new_id)
        for k, v in employee:
            new_employee.set_value(k, v)


class Employee:
    def __init__(self):
        self.fields = dict()
        for field_name in e.EMPLOYEE_FIELDS + e.JOB_FIELDS:
            if field_name in ('hazard_types', 'hazard_factors'):
                self.fields[field_name] = list()
            else:
                self.fields[field_name] = ''

    def set_value(self, field_name, value):
        if field_name in self.fields:
            if field_name in ('hazard_types', 'hazard_factors'):
                self.fields[field_name] = value.copy()
            else:
                self.fields[field_name] = value
        else:
            raise KeyError

    def value(self, field_name):
        if field_name == 'full_name':
            return ' '.join((self.fields['family_name'], self.fields['first_name'], self.fields['patronymic']))
        return self.fields[field_name]
