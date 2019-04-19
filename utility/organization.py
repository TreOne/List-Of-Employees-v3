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

    def __init__(self, original=None):
        for key in Organization.ALL_FIELDS:
            value = original[key] if original is not None else ''
            self.__dict__[key] = value

    def __setitem__(self, key, value):
        if key not in Organization.ALL_FIELDS:
            raise KeyError(key)
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key] if self.__dict__[key] is not None else ''

    def __repr__(self):
        return "Organization({})".format(self['org_name'])

    def __str__(self):
        return self['org_name']

    def show(self):
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
""".format(*self.values())
        print(string)

    def copy(self):
        """Возвращает копию объекта организации"""
        return Organization(self)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()
