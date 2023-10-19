# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TerminalDetail.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class UI_TerminalDetail(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 125)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 450, 61))
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
        self.lblTerminalDetail = QtWidgets.QLabel(self.frame)
        self.lblTerminalDetail.setGeometry(QtCore.QRect(50, 10, 160, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lblTerminalDetail.setFont(font)
        self.lblTerminalDetail.setObjectName("lblTerminalDetail")
        self.btnSave = QtWidgets.QPushButton(self.frame)
        self.btnSave.setGeometry(QtCore.QRect(260, 10, 91, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnSave.setFont(font)
        self.btnSave.setStyleSheet("background-color: rgb(240, 80, 128);\n"
"color: rgb(255, 255, 255);")
        self.btnSave.setObjectName("btnSave")
        self.btnClose = QtWidgets.QPushButton(self.frame)
        self.btnClose.setGeometry(QtCore.QRect(360, 10, 81, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnClose.setFont(font)
        self.btnClose.setStyleSheet("background-color: rgb(243, 79, 28);\n"
"color: rgb(255, 255, 255);")
        self.btnClose.setObjectName("btnClose")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(0, 60, 450, 190))
        self.frame_2.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.txtTerminal = QtWidgets.QTextEdit(self.frame_2)
        self.txtTerminal.setGeometry(QtCore.QRect(140, 10, 300, 31))
        self.txtTerminal.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.txtTerminal.setObjectName("txtTerminal")
        self.lblTerminal = QtWidgets.QLabel(self.frame_2)
        self.lblTerminal.setGeometry(QtCore.QRect(10, 10, 120, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.lblTerminal.setFont(font)
        self.lblTerminal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblTerminal.setObjectName("lblTerminal")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lblTerminalDetail.setText(_translate("Form", "Terminal Detail"))
        self.btnSave.setText(_translate("Form", "Enter - Save"))
        self.btnClose.setText(_translate("Form", "Esc - Close"))
        self.lblTerminal.setText(_translate("Form", "Terminal:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = UI_TerminalDetail()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
