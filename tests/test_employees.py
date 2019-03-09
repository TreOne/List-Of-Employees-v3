import unittest
from utility.employees import Employees


class ClassTestEmployees(unittest.TestCase):

    def setUp(self):
        self.employees = Employees()

    def test_creation(self):
        self.assertEqual(self.employees.num(), 0)

    def test_adding_employees(self):
        self.employees.add_empty_employee()
        self.assertEqual(self.employees.num(), 1)

    def test_getting_employees(self):
        self.employees.add_empty_employee()
        employee = self.employees.get_employee(0)
        with self.assertRaises(KeyError):
            employee.value('bla-bla-bla')
        self.assertEqual(employee.value('patronymic'), '')
        self.assertIsInstance(employee.value('hazard_factors'), list)

    def test_edit_employee(self):
        self.employees.add_empty_employee()
        hazards = ['1', '2', '3']
        employee = self.employees.get_employee(0)
        employee.set_value('family_name', 'Иванов')
        self.assertEqual(employee.value('family_name'), 'Иванов')
        employee.set_value('hazard_types', hazards)
        hazards.append('4')
        self.assertEqual(len(employee.value('hazard_types')), 3)

    def remove_employee(self):
        self.employees.add_empty_employee()
        self.employees.add_empty_employee()
        self.assertEqual(self.employees.num(), 2)
        self.employees.rem_employee(1)
        self.assertEqual(self.employees.num(), 1)


if __name__ == '__main__':
    unittest.main()
