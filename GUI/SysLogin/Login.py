# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class UI_Login(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(481, 315)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 701, 51))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 10, 35, 35))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("img/User.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(50, 10, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButtonLogin = QtWidgets.QPushButton(self.frame)
        self.pushButtonLogin.setGeometry(QtCore.QRect(291, 5, 91, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonLogin.setFont(font)
        self.pushButtonLogin.setStyleSheet("background-color: rgb(240, 80, 128);\n"
"color: rgb(255, 255, 255);")
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        self.pushButtonClose = QtWidgets.QPushButton(self.frame)
        self.pushButtonClose.setGeometry(QtCore.QRect(390, 5, 81, 40))
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
        self.frame_2.setGeometry(QtCore.QRect(0, 50, 701, 451))
        self.frame_2.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(0, 70, 481, 141))
        self.frame_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.textEditPassword = QtWidgets.QTextEdit(self.frame_3)
        self.textEditPassword.setGeometry(QtCore.QRect(170, 79, 301, 31))
        self.textEditPassword.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.textEditPassword.setObjectName("textEditPassword")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(60, 83, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.textEditUserCardNumber = QtWidgets.QTextEdit(self.frame_3)
        self.textEditUserCardNumber.setGeometry(QtCore.QRect(50, 13, 421, 31))
        self.textEditUserCardNumber.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.textEditUserCardNumber.setObjectName("textEditUserCardNumber")
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        self.label_5.setGeometry(QtCore.QRect(60, 50, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.labelSysKeyboardUsername = QtWidgets.QLabel(self.frame_3)
        self.labelSysKeyboardUsername.setGeometry(QtCore.QRect(140, 48, 28, 28))
        self.labelSysKeyboardUsername.setText("")
        self.labelSysKeyboardUsername.setPixmap(QtGui.QPixmap("../../Documents/GitHub/python-pos/img/Keyboard Icon/keyboard.png"))
        self.labelSysKeyboardUsername.setScaledContents(True)
        self.labelSysKeyboardUsername.setObjectName("labelSysKeyboardUsername")
        self.labelSyskeyboardPassword = QtWidgets.QLabel(self.frame_3)
        self.labelSyskeyboardPassword.setGeometry(QtCore.QRect(140, 79, 28, 28))
        self.labelSyskeyboardPassword.setText("")
        self.labelSyskeyboardPassword.setPixmap(QtGui.QPixmap("../../Documents/GitHub/python-pos/img/Keyboard Icon/keyboard.png"))
        self.labelSyskeyboardPassword.setScaledContents(True)
        self.labelSyskeyboardPassword.setObjectName("labelSyskeyboardPassword")
        self.labelSysKeyboardUserCardNumber = QtWidgets.QLabel(self.frame_3)
        self.labelSysKeyboardUserCardNumber.setGeometry(QtCore.QRect(10, 13, 28, 28))
        self.labelSysKeyboardUserCardNumber.setText("")
        self.labelSysKeyboardUserCardNumber.setPixmap(QtGui.QPixmap("../../Documents/GitHub/python-pos/img/Keyboard Icon/keyboard.png"))
        self.labelSysKeyboardUserCardNumber.setScaledContents(True)
        self.labelSysKeyboardUserCardNumber.setObjectName("labelSysKeyboardUserCardNumber")
        self.textEditUsername = QtWidgets.QTextEdit(self.frame_3)
        self.textEditUsername.setGeometry(QtCore.QRect(170, 46, 301, 31))
        self.textEditUsername.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.textEditUsername.setObjectName("textEditUsername")
        self.labelPrivacyPolicy = QtWidgets.QLabel(self.frame_3)
        self.labelPrivacyPolicy.setGeometry(QtCore.QRect(360, 114, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setUnderline(True)
        self.labelPrivacyPolicy.setFont(font)
        self.labelPrivacyPolicy.setStyleSheet("color: rgb(5, 159, 255);")
        self.labelPrivacyPolicy.setObjectName("labelPrivacyPolicy")
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setGeometry(QtCore.QRect(0, 210, 481, 61))
        self.frame_4.setStyleSheet("background-color: rgb(116, 116, 116);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label_6 = QtWidgets.QLabel(self.frame_4)
        self.label_6.setGeometry(QtCore.QRect(60, 5, 211, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.frame_4)
        self.label_7.setGeometry(QtCore.QRect(60, 27, 321, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_7.setObjectName("label_7")
        self.labelSysKeyboardLoginDate = QtWidgets.QLabel(self.frame_2)
        self.labelSysKeyboardLoginDate.setGeometry(QtCore.QRect(110, 36, 28, 28))
        self.labelSysKeyboardLoginDate.setText("")
        self.labelSysKeyboardLoginDate.setPixmap(QtGui.QPixmap("../../Documents/GitHub/python-pos/img/Keyboard Icon/keyboard.png"))
        self.labelSysKeyboardLoginDate.setScaledContents(True)
        self.labelSysKeyboardLoginDate.setObjectName("labelSysKeyboardLoginDate")
        self.textEditLoginDate = QtWidgets.QTextEdit(self.frame_2)
        self.textEditLoginDate.setGeometry(QtCore.QRect(150, 36, 291, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.textEditLoginDate.setFont(font)
        self.textEditLoginDate.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.textEditLoginDate.setUndoRedoEnabled(False)
        self.textEditLoginDate.setObjectName("textEditLoginDate")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(30, 40, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.radioButtonSytemDate = QtWidgets.QRadioButton(self.frame_2)
        self.radioButtonSytemDate.setGeometry(QtCore.QRect(150, 10, 101, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.radioButtonSytemDate.setFont(font)
        self.radioButtonSytemDate.setChecked(True)
        self.radioButtonSytemDate.setObjectName("radioButtonSytemDate")
        self.radioButtonLoginDate = QtWidgets.QRadioButton(self.frame_2)
        self.radioButtonLoginDate.setGeometry(QtCore.QRect(280, 10, 82, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.radioButtonLoginDate.setFont(font)
        self.radioButtonLoginDate.setObjectName("radioButtonLoginDate")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Login"))
        self.pushButtonLogin.setText(_translate("Form", "Login"))
        self.pushButtonClose.setText(_translate("Form", "Close"))
        self.label_3.setText(_translate("Form", "Password:"))
        self.label_5.setText(_translate("Form", "Username:"))
        self.labelPrivacyPolicy.setText(_translate("Form", "Privacy Policy"))
        self.label_6.setText(_translate("Form", "Easy POS Version : Alpha.001.000"))
        self.label_7.setText(_translate("Form", "Support : Human Incubator Inc. (+63) 908 8906 496"))
        self.textEditLoginDate.setPlaceholderText(_translate("Form", "__/__/____"))
        self.label_8.setText(_translate("Form", "Login Date:"))
        self.radioButtonSytemDate.setText(_translate("Form", "System Date"))
        self.radioButtonLoginDate.setText(_translate("Form", "Login Date"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = UI_Login()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())