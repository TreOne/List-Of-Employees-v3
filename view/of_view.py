from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

from utility.organization import Organization
from view.ui.organization_form import Ui_OrganizationForm
from PyQt5.QtCore import Qt


class OFView(QtWidgets.QWidget):
    """
    Класс OFView отвечает за визуальное представление модального окна для изменения данных организации.
    (Заметка для разработчика) Для импорта UI в PY:
        pyuic5 -x .pyqt5/organization_form.ui -o view/ui/organization_form.py
    """

    def __init__(self, organization_data, parent=None):
        flags = Qt.WindowFlags(Qt.Dialog | Qt.WindowSystemMenuHint | Qt.MSWindowsFixedSizeDialogHint)
        super(OFView, self).__init__(parent, flags)
        self.ui = Ui_OrganizationForm()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle("Данные организации")
        self.parent = parent

        for field in Organization.ALL_FIELDS:
            ui_field = getattr(self.ui, field)
            ui_field.setText(organization_data[field])

        self.ui.cancel_btn.clicked.connect(self.close)
        QShortcut(QKeySequence(Qt.Key_Escape), self, self.close)
        self.ui.save_btn.clicked.connect(self.save_btn_clicked)
        QShortcut(QKeySequence(Qt.Key_Return), self, self.save_btn_clicked)

    def save_btn_clicked(self):
        new_data = dict()
        for field in Organization.ALL_FIELDS:
            ui_field = getattr(self.ui, field)
            new_data[field] = ui_field.text()
        self.parent.organization = new_data
        self.parent.fill_organization_fields()
        self.parent.data_changed()
        self.close()
