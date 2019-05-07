from PyQt5 import QtWidgets, QtCore, QtGui
from utility.address_assistant import set_address_completer
from utility.employees import Employee
from view.hw_view import HWView


class InLineEditDelegate(QtWidgets.QStyledItemDelegate):
    """Делегат для редактирования текстовых данных"""
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model

    def createEditor(self, parent, option, index):
        line_editor = super(InLineEditDelegate, self).createEditor(parent, option, index)
        return line_editor

    def setEditorData(self, editor, index):
        column = index.column()
        field_name = Employee.ALL_FIELDS[column]
        text = index.data(QtCore.Qt.EditRole)
        if field_name == 'address_free_form':
            # Подключаем кастомный комплитер для поля адреса
            set_address_completer(editor, self.parent().ui.is_nov_obl)
            editor.setText(str(text))
            return
        auto_complete = QtWidgets.QCompleter(self.model.get_completer(field_name))
        auto_complete.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        editor.setCompleter(auto_complete)
        editor.setText(str(text))


class GenderSelectionDelegate(QtWidgets.QStyledItemDelegate):
    """Делегат для выбора пола"""

    def __init__(self, parent):
        super().__init__(parent)
        self.genders = ['Мужской', 'Женский']

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QComboBox(parent)
        editor.currentIndexChanged.connect(self.commit_editor)
        editor.addItems(self.genders)
        editor.setItemIcon(0, QtGui.QIcon(':/icons/male.svg'))
        editor.setItemIcon(1, QtGui.QIcon(':/icons/female.svg'))
        return editor

    def commit_editor(self):
        editor = self.sender()
        self.commitData.emit(editor)

    def setEditorData(self, editor, index):
        try:
            value = index.data(QtCore.Qt.EditRole)
            num = self.genders.index(value)
            editor.setCurrentIndex(num)
        except ValueError:
            editor.setCurrentIndex(0)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class BirthDateSelectionDelegate(QtWidgets.QStyledItemDelegate):
    """Делегат для выбора даты рождения"""

    def __init__(self, parent):
        super().__init__(parent)
        self.date_picker = QtWidgets.QCalendarWidget()

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QDateEdit(parent)
        editor.setDisplayFormat('dd.MM.yyyy')
        editor.setDateRange(QtCore.QDate(1900, 1, 1), QtCore.QDate.currentDate().addYears(-12))
        editor.setCalendarPopup(True)
        editor.dateChanged.connect(self.commit_editor)
        return editor

    def commit_editor(self):
        editor = self.sender()
        self.commitData.emit(editor)

    def setEditorData(self, editor, index):
        birth_date = index.data(QtCore.Qt.EditRole)
        editor.setDate(birth_date)

    def setModelData(self, editor, model, index):
        birth_date = editor.date()
        str_birth_date = birth_date.toString('yyyy-MM-dd')
        model.setData(index, str_birth_date)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class ExperienceSelectionDelegate(QtWidgets.QStyledItemDelegate):
    """Делегат для выбора стажа"""

    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setRange(0, 100)
        editor.valueChanged.connect(self.commit_editor)
        return editor

    def commit_editor(self):
        editor = self.sender()
        self.commitData.emit(editor)

    def setEditorData(self, editor, index):
        number = index.data(QtCore.Qt.EditRole)
        editor.setValue(number)

    def setModelData(self, editor, model, index):
        experience = editor.value()
        str_experience = str(experience)
        model.setData(index, str_experience)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

#
# class HazardsSelectionDelegate(QtWidgets.QStyledItemDelegate):
#     """Делегат для редактирования вредностей"""
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#     def paint(self, painter, option, index):
#         pass
#         # if isinstance(self.parent(), QtWidgets.QAbstractItemView):
#         #     self.parent().openPersistentEditor(index)
#         # super(HazardsSelectionDelegate, self).paint(painter, option, index)
#
#     def createEditor(self, parent, option, index):
#         pass
#         # editor = HWView(parent=self.parent(), autoload_ui=True)
#         # return editor
#
#     def setEditorData(self, editor, index):
#         pass
#
#     def setModelData(self, editor, model, index):
#         pass


class HazardsSelectionDelegate(QtWidgets.QStyledItemDelegate):
    """Делегат для редактирования вредностей"""

    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        editor = HWView(parent=self.parent())
        return editor

    def setEditorData(self, editor, index):
        editor.showMaximized()
        hazard_types = index.siblingAtColumn(8).data(QtCore.Qt.EditRole)
        hazard_factors = index.siblingAtColumn(9).data(QtCore.Qt.EditRole)
        editor.set_hazards(hazard_types, hazard_factors)

    def setModelData(self, editor, model, index):
        # Получаем данные из редактора вредностей
        hazard_types, hazard_factors = editor.hazards()

        # Данные обновляем в исходной модели, так как прокси модель может
        # сменить индексы после первого изменения данных
        # и второе будет уже по неправильному индексу
        hazard_types_index = model.mapToSource(index.siblingAtColumn(8))
        hazard_factors_index = model.mapToSource(index.siblingAtColumn(9))

        model.sourceModel().setData(hazard_types_index, hazard_types)
        model.sourceModel().setData(hazard_factors_index, hazard_factors)
