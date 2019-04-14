import json
import requests
from utility.resource_path import resource_path

URL = "http://tre.one/test/"


class HazardsListsHelper:
    """
    Класс HazardListsHelper служит для работы со списками вредностей.
    """
    def __init__(self):
        ins_lists_json_web = None
        try:
            r = requests.post(URL, timeout=5)
            ins_lists_json_web = r.json()
        except Exception as e:
            print(e)

        # Если данные с web получены и хэш обновился, то перезаписываем локальную базу
        if ins_lists_json_web is not None and 'hash' in ins_lists_json_web:
            try:  # Если файл не открыть (удален) то скачиваем новый файл
                with open(resource_path('../resources/hazard_lists.json'), encoding='utf-8') as f:
                    ins_lists_json_local = json.load(f)
                if ins_lists_json_local['hash'] != ins_lists_json_web['hash']:
                    with open(resource_path('../resources/hazard_lists.json'), 'w', encoding="utf-8") as outfile:
                        json.dump(ins_lists_json_web, outfile, ensure_ascii=False)
            except (OSError, IOError):
                with open(resource_path('../resources/hazard_lists.json'), 'w', encoding="utf-8") as outfile:
                    json.dump(ins_lists_json_web, outfile, ensure_ascii=False)

        with open(resource_path('../resources/hazard_lists.json'), encoding='utf-8') as f:
            ins_lists_json = json.load(f)

        self.__hazard_factors = ins_lists_json['hazards_factors']
        self.__hazard_types = ins_lists_json['hazards_types']
        self.__hazard_factors_tree = HazardListTree(self.__hazard_factors)
        self.__hazard_types_tree = HazardListTree(self.__hazard_types)

        # Примеры использования self.__hazard_factors
        """
        self.__hazard_factors.tree.print_the_tree()

        childs = self.__hazard_factors_tree.root.search_child_by_code("1").childs
        for child in childs:
            print(child.code, child.name)

        node = self.__hazard_factors_tree.root.search_child_by_code(0).search_child_by_code(0).search_child_by_code(0)
        print(node.name)
        """

    def get_hazard_factors(self):
        return self.__hazard_factors

    def get_hazard_types(self):
        return self.__hazard_types

    def get_hazard_factors_tree(self):
        return self.__hazard_factors_tree

    def get_hazard_types_tree(self):
        return self.__hazard_types_tree


class HazardListItem:
    """
    Класс HazardListItem - вспомогательный класс для построения древа факторов и типов вредности.
    """

    def __init__(self, code, name=None, parent=None):
        self.parent = parent
        self.childs = list()
        self.code = int(code)
        self.name = name

    def __lt__(self, other):
        return self.code < other.code

    def set_parent(self, parent):
        self.parent = parent

    def set_name(self, name):
        self.name = name.strip()

    def get_name(self, name):
        if self.name is None:
            return ''
        return self.name

    def add_child(self, child):
        self.childs.append(child)
        child.set_parent(self)
        self.childs.sort()

    def get_full_code(self):
        full_code = ''
        node = self
        while node.parent is not None:
            full_code = str(node.code) + '.' + full_code
            node = node.parent
        if len(self.childs) == 0:  # Убрать точку в адресе листового нода
            full_code = full_code[0:-1]
        return full_code

    def search_child_by_code(self, code):
        if len(self.childs) == 0:
            return None
        for child in self.childs:
            if child.code == int(code):
                return child
        return None

    def print_node(self):
        if self.name is not None:
            name = self.name
        print(' '*len(self.get_full_code()) + self.get_full_code() + " -> " + name)
        if self.childs is not None:
            for child in self.childs:
                child.print_node()


class HazardListTree:
    """
    Класс HazardListTree - класс древа факторов и типов вредности.
    """
    def __init__(self, json_obj):
        self.root = HazardListItem(0)
        for k, name in json_obj.items():
            item_address = k.split('.')  # ['1', '3', '4', '4', '2', ''] для 1.3.4.4.2.
            start_from = self.root
            for step in item_address:
                if step == '':  # Если дошли до конца адреса то записываем название нода.
                    start_from.set_name(name)
                    break
                node = start_from.search_child_by_code(step)
                if node is None:
                    node = HazardListItem(code=step, parent=start_from)
                    start_from.add_child(node)
                start_from = node

    def print_the_tree(self):
        self.root.print_node()
