from datetime import date
from utility.organization import Organization
from utility.employees import Employee, Employees
from utility.hazards_lists_helper import HazardsListsHelper
from utility.xml_parser import XMLParser
from utility.resource_path import resource_path
import random
# pip install mimesis
from mimesis import Generic
from mimesis.enums import Gender
from mimesis.builtins import RussiaSpecProvider

if __name__ == '__main__':
    EMPLOYEE_NUMS = 100

    organization = Organization()
    list_of_employees = Employees()

    generic = Generic('ru')
    ru = RussiaSpecProvider()
    generic.add_provider(RussiaSpecProvider)

    hazards = HazardsListsHelper()
    hazard_types = list(hazards.get_hazard_types().keys())
    hazard_factors = list(hazards.get_hazard_factors().keys())

    for _ in range(0, EMPLOYEE_NUMS):
        # Создаем нового сотрудника и выбираем ему случайный пол
        employee = Employee()
        gender = random.choice([Gender.FEMALE, Gender.MALE])

        # Заполняем объект сотрудника данными
        employee['family_name'] = generic.person.last_name(gender=gender)
        employee['first_name'] = generic.person.name(gender=gender)
        employee['patronymic'] = ru.patronymic(gender=gender)

        employee['sex'] = "Мужской" if gender == Gender.MALE else "Женский"
        birth_date = generic.datetime.date(start=1950, end=2000)
        employee['birth_date'] = birth_date.strftime("%Y-%m-%d")
        employee['address_free_form'] = "{}, г {}, {} {}, д {}, кв {}".format(generic.address.region(),
                                                                              generic.address.city(),
                                                                              generic.address.street_suffix(),
                                                                              generic.address.street_name(),
                                                                              random.randint(1, 400),
                                                                              random.randint(1, 400))

        age = date.today().year - birth_date.year
        employee['experience'] = str(random.randint(0, age - 18))
        employee['specialty'] = generic.person.occupation()

        hazard_types_copy = hazard_types.copy()
        hazard_factors_copy = hazard_factors.copy()
        employee_hazard_types = list()
        employee_hazard_factors = list()
        for i in range(0, random.randint(0, 5)):
            employee_hazard_types.append(hazard_types_copy.pop(random.randint(0, len(hazard_types_copy)-1)))
        for i in range(0, random.randint(0, 10)):
            employee_hazard_factors.append(hazard_factors_copy.pop(random.randint(0, len(hazard_factors_copy)-1)))

        employee['hazard_types'] = employee_hazard_types
        employee['hazard_factors'] = employee_hazard_factors

        # Добавляем острудника в список
        list_of_employees.add(employee)

    organization['org_name'] = '{} "{}"'.format(generic.business.company_type(abbr=True), generic.business.company())
    organization['inn'] = str(random.randint(1000000000, 9999999999))
    organization['ogrn'] = str(random.randint(1000000000000, 9999999999999))
    organization['org_address'] = "{}, {}, город {}, {} {}, дом {}".format(generic.address.zip_code(),
                                                                           generic.address.region(),
                                                                           generic.address.city(),
                                                                           generic.address.street_suffix(),
                                                                           generic.address.street_name(),
                                                                           random.randint(1, 400))

    gender = random.choice([Gender.FEMALE, Gender.MALE])
    organization['head_full_name'] = "{} {} {}".format(generic.person.last_name(gender=gender),
                                                       generic.person.name(gender=gender),
                                                       ru.patronymic(gender=gender))

    gender = random.choice([Gender.FEMALE, Gender.MALE])
    organization['representative_full_name'] = "{} {} {}".format(generic.person.last_name(gender=gender),
                                                                 generic.person.name(gender=gender),
                                                                 ru.patronymic(gender=gender))
    organization['representative_position'] = generic.person.occupation()

    xml_parser = XMLParser()
    xml_parser.save_to_file(resource_path('../tests/demo_data.xml'), organization, list_of_employees)
