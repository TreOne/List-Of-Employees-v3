from PyQt5 import QtCore, QtWidgets
import json
import requests


class AddressAssistant:

    def __init__(self):
        self.__API_KEY = "58c79357ce70340f59484f04cf588738b6633fa6"
        self.__URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"
        self.__headers = {"Authorization": "Token {}".format(self.__API_KEY),
                          "Content-Type": "application/json",
                          "Accept": "application/json"}

    def give_address_hints(self, address, hints_count=5, is_novobl=True):
        data = {"query": address, "count": hints_count}
        if is_novobl:
            data["restrict_value"] = "true"
            data["locations"] = [{"region_fias_id": "e5a84b81-8ea1-49e3-b3c4-0528651be129"}]  # Новгородская область

        response = self.__do_request(data)
        if response:
            address_list = list()
            for suggestion in response["suggestions"]:
                address_list.append(suggestion["value"] + " ")
            return tuple(address_list)

    def give_full_address(self, address):
        data = {"query": address, "count": 1}
        response = self.__do_request(data)
        if response:
            return response["suggestions"][0]["unrestricted_value"]
        else:
            return None

    def give_short_address(self, address):
        data = {"query": address, "count": 1}
        response = self.__do_request(data)
        if response:
            return response["suggestions"][0]["value"]
        else:
            return None

    def __do_request(self, data):
        try:
            r = requests.post(self.__URL, data=json.dumps(data), headers=self.__headers, timeout=5)
            return r.json()
        except Exception as e:
            print(e)
            return False


class AddressesHintsList(QtCore.QAbstractListModel):
    hint_complete = QtCore.pyqtSignal()

    def __init__(self, is_novobl_checkbox, parent=None):
        super(AddressesHintsList, self).__init__(parent)
        self._addresses_hints = tuple()
        self.aa = AddressAssistant()
        self.address_for_search = ''
        self.is_novobl_checkbox = is_novobl_checkbox
        self.hints_delay_timer_id = -1

    def rowCount(self, parent=QtCore.QModelIndex(), **kwargs):
        return len(self._addresses_hints)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        address = self._addresses_hints[index.row()]
        if role == QtCore.Qt.DisplayRole:  # Для отображения в popup окне
            if len(address) < 45:
                return address
            else:
                return '...' + address[-45:]
        elif role == QtCore.Qt.EditRole:  # Для передачи в форму при подтверждении выбора
            return address

    def set_hints_for_address(self, user_input):
        # Таймер использован для экономии количества запросов к API
        if len(user_input) < 3:  # Очищать модель если заполнение поля началось заново.
            self.clear_hints()
        self.address_for_search = user_input
        if self.hints_delay_timer_id != -1:
            self.killTimer(self.hints_delay_timer_id)
        self.hints_delay_timer_id = self.startTimer(1000)

    def timerEvent(self, event):
        self.killTimer(self.hints_delay_timer_id)
        self.hints_delay_timer_id = -1
        self.update_hints()

    def update_hints(self):
        is_novobl = self.is_novobl_checkbox.checkState()
        hints = self.aa.give_address_hints(self.address_for_search, is_novobl=is_novobl)
        self.beginResetModel()
        self._addresses_hints = hints
        self.endResetModel()
        self.hint_complete.emit()

    def clear_hints(self):
        self.beginResetModel()
        self._addresses_hints = tuple()
        self.endResetModel()


class AddressCompleter(QtWidgets.QCompleter):

    def __init__(self, parent=None):
        super(AddressCompleter, self).__init__(parent)
        self.model = None

    def setModel(self, model):
        self.model = model
        super(AddressCompleter, self).setModel(self.model)


def set_address_completer(line_edit, is_novobl_checkbox):
    model = AddressesHintsList(is_novobl_checkbox)
    completer = QtWidgets.QCompleter(line_edit)
    completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
    completer.setModelSorting(QtWidgets.QCompleter.UnsortedModel)
    completer.setModel(model)
    line_edit.setCompleter(completer)
    line_edit.textChanged.connect(lambda: model.set_hints_for_address(line_edit.text()))

    def hint_complete():
        # За время поиска подсказки для адреса, пользователь может закрыть поле редактирования.
        try:
            completer.complete()
        except RuntimeError:
            pass

    model.hint_complete.connect(hint_complete)
