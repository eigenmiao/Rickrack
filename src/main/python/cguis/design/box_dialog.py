# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\python\cguis\design\box_dialog.ui'
#
# Created by: PySide2 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_BoxDialog(object):
    def setupUi(self, BoxDialog):
        BoxDialog.setObjectName("BoxDialog")
        BoxDialog.resize(640, 300)
        BoxDialog.setWindowTitle("Dialog")
        self.gridLayout = QtWidgets.QGridLayout(BoxDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.color_box = QtWidgets.QWidget(BoxDialog)
        self.color_box.setMinimumSize(QtCore.QSize(240, 160))
        self.color_box.setMaximumSize(QtCore.QSize(240, 240))
        self.color_box.setObjectName("color_box")
        self.gridLayout.addWidget(self.color_box, 0, 0, 4, 1)
        self.info_label = QtWidgets.QLabel(BoxDialog)
        self.info_label.setMinimumSize(QtCore.QSize(250, 60))
        self.info_label.setMaximumSize(QtCore.QSize(250, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.info_label.setFont(font)
        self.info_label.setObjectName("info_label")
        self.gridLayout.addWidget(self.info_label, 0, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.name_label = QtWidgets.QLabel(BoxDialog)
        self.name_label.setMinimumSize(QtCore.QSize(120, 30))
        self.name_label.setMaximumSize(QtCore.QSize(120, 30))
        self.name_label.setObjectName("name_label")
        self.gridLayout.addWidget(self.name_label, 1, 1, 1, 1)
        self.name_ledit = QtWidgets.QLineEdit(BoxDialog)
        self.name_ledit.setMinimumSize(QtCore.QSize(200, 30))
        self.name_ledit.setMaximumSize(QtCore.QSize(800, 30))
        self.name_ledit.setObjectName("name_ledit")
        self.gridLayout.addWidget(self.name_ledit, 1, 2, 1, 1)
        self.hec_label = QtWidgets.QLabel(BoxDialog)
        self.hec_label.setMinimumSize(QtCore.QSize(120, 30))
        self.hec_label.setMaximumSize(QtCore.QSize(120, 30))
        self.hec_label.setObjectName("hec_label")
        self.gridLayout.addWidget(self.hec_label, 2, 1, 1, 1)
        self.hec_ledit = QtWidgets.QLineEdit(BoxDialog)
        self.hec_ledit.setMinimumSize(QtCore.QSize(200, 30))
        self.hec_ledit.setMaximumSize(QtCore.QSize(800, 30))
        self.hec_ledit.setObjectName("hec_ledit")
        self.gridLayout.addWidget(self.hec_ledit, 2, 2, 1, 1)
        self.index_label = QtWidgets.QLabel(BoxDialog)
        self.index_label.setMinimumSize(QtCore.QSize(120, 30))
        self.index_label.setMaximumSize(QtCore.QSize(120, 30))
        self.index_label.setObjectName("index_label")
        self.gridLayout.addWidget(self.index_label, 3, 1, 1, 1)
        self.index_spb = QtWidgets.QSpinBox(BoxDialog)
        self.index_spb.setMinimumSize(QtCore.QSize(200, 30))
        self.index_spb.setMaximumSize(QtCore.QSize(800, 30))
        self.index_spb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.index_spb.setObjectName("index_spb")
        self.gridLayout.addWidget(self.index_spb, 3, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(558, 62, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 3)
        self.buttonBox = QtWidgets.QDialogButtonBox(BoxDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 4)

        self.retranslateUi(BoxDialog)
        self.buttonBox.accepted.connect(BoxDialog.accept)
        self.buttonBox.rejected.connect(BoxDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BoxDialog)

    def retranslateUi(self, BoxDialog):
        _translate = QtCore.QCoreApplication.translate
        self.info_label.setText(_translate("BoxDialog", "Color Box Information"))
        self.name_label.setText(_translate("BoxDialog", "Name:"))
        self.hec_label.setText(_translate("BoxDialog", "Color:"))
        self.index_label.setText(_translate("BoxDialog", "Index:"))


