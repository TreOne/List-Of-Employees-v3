from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from view.ui.save_list import Ui_SaveListForm
from PyQt5.QtCore import Qt


class SLView(QtWidgets.QWidget):
    """
    Класс SLView отвечает за визуальное представление списка автосохранений.
    (Заметка для разработчика) Для импорта UI в PY:
        pyuic5 -x .pyqt5/save_list.ui -o view/ui/save_list.py
    """
    def __init__(self, auto_saver, parent=None):
        flags = Qt.WindowFlags(Qt.Dialog | Qt.WindowSystemMenuHint | Qt.MSWindowsFixedSizeDialogHint)
        super(SLView, self).__init__(parent, flags)
        self.ui = Ui_SaveListForm()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModal)

        self.auto_saver = auto_saver
        self.__fill_save_list()

        self.ui.cancel_btn.clicked.connect(self.close)
        QShortcut(QKeySequence(Qt.Key_Escape), self, self.close)
        self.ui.load_btn.clicked.connect(self.load_btn_clicked)
        QShortcut(QKeySequence(Qt.Key_Return), self, self.load_btn_clicked)

    def load_btn_clicked(self):
        selected_save = self.ui.save_list.selectedItems()[0]
        filename = selected_save.toolTip()
        self.parent().load_file(filename, save_last_path=False)
        self.close()

    def cancel_btn_clicked(self):
        self.close()

    def __fill_save_list(self):
        for menu_name, menu_path in self.auto_saver.get_saves_list().values():
            item = QtWidgets.QListWidgetItem(menu_name)
            item.setToolTip(menu_path)
            self.ui.save_list.addItem(item)
