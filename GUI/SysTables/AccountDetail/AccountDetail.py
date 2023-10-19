# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AccountDetail.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AccountDetail(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(394, 182)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 391, 61))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 10, 35, 35))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("img/System Tables.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(50, 10, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButtonSave = QtWidgets.QPushButton(self.frame)
        self.pushButtonSave.setGeometry(QtCore.QRect(200, 10, 91, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonSave.setFont(font)
        self.pushButtonSave.setStyleSheet("background-color: rgb(240, 80, 128);\n"
"color: rgb(255, 255, 255);")
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.pushButtonClose = QtWidgets.QPushButton(self.frame)
        self.pushButtonClose.setGeometry(QtCore.QRect(299, 10, 81, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonClose.setFont(font)
        self.pushButtonClose.setStyleSheet("background-color: rgb(243, 79, 28);\n"
"color: rgb(255, 255, 255);")
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(0, 60, 391, 121))
        self.frame_2.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.textEditAccountCode = QtWidgets.QTextEdit(self.frame_2)
        self.textEditAccountCode.setGeometry(QtCore.QRect(100, 5, 281, 31))
        self.textEditAccountCode.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.textEditAccountCode.setObjectName("textEditAccountCode")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(20, 45, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.textEditAccount = QtWidgets.QTextEdit(self.frame_2)
        self.textEditAccount.setGeometry(QtCore.QRect(100, 40, 281, 31))
        self.textEditAccount.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.textEditAccount.setObjectName("textEditAccount")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(20, 80, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.comboBoxAccountType = QtWidgets.QComboBox(self.frame_2)
        self.comboBoxAccountType.setGeometry(QtCore.QRect(100, 75, 281, 31))
        self.comboBoxAccountType.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.comboBoxAccountType.setObjectName("comboBoxAccountType")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Account Detail"))
        self.pushButtonSave.setText(_translate("Form", "Enter - Save"))
        self.pushButtonClose.setText(_translate("Form", "Esc - Close"))
        self.label_4.setText(_translate("Form", "Code:"))
        self.label_5.setText(_translate("Form", "Account:"))
        self.label_6.setText(_translate("Form", "Type:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_AccountDetail()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
