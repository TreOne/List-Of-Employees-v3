# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.pyqt5/hazards_form.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HazardsForm(object):
    def setupUi(self, HazardsForm):
        HazardsForm.setObjectName("HazardsForm")
        HazardsForm.resize(1631, 860)
        self.verticalLayout = QtWidgets.QVBoxLayout(HazardsForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hl_hazards = QtWidgets.QHBoxLayout()
        self.hl_hazards.setObjectName("hl_hazards")
        self.hazards_types = QtWidgets.QTreeWidget(HazardsForm)
        self.hazards_types.setObjectName("hazards_types")
        self.hazards_types.header().setStretchLastSection(True)
        self.hl_hazards.addWidget(self.hazards_types)
        self.hazards_factors = QtWidgets.QTreeWidget(HazardsForm)
        self.hazards_factors.setObjectName("hazards_factors")
        self.hazards_factors.header().setStretchLastSection(True)
        self.hl_hazards.addWidget(self.hazards_factors)
        self.hl_hazards.setStretch(0, 1)
        self.hl_hazards.setStretch(1, 1)
        self.verticalLayout.addLayout(self.hl_hazards)
        self.al_hazards_btns = QtWidgets.QHBoxLayout()
        self.al_hazards_btns.setObjectName("al_hazards_btns")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.al_hazards_btns.addItem(spacerItem)
        self.save_btn = QtWidgets.QPushButton(HazardsForm)
        self.save_btn.setMinimumSize(QtCore.QSize(200, 30))
        self.save_btn.setObjectName("save_btn")
        self.al_hazards_btns.addWidget(self.save_btn)
        self.verticalLayout.addLayout(self.al_hazards_btns)

        self.retranslateUi(HazardsForm)
        QtCore.QMetaObject.connectSlotsByName(HazardsForm)

    def retranslateUi(self, HazardsForm):
        _translate = QtCore.QCoreApplication.translate
        HazardsForm.setWindowTitle(_translate("HazardsForm", "Form"))
        self.hazards_types.headerItem().setText(0, _translate("HazardsForm", "Код"))
        self.hazards_types.headerItem().setText(1, _translate("HazardsForm", "Тип вредности (Приложение 2)"))
        self.hazards_factors.headerItem().setText(0, _translate("HazardsForm", "Код"))
        self.hazards_factors.headerItem().setText(1, _translate("HazardsForm", "Фактор вредности (Приложение 1)"))
        self.save_btn.setText(_translate("HazardsForm", "Сохранить и закрыть"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HazardsForm = QtWidgets.QWidget()
    ui = Ui_HazardsForm()
    ui.setupUi(HazardsForm)
    HazardsForm.show()
    sys.exit(app.exec_())
