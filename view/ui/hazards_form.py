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
        self.hl_summary = QtWidgets.QHBoxLayout()
        self.hl_summary.setObjectName("hl_summary")
        self.fl_types_summary = QtWidgets.QFormLayout()
        self.fl_types_summary.setObjectName("fl_types_summary")
        self.types_summary_label = QtWidgets.QLabel(HazardsForm)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.types_summary_label.setFont(font)
        self.types_summary_label.setObjectName("types_summary_label")
        self.fl_types_summary.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.types_summary_label)
        self.types_summary = QtWidgets.QLabel(HazardsForm)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.types_summary.setFont(font)
        self.types_summary.setText("")
        self.types_summary.setObjectName("types_summary")
        self.fl_types_summary.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.types_summary)
        self.hl_summary.addLayout(self.fl_types_summary)
        self.fl_factors_summary = QtWidgets.QFormLayout()
        self.fl_factors_summary.setObjectName("fl_factors_summary")
        self.factors_summary_label = QtWidgets.QLabel(HazardsForm)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.factors_summary_label.setFont(font)
        self.factors_summary_label.setObjectName("factors_summary_label")
        self.fl_factors_summary.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.factors_summary_label)
        self.factors_summary = QtWidgets.QLabel(HazardsForm)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.factors_summary.setFont(font)
        self.factors_summary.setText("")
        self.factors_summary.setObjectName("factors_summary")
        self.fl_factors_summary.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.factors_summary)
        self.hl_summary.addLayout(self.fl_factors_summary)
        self.verticalLayout.addLayout(self.hl_summary)
        self.fl_hazards_btns = QtWidgets.QHBoxLayout()
        self.fl_hazards_btns.setObjectName("fl_hazards_btns")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.fl_hazards_btns.addItem(spacerItem)
        self.save_btn = QtWidgets.QPushButton(HazardsForm)
        self.save_btn.setMinimumSize(QtCore.QSize(200, 30))
        self.save_btn.setObjectName("save_btn")
        self.fl_hazards_btns.addWidget(self.save_btn)
        self.verticalLayout.addLayout(self.fl_hazards_btns)

        self.retranslateUi(HazardsForm)
        QtCore.QMetaObject.connectSlotsByName(HazardsForm)
        HazardsForm.setTabOrder(self.hazards_types, self.hazards_factors)
        HazardsForm.setTabOrder(self.hazards_factors, self.save_btn)

    def retranslateUi(self, HazardsForm):
        _translate = QtCore.QCoreApplication.translate
        HazardsForm.setWindowTitle(_translate("HazardsForm", "Form"))
        self.hazards_types.headerItem().setText(0, _translate("HazardsForm", "Код"))
        self.hazards_types.headerItem().setText(1, _translate("HazardsForm", "Тип вредности (Приложение 2)"))
        self.hazards_factors.headerItem().setText(0, _translate("HazardsForm", "Код"))
        self.hazards_factors.headerItem().setText(1, _translate("HazardsForm", "Фактор вредности (Приложение 1)"))
        self.types_summary_label.setText(_translate("HazardsForm", "Выбраны типы:"))
        self.factors_summary_label.setText(_translate("HazardsForm", "Выбраны факторы:"))
        self.save_btn.setText(_translate("HazardsForm", "Сохранить и закрыть (Enter)"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HazardsForm = QtWidgets.QWidget()
    ui = Ui_HazardsForm()
    ui.setupUi(HazardsForm)
    HazardsForm.show()
    sys.exit(app.exec_())
