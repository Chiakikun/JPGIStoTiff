# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\JPGIS(GML)toASCII_Form.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(278, 236)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 200, 241, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 151, 16))
        self.label.setObjectName("label")
        self.LoadFolderPath = QtWidgets.QLineEdit(Dialog)
        self.LoadFolderPath.setGeometry(QtCore.QRect(10, 30, 241, 20))
        self.LoadFolderPath.setObjectName("LoadFolderPath")
        self.LoadFolderSelect = QtWidgets.QPushButton(Dialog)
        self.LoadFolderSelect.setGeometry(QtCore.QRect(250, 30, 21, 23))
        self.LoadFolderSelect.setText("")
        self.LoadFolderSelect.setObjectName("LoadFolderSelect")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 21, 16))
        self.label_2.setObjectName("label_2")
        self.LogViewer = QtWidgets.QTextEdit(Dialog)
        self.LogViewer.setGeometry(QtCore.QRect(11, 80, 255, 111))
        self.LogViewer.setObjectName("LogViewer")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.LoadFolderSelect.clicked.connect(Dialog.LoadFolderSelect)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "JPGIStoAsciiGrid"))
        self.label.setText(_translate("Dialog", "zipファイルが置いてあるフォルダ"))
        self.label_2.setText(_translate("Dialog", "ログ"))
