import unittest
from utility.employees import Employees


class ClassTestEmployees(unittest.TestCase):

    def setUp(self):
        self.employees = Employees()

    def test_creation(self):
        self.assertEqual(len(self.employees), 0)

    def test_adding_employees(self):
        self.employees.add_empty_employee()
        self.assertEqual(len(self.employees), 1)

    def test_getting_employees(self):
        self.employees.add_empty_employee()
        employee = self.employees.get_employee(0)
        with self.assertRaises(AttributeError):
            employee.bla_bla_bla = 0
        self.assertEqual(employee.patronymic, '')
        self.assertIsInstance(employee.hazard_factors, list)

    def test_edit_employee(self):
        self.employees.add_empty_employee()
        hazards = ['1', '2', '3']
        employee = self.employees.get_employee(0)
        employee.family_name = 'Иванов'
        employee.first_name = 'Иван'
        self.assertEqual(employee.full_name, 'Иванов Иван')
        employee.patronymic = 'Иванович'
        self.assertEqual(employee.family_name, 'Иванов')
        self.assertEqual(employee.full_name, 'Иванов Иван Иванович')
        employee.hazard_types = hazards
        hazards.append('4')
        new_patronymic = 'Сидорович'
        employee.patronymic = new_patronymic
        new_patronymic = 'Андреевич'
        self.assertEqual(employee.full_name, 'Иванов Иван Сидорович')
        self.assertEqual(len(employee.hazard_types), 3)

    def test_clone_employee(self):
        employee = self.employees.add_empty_employee()
        employee.family_name = 'Иванов'
        employee.first_name = 'Иван'
        employee.patronymic = 'Иванович'
        employee.hazard_types = ['1', '2', '3']
        employee2 = employee.copy()
        employee2.family_name = 'Петров'
        employee2.hazard_types = ['4', '5', '6', '7']
        self.assertEqual(employee.family_name, 'Иванов')
        self.assertEqual(len(employee.hazard_types), 3)
        self.assertEqual(employee2.family_name, 'Петров')
        self.assertEqual(len(employee2.hazard_types), 4)

    def remove_employee(self):
        self.employees.add_empty_employee()
        self.employees.add_empty_employee()
        self.assertEqual(len(self.employees), 2)
        self.employees.rem_employee(1)
        self.assertEqual(len(self.employees), 1)


if __name__ == '__main__':
    unittest.main()
