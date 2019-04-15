from PyQt5 import QtWidgets, QtCore, QtGui


class InLineEditDelegate(QtWidgets.QItemDelegate):
    """Делегат для редактирования текстовых данных"""
    def __init__(self, owner, model):
        super().__init__(owner)
        self.model = model

    def createEditor(self, parent, option, index):
        line_editor = super(InLineEditDelegate, self).createEditor(parent, option, index)
        return line_editor

    def setEditorData(self, editor, index):
        text = index.data(QtCore.Qt.EditRole)
        variants = set()
        for row in range(0, self.model.rowCount()):
            variants.add(self.model.index(row, index.column()).data())
        auto_complete = QtWidgets.QCompleter(variants)
        editor.setCompleter(auto_complete)
        editor.setText(str(text))


class GenderSelectionDelegate(QtWidgets.QStyledItemDelegate):
    """Делегат для выбора пола"""

    def __init__(self, owner):
        super().__init__(owner)
        self.genders = ['Мужской', 'Женский']

    def paint(self, painter, option, index):
        if isinstance(self.parent(), QtWidgets.QAbstractItemView):
            self.parent().openPersistentEditor(index)
        super(GenderSelectionDelegate, self).paint(painter, option, index)

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
        value = index.data(QtCore.Qt.DisplayRole)
        num = self.genders.index(value)
        editor.setCurrentIndex(num)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)

    # def updateEditorGeometry(self, editor, option, index):
    #     editor.setGeometry(option.rect)


class BirthDateSelectionDelegate(QtWidgets.QStyledItemDelegate):
    """Делегат для выбора даты рождения"""

    def __init__(self, owner):
        super().__init__(owner)
        self.date_picker = QtWidgets.QCalendarWidget()

    def paint(self, painter, option, index):
        if isinstance(self.parent(), QtWidgets.QAbstractItemView):
            self.parent().openPersistentEditor(index)
        super(BirthDateSelectionDelegate, self).paint(painter, option, index)

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

    def __init__(self, owner):
        super().__init__(owner)

    def paint(self, painter, option, index):
        if isinstance(self.parent(), QtWidgets.QAbstractItemView):
            self.parent().openPersistentEditor(index)
        super(ExperienceSelectionDelegate, self).paint(painter, option, index)

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


class EmployeesHazardsDelegate(QtWidgets.QStyledItemDelegate):
    """Делегат для редактирования и отображения вредностей"""

    # TODO: Доделать

    def __init__(self, parent=None):
        """Инициализация делегата"""
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        """Создание редактора"""
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        """Передача данных в редактор"""
        return super().setEditorData(editor, index)

    # def setModelData(self, editor, model, index):
    # row = index.row()
    # column = index.column()
    # field_name = Employee.ALL_FIELDS[column]
    # emp_id = tuple(self.employees.keys())[row]
    #
    # if field_name in Employee.LIST_FIELDS:
    #     return len(self.employees[emp_id][field_name])
    #
    # data_int = editor.value()
    # data_var = QVariant(data_int)

    # model.setData(index, self.__generate_hazard_cell(editor.text()))
    # print(editor, model, index)

    @staticmethod
    def __generate_hazard_cell(hazard_codes):
        """Создает ряд скругленных ячеек вредностей для таблицы"""
        if type(hazard_codes) == str:
            hazard_codes = hazard_codes.split(',')
        hazards_layout = QtWidgets.QHBoxLayout()
        hazards_cell = QtWidgets.QWidget()
        hazards_cell.setLayout(hazards_layout)
        for hazard_code in hazard_codes:
            if hazard_code.endswith('.'):
                hazard_code = hazard_code[:-1]
            hazard_label = QtWidgets.QLabel(hazard_code)
            hazard_label.setStyleSheet('background-color: #fff; border-radius: 5px; padding: 2px;'
                                       'min-height: 15px; border: 1px solid;')
            hazards_layout.addWidget(hazard_label)
        h_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding)
        hazards_layout.addSpacerItem(h_spacer)
        return hazards_cell


class HazardsSelectionDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        # painter.save()
        #
        # # set background color
        # painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        # if option.state & QtWidgets.QStyle.State_Selected:
        #     painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
        # else:
        #     painter.setBrush(QtGui.QBrush(QtCore.Qt.green))
        # painter.drawRect(option.rect)
        #
        # # set text color
        # painter.setPen(QtGui.QPen(QtCore.Qt.black))
        # value = index.data(QtCore.Qt.DisplayRole)
        # if index.isValid():
        #     painter.drawText(option.rect, QtCore.Qt.AlignCenter, value)
        #
        # painter.restore()
        print(self.__generate_hazard_cell(index.data()))


    @staticmethod
    def __generate_hazard_cell(hazard_codes):
        """Создает ряд скругленных ячеек вредностей для таблицы"""
        if type(hazard_codes) == str:
            hazard_codes = hazard_codes.split(',')
        hazards_layout = QtWidgets.QHBoxLayout()
        hazards_cell = QtWidgets.QWidget()
        hazards_cell.setLayout(hazards_layout)
        for hazard_code in hazard_codes:
            if hazard_code.endswith('.'):
                hazard_code = hazard_code[:-1]
            hazard_label = QtWidgets.QLabel(hazard_code)
            hazard_label.setStyleSheet('background-color: #fff; border-radius: 5px; padding: 2px;'
                                       'min-height: 15px; border: 1px solid;')
            hazards_layout.addWidget(hazard_label)
        h_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding)
        hazards_layout.addSpacerItem(h_spacer)
        return hazards_cell
