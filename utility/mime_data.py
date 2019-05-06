from datetime import date
from utility.organization import Organization
from utility.employees import Employee, Employees
from utility.hazards_lists_helper import HazardsListsHelper
import random
from mimesis import Generic
from mimesis.enums import Gender
from mimesis.builtins import RussiaSpecProvider


class MimeData:
    """Класс для создания рыба-данных"""

    def __init__(self, list_len):
        self.organization = Organization()
        self.employees = Employees()

        generic = Generic('ru')
        ru = RussiaSpecProvider()
        generic.add_provider(RussiaSpecProvider)

        hazards = HazardsListsHelper()
        hazard_types = list(hazards.get_hazard_types().keys())
        hazard_factors = list(hazards.get_hazard_factors().keys())

        for _ in range(0, list_len):
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
                employee_hazard_types.append(hazard_types_copy.pop(random.randint(0, len(hazard_types_copy) - 1)))
            for i in range(0, random.randint(0, 10)):
                employee_hazard_factors.append(hazard_factors_copy.pop(random.randint(0, len(hazard_factors_copy) - 1)))

            employee['hazard_types'] = employee_hazard_types
            employee['hazard_factors'] = employee_hazard_factors

            # Добавляем острудника в список
            self.employees.add(employee)

        self.organization['org_name'] = '{} "{}"'.format(generic.business.company_type(abbr=True),
                                                         generic.business.company())
        self.organization['inn'] = str(random.randint(1000000000, 9999999999))
        self.organization['ogrn'] = str(random.randint(1000000000000, 9999999999999))
        self.organization['org_address'] = "{}, {}, город {}, {} {}, дом {}".format(generic.address.zip_code(),
                                                                                    generic.address.region(),
                                                                                    generic.address.city(),
                                                                                    generic.address.street_suffix(),
                                                                                    generic.address.street_name(),
                                                                                    random.randint(1, 400))

        gender = random.choice([Gender.FEMALE, Gender.MALE])
        self.organization['head_full_name'] = "{} {} {}".format(generic.person.last_name(gender=gender),
                                                                generic.person.name(gender=gender),
                                                                ru.patronymic(gender=gender))

        gender = random.choice([Gender.FEMALE, Gender.MALE])
        self.organization['representative_full_name'] = "{} {} {}".format(generic.person.last_name(gender=gender),
                                                                          generic.person.name(gender=gender),
                                                                          ru.patronymic(gender=gender))
        self.organization['representative_position'] = generic.person.occupation()
