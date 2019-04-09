class Organization:
    """
    Класс Organization представляет собой модель получения, изменения и хранения данных об организации.
    Получить список полей класса: Organization.ALL_FIELDS
    Так же класс является итерабельным, что обозначает, что вы можете перебирать все поля класса вот так:
        org = Organization()
        for field_name, field_value in org:
            setattr(org, field_name, field_value + ' изменение')
    """

    ALL_FIELDS = ('org_name', 'inn', 'ogrn', 'org_address',
                  'head_full_name', 'representative_full_name', 'representative_position')

    def __init__(self):
        self.__dict__['fields'] = dict()
        for key in Organization.ALL_FIELDS:
            self.__dict__['fields'][key] = ''

    def __getattr__(self, key):
        if key in Organization.ALL_FIELDS:
            return self.fields[key]
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __repr__(self):
        return "Organization({})".format(self.org_name)

    def __str__(self):
        string = """\
############################## ОРГАНИЗАЦИЯ ##############################
    Название: '{}'
    ИНН: '{}'
    ОГРН: '{}'
    Адрес: '{}'

    Директор: '{}'
    Представитель: '{}'
    Должность представителя: '{}'
#########################################################################
""".format(self.org_name, self.inn, self.ogrn, self.org_address,
           self.head_full_name, self.representative_full_name, self.representative_position)
        return string

    def __iter__(self):
        self.iter_index = 0
        return self

    def __next__(self):
        if self.iter_index >= len(Organization.ALL_FIELDS):
            raise StopIteration
        key = Organization.ALL_FIELDS[self.iter_index]
        value = getattr(self, key)
        self.iter_index += 1
        return key, value
