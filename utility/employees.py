import utility.enumerations as e


class Employees:
    def __init__(self):
        self.list_of_employees = dict()
        self.max_id = -1

    def num(self):
        return len(self.list_of_employees)

    def get_new_id(self):
        self.max_id += 1
        return self.max_id

    def add_empty_employee(self):
        self.list_of_employees[self.get_new_id()] = Employee()

    def get_employees(self):
        return self.list_of_employees

    def get_employee(self, emp_id: int):
        try:
            return self.list_of_employees[emp_id]
        except KeyError:
            return None


class Employee:
    def __init__(self):
        self.fields = dict()
        for field_name in e.EMPLOYEE_FIELDS + e.JOB_FIELDS:
            if field_name in ('hazard_types', 'hazard_factors'):
                self.fields[field_name] = list()
            else:
                self.fields[field_name] = ''
