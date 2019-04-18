from PyQt5 import QtWidgets, QtCore
from view.ui.organization_form import Ui_OrganizationForm
from PyQt5.QtCore import Qt


class OFView(QtWidgets.QWidget):
    """
    Класс OFView отвечает за визуальное представление модального окна для изменения данных организации.
    (Заметка для разработчика) Для импорта UI в PY:
        pyuic5 -x .pyqt5/organization_form.ui -o view/ui/organization_form.py
    """

    def __init__(self, controller, organization_data, parent=None):
        flags = Qt.WindowFlags(Qt.Dialog | Qt.WindowSystemMenuHint | Qt.MSWindowsFixedSizeDialogHint)
        super(OFView, self).__init__(parent, flags)
        self.ui = Ui_OrganizationForm()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle("Данные организации")
        self.controller = controller
        self.parent = parent

        self.ui.org_name.setText(organization_data['org_name'])
        self.ui.inn.setText(organization_data['inn'])
        self.ui.ogrn.setText(organization_data['ogrn'])
        self.ui.org_address.setText(organization_data['org_address'])
        self.ui.head_full_name.setText(organization_data['head_full_name'])
        self.ui.representative_full_name.setText(organization_data['representative_full_name'])
        self.ui.representative_position.setText(organization_data['representative_position'])

        self.ui.cancel_btn.clicked.connect(self.close)
        self.ui.save_btn.clicked.connect(self.save_btn_clicked)

    def save_btn_clicked(self):
        org_name = self.ui.org_name.text()
        inn = self.ui.inn.text()
        ogrn = self.ui.ogrn.text()
        org_address = self.ui.org_address.text()
        head_full_name = self.ui.head_full_name.text()
        representative_full_name = self.ui.representative_full_name.text()
        representative_position = self.ui.representative_position.text()
        new_data = {'org_name': org_name, 'inn': inn, 'ogrn': ogrn, 'org_address': org_address,
                    'head_full_name': head_full_name, 'representative_full_name': representative_full_name,
                    'representative_position': representative_position}
        self.controller.organization = new_data
        self.parent.fill_organization_fields()
        self.close()
