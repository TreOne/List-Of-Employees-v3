from PyQt5 import QtWidgets, uic, QtCore
from utility.hazards_lists_helper import HazardsListsHelper
from utility.resource_path import resource_path
from view.ui.hazards_form import Ui_HazardsForm
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QColor, QBrush
from PyQt5.QtWidgets import QShortcut, QMessageBox


class HFView(QtWidgets.QWidget):
    """
    Класс HFView отвечает за визуальное представление формы редактирования типов и факторво вредностей.
    (Заметка для разработчика) Для импорта UI в PY:
        pyuic5 -x .pyqt5/hazards_form.ui -o view/ui/hazards_form.py
    """

    def __init__(self, parent=None, autoload_ui=False):

        # Подключаем Представление
        flags = Qt.WindowFlags(Qt.Window | Qt.WindowTitleHint)
        super(HFView, self).__init__(parent, flags)

        # Подключаем UI
        # TODO: При релизе, переключить с динамической компиляции интерфейса на статическую.
        if autoload_ui:
            self.ui = uic.loadUi(resource_path('.pyqt5/hazards_form.ui'), self)
        else:
            self.ui = Ui_HazardsForm()
            self.ui.setupUi(self)

        # Настраиваем внешний вид окна
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle("Типы и факторы вредностей")

        # Загружаем деревья вредностей
        self.hazards_lists_helper = HazardsListsHelper()
        self.hazards_types = self.hazards_lists_helper.get_hazard_types_tree()
        self.hazards_factors = self.hazards_lists_helper.get_hazard_factors_tree()
        self.types_tree = self.ui.hazards_types
        self.factors_tree = self.ui.hazards_factors

        # # Визуализируем деревья вредностей
        # self.load_tree_data(self.types_tree, self.hazards_types, 'hazard_types')
        # self.load_tree_data(self.factors_tree, self.hazards_factors, 'hazard_factors')

        # # При двойном клике отмечаем вредность
        # self.types_tree.itemDoubleClicked.connect(self.item_double_clicked)
        # self.factors_tree.itemDoubleClicked.connect(self.item_double_clicked)

        # Подключаем слоты кнопок
        self.ui.cancel_btn.clicked.connect(self.cancel_btn_clicked)
        QShortcut(QKeySequence(Qt.Key_Escape), self, self.cancel_btn_clicked)
        self.ui.save_btn.clicked.connect(self.save_btn_clicked)
        QShortcut(QKeySequence(Qt.Key_F5), self, self.save_btn_clicked)

    def item_double_clicked(self, item):
        if item.childCount() == 0:
            if item.checkState(2):
                item.setCheckState(2, Qt.Unchecked)
            else:
                item.setCheckState(2, Qt.Checked)

    def set_hazards(self, hazard_types, hazard_factors):
        """Загружает списки факторов и типов вредностей"""
        self.load_tree_data(self.types_tree, hazard_types, 'hazard_types')
        self.load_tree_data(self.factors_tree, hazard_factors, 'hazard_factors')

    def hazards(self):
        """Возвращает списки факторов и типов вредностей"""
        hazard_types = list()
        for i in range(self.types_tree.topLevelItemCount()):
            self.__fill_hazards_list(self.types_tree.topLevelItem(i), hazard_types)
        hazard_factors = list()
        for i in range(self.factors_tree.topLevelItemCount()):
            self.__fill_hazards_list(self.factors_tree.topLevelItem(i), hazard_factors)
        return hazard_types, hazard_factors

    def load_tree_data(self, tree, data, mode):
        tree.setColumnWidth(0, 550)
        top_level_items = data.root.childs
        for top_level_item in top_level_items:
            root = QtWidgets.QTreeWidgetItem([top_level_item.name, top_level_item.get_full_code()])
            self.__fill_the_brunch(top_level_item, root)
            tree.addTopLevelItem(root)
            self.__add_checkboxes(root, mode)
        tree.expandAll()

    def __add_checkboxes(self, node, mode):
        hazards = self.employee[mode]
        child_count = node.childCount()
        if not child_count:
            node.setFlags(node.flags() | Qt.ItemIsUserCheckable)
            if node.text(1) + '.' in hazards:
                node.setCheckState(2, Qt.Checked)
            else:
                node.setCheckState(2, Qt.Unchecked)
        else:
            node.setFlags(node.flags() | Qt.ItemIsUserCheckable)
            if node.text(1) in hazards:
                node.setCheckState(2, Qt.Checked)
            else:
                node.setCheckState(2, Qt.Unchecked)
            for i in range(child_count):
                self.__add_checkboxes(node.child(i), mode)

    def save_btn_clicked(self):
        employee_hazards = self.employee['hazard_types']
        employee_hazards.clear()
        for i in range(self.types_tree.topLevelItemCount()):
            self.__fill_hazards_list(self.types_tree.topLevelItem(i), employee_hazards)
        employee_hazards = self.employee['hazard_factors']
        employee_hazards.clear()
        for i in range(self.factors_tree.topLevelItemCount()):
            self.__fill_hazards_list(self.factors_tree.topLevelItem(i), employee_hazards)
        self.controller.update_hazards_count()
        self.close()

    def cancel_btn_clicked(self):
        types_codes = []
        for i in range(self.types_tree.topLevelItemCount()):
            self.__fill_hazards_list(self.types_tree.topLevelItem(i), types_codes)
        factors_codes = []
        for i in range(self.factors_tree.topLevelItemCount()):
            self.__fill_hazards_list(self.factors_tree.topLevelItem(i), factors_codes)

        types_codes.sort()
        self.controller.changed_employee['hazard_types'].sort()
        factors_codes.sort()
        self.controller.changed_employee['hazard_factors'].sort()
        if types_codes != self.controller.changed_employee['hazard_types'] or \
                factors_codes != self.controller.changed_employee['hazard_factors']:
            are_changed = True
        else:
            print(types_codes)
            are_changed = False

        if not are_changed:
            self.close()
        else:
            reply = QMessageBox.question(self, 'Вы не сохранили изменения!',
                                         'Все несохраненные изменения будут потеряны. Сохранить сделанные изменения?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.save_btn_clicked()
            elif reply == QMessageBox.No:
                self.close()

    def __fill_hazards_list(self, node, hazard_list):
        """Заполняет список отмеченными в дереве вредностями"""
        child_count = node.childCount()
        if node.text(1).endswith('.'):
            code = node.text(1)
        else:
            code = node.text(1) + '.'
        if node.checkState(2):
            hazard_list.append(code)
        # Если у узла есть дети, то рекурсивно вызываем эту же функцию для каждого потомка
        if child_count:
            for i in range(child_count):
                self.__fill_hazards_list(node.child(i), hazard_list)

    def __fill_the_brunch(self, node, q_tree_item):
        if len(node.childs) == 0:
            return
        else:
            bg_color = QBrush(QColor(179, 196, 212, 150))
            q_tree_item.setBackground(0, bg_color)
            q_tree_item.setBackground(1, bg_color)
            q_tree_item.setBackground(2, bg_color)
            for child in node.childs:
                q_item_child = QtWidgets.QTreeWidgetItem([child.name, child.get_full_code()])
                self.__fill_the_brunch(child, q_item_child)
                q_tree_item.addChild(q_item_child)
