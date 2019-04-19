from PyQt5 import QtWidgets, uic, QtCore
from utility.hazards_lists_helper import HazardsListsHelper
from utility.resource_path import resource_path
from view.ui.hazards_form import Ui_HazardsForm
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence, QColor, QBrush
from PyQt5.QtWidgets import QShortcut, QMessageBox


class HWView(QtWidgets.QWidget):
    """
    Класс HWView отвечает за визуальное представление формы редактирования типов и факторво вредностей.
    (Заметка для разработчика) Для импорта UI в PY:
        pyuic5 -x .pyqt5/hazards_form.ui -o view/ui/hazards_form.py
    """
    hazardsChanged = pyqtSignal()

    def __init__(self, parent=None):

        # Подключаем Представление
        flags = Qt.WindowFlags(Qt.Window | Qt.WindowTitleHint)
        super(HWView, self).__init__(parent, flags)
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

        # Подключаем слоты кнопок
        self.ui.save_btn.clicked.connect(self.save_btn_clicked)
        QShortcut(QKeySequence(Qt.Key_Return), self, self.save_btn_clicked)

    def set_hazards(self, hazard_types, hazard_factors):
        """Загружает списки факторов и типов вредностей"""
        self.load_tree_data(self.types_tree, self.hazards_types, 'hazard_types', hazard_types)
        self.load_tree_data(self.factors_tree, self.hazards_factors, 'hazard_factors', hazard_factors)
        self.types_tree.resizeColumnToContents(0)
        self.factors_tree.resizeColumnToContents(0)
        self.update_summaries()

    def hazards(self):
        """Возвращает списки факторов и типов вредностей"""
        hazard_types = list()
        for i in range(self.types_tree.topLevelItemCount()):
            self.__fill_hazards_list(self.types_tree.topLevelItem(i), hazard_types)
        hazard_factors = list()
        for i in range(self.factors_tree.topLevelItemCount()):
            self.__fill_hazards_list(self.factors_tree.topLevelItem(i), hazard_factors)
        return hazard_types, hazard_factors

    def load_tree_data(self, tree, data, mode, emp_hazards):
        """Создаем незаполненные деревья вредностей (интерфейс)"""
        # tree.setColumnWidth(0, 550)
        top_level_items = data.root.childs
        for top_level_item in top_level_items:
            root = QtWidgets.QTreeWidgetItem([top_level_item.get_full_code(), top_level_item.name])
            root.setToolTip(1, '<div style="width: 80px;">{}</div>'.format(top_level_item.name))
            self.__fill_the_brunch(top_level_item, root)
            tree.addTopLevelItem(root)
            self.__add_checkboxes(root, mode, emp_hazards)
        tree.expandAll()
        tree.clicked.connect(self.update_summaries)

    def __add_checkboxes(self, node, mode, emp_hazards):
        child_count = node.childCount()
        if not child_count:
            node.setFlags(node.flags() | Qt.ItemIsUserCheckable)
            if node.text(0) in emp_hazards:
                node.setCheckState(0, Qt.Checked)
            else:
                node.setCheckState(0, Qt.Unchecked)
        else:
            node.setFlags(node.flags() | Qt.ItemIsUserCheckable)
            if node.text(0) in emp_hazards:
                node.setCheckState(0, Qt.Checked)
            else:
                node.setCheckState(0, Qt.Unchecked)
            for i in range(child_count):
                self.__add_checkboxes(node.child(i), mode, emp_hazards)

    def save_btn_clicked(self):
        self.hazardsChanged.emit()
        self.close()

    def __fill_hazards_list(self, node, hazard_list):
        """Заполняет список отмеченными в дереве вредностями"""
        child_count = node.childCount()
        code = node.text(0)
        if node.checkState(0):
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
                q_item_child = QtWidgets.QTreeWidgetItem([child.get_full_code(), child.name])
                q_item_child.setToolTip(1, '<div style="width: 80px;">{}</div>'.format(child.name))
                self.__fill_the_brunch(child, q_item_child)
                q_tree_item.addChild(q_item_child)

    def update_summaries(self):
        hazard_types, hazard_factors = self.hazards()
        self.ui.types_summary.setText(" / ".join(hazard_types))
        self.ui.factors_summary.setText(" / ".join(hazard_factors))
