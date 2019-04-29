# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.pyqt5/save_list.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SaveListForm(object):
    def setupUi(self, SaveListForm):
        SaveListForm.setObjectName("SaveListForm")
        SaveListForm.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(SaveListForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.save_list = QtWidgets.QListWidget(SaveListForm)
        self.save_list.setObjectName("save_list")
        self.verticalLayout.addWidget(self.save_list)
        self.hl_main_layout = QtWidgets.QHBoxLayout()
        self.hl_main_layout.setObjectName("hl_main_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hl_main_layout.addItem(spacerItem)
        self.load_btn = QtWidgets.QPushButton(SaveListForm)
        self.load_btn.setObjectName("load_btn")
        self.hl_main_layout.addWidget(self.load_btn)
        self.cancel_btn = QtWidgets.QPushButton(SaveListForm)
        self.cancel_btn.setObjectName("cancel_btn")
        self.hl_main_layout.addWidget(self.cancel_btn)
        self.verticalLayout.addLayout(self.hl_main_layout)

        self.retranslateUi(SaveListForm)
        QtCore.QMetaObject.connectSlotsByName(SaveListForm)

    def retranslateUi(self, SaveListForm):
        _translate = QtCore.QCoreApplication.translate
        SaveListForm.setWindowTitle(_translate("SaveListForm", "Список автосохранений"))
        self.load_btn.setText(_translate("SaveListForm", "Загрузить"))
        self.cancel_btn.setText(_translate("SaveListForm", "Отмена"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SaveListForm = QtWidgets.QWidget()
    ui = Ui_SaveListForm()
    ui.setupUi(SaveListForm)
    SaveListForm.show()
    sys.exit(app.exec_())
