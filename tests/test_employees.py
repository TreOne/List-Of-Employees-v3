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
        with self.assertRaises(KeyError):
            employee.attr('bla-bla-bla')
        self.assertEqual(employee.attr('patronymic'), '')
        self.assertIsInstance(employee.attr('hazard_factors'), list)

    def test_edit_employee(self):
        self.employees.add_empty_employee()
        hazards = ['1', '2', '3']
        employee = self.employees.get_employee(0)
        employee.set_attr('family_name', 'Иванов')
        employee.set_attr('first_name', 'Иван')
        self.assertEqual(employee.attr('full_name'), 'Иванов Иван')
        employee.set_attr('patronymic', 'Иванович')
        self.assertEqual(employee.attr('family_name'), 'Иванов')
        self.assertEqual(employee.attr('full_name'), 'Иванов Иван Иванович')
        employee.set_attr('hazard_types', hazards)
        hazards.append('4')
        self.assertEqual(len(employee.attr('hazard_types')), 3)

    def test_clone_employee(self):
        employee = self.employees.add_empty_employee()
        employee.set_attr('family_name', 'Иванов')
        employee.set_attr('first_name', 'Иван')
        employee.set_attr('patronymic', 'Иванович')
        employee.set_attr('hazard_types', ['1', '2', '3'])
        employee2 = employee.clone()
        employee2.set_attr('family_name', 'Петров')
        employee2.set_attr('hazard_types', ['4', '5', '6', '7'])
        self.assertEqual(employee.attr('family_name'), 'Иванов')
        self.assertEqual(len(employee.attr('hazard_types')), 3)
        self.assertEqual(employee2.attr('family_name'), 'Петров')
        self.assertEqual(len(employee2.attr('hazard_types')), 4)

    def remove_employee(self):
        self.employees.add_empty_employee()
        self.employees.add_empty_employee()
        self.assertEqual(len(self.employees), 2)
        self.employees.rem_employee(1)
        self.assertEqual(len(self.employees), 1)


if __name__ == '__main__':
    unittest.main()
