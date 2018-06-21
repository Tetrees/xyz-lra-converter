# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_DataSelect.ui'
#
# Created: Wed Aug 14 12:25:52 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(250, 135)
        Dialog.setMinimumSize(QtCore.QSize(250, 135))
        Dialog.setMaximumSize(QtCore.QSize(250, 135))
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radioButtonXYZ = QtGui.QRadioButton(self.groupBox)
        self.radioButtonXYZ.setChecked(True)
        self.radioButtonXYZ.setObjectName(_fromUtf8("radioButtonXYZ"))
        self.horizontalLayout.addWidget(self.radioButtonXYZ)
        spacerItem = QtGui.QSpacerItem(73, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.radioButtonLRA = QtGui.QRadioButton(self.groupBox)
        self.radioButtonLRA.setObjectName(_fromUtf8("radioButtonLRA"))
        self.horizontalLayout.addWidget(self.radioButtonLRA)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.okButton = QtGui.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.okButton.setFont(font)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout_2.addWidget(self.okButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Data Type Select", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Data Type", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonXYZ.setText(QtGui.QApplication.translate("Dialog", "XYZ", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonLRA.setText(QtGui.QApplication.translate("Dialog", "LRA", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "OK", None, QtGui.QApplication.UnicodeUTF8))

