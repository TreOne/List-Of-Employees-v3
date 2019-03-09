import unittest
from utility.employees import Employees


class ClassTestEmployees(unittest.TestCase):

    def setUp(self):
        self.employees = Employees()

    def test_creation(self):
        self.assertEqual(self.employees.num(), 0)

    def test_adding_employees(self):
        self.assertEqual(self.employees.num(), 0)
        self.employees.add_empty_employee()
        self.assertEqual(self.employees.num(), 1)

    def test_getting_employees(self):
        self.assertEqual(self.employees.num(), 0)
        self.employees.add_empty_employee()
        self.assertIsNone(self.employees.get_employee(1))
        employee = self.employees.get_employee(0)
        self.assertEqual(employee.fields['patronymic'], '')
        self.assertIsInstance(employee.fields['hazard_factors'], list)


if __name__ == '__main__':
    unittest.main()
