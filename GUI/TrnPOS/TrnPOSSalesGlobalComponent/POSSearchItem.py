# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'POSSearchItem.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 400)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 700, 60))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 10, 38, 32))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("img/POS.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(60, 10, 220, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(1200, 10, 70, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("background-color: rgb(240, 80, 128);\n"
"color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(1280, 10, 70, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(243, 79, 28);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButtonClose = QtWidgets.QPushButton(Dialog)
        self.pushButtonClose.setGeometry(QtCore.QRect(589, 10, 101, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonClose.setFont(font)
        self.pushButtonClose.setAutoFillBackground(False)
        self.pushButtonClose.setStyleSheet("background-color: rgb(243, 79, 28);\n"
"color: rgb(255, 255, 255);")
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(0, 60, 701, 301))
        self.frame_2.setStyleSheet("background-color: rgb(231, 231, 231);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.textEditItemFilter = QtWidgets.QTextEdit(self.frame_2)
        self.textEditItemFilter.setGeometry(QtCore.QRect(10, 5, 680, 30))
        self.textEditItemFilter.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.textEditItemFilter.setObjectName("textEditItemFilter")
        self.tableWidget = QtWidgets.QTableWidget(self.frame_2)
        self.tableWidget.setGeometry(QtCore.QRect(10, 45, 681, 250))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.frame_3 = QtWidgets.QFrame(Dialog)
        self.frame_3.setGeometry(QtCore.QRect(0, 360, 701, 37))
        self.frame_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.pushButtonFirst = QtWidgets.QPushButton(self.frame_3)
        self.pushButtonFirst.setGeometry(QtCore.QRect(10, 0, 71, 37))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.pushButtonFirst.setFont(font)
        self.pushButtonFirst.setStyleSheet("color: rgb(0, 0, 0);")
        self.pushButtonFirst.setFlat(True)
        self.pushButtonFirst.setObjectName("pushButtonFirst")
        self.pushButtonPrevious = QtWidgets.QPushButton(self.frame_3)
        self.pushButtonPrevious.setGeometry(QtCore.QRect(90, 0, 71, 37))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.pushButtonPrevious.setFont(font)
        self.pushButtonPrevious.setStyleSheet("color: rgb(0, 0, 0);")
        self.pushButtonPrevious.setFlat(True)
        self.pushButtonPrevious.setObjectName("pushButtonPrevious")
        self.pushButtonNext = QtWidgets.QPushButton(self.frame_3)
        self.pushButtonNext.setGeometry(QtCore.QRect(230, 0, 71, 37))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.pushButtonNext.setFont(font)
        self.pushButtonNext.setStyleSheet("color: rgb(0, 0, 0);")
        self.pushButtonNext.setFlat(True)
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.pushButtonLast = QtWidgets.QPushButton(self.frame_3)
        self.pushButtonLast.setGeometry(QtCore.QRect(310, 0, 71, 37))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.pushButtonLast.setFont(font)
        self.pushButtonLast.setStyleSheet("color: rgb(0, 0, 0);")
        self.pushButtonLast.setFlat(True)
        self.pushButtonLast.setObjectName("pushButtonLast")
        self.textEditPageNumber = QtWidgets.QTextEdit(self.frame_3)
        self.textEditPageNumber.setGeometry(QtCore.QRect(170, 5, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.textEditPageNumber.setFont(font)
        self.textEditPageNumber.setStyleSheet("color: rgb(0, 0, 0);")
        self.textEditPageNumber.setReadOnly(True)
        self.textEditPageNumber.setObjectName("textEditPageNumber")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Search Item"))
        self.pushButton.setText(_translate("Dialog", "View"))
        self.pushButton_2.setText(_translate("Dialog", "Close"))
        self.pushButtonClose.setText(_translate("Dialog", "Esc-Close"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Barcode"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Item Description"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Price"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "On Hand Qty."))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "I"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "Pick"))
        self.pushButtonFirst.setText(_translate("Dialog", "First"))
        self.pushButtonPrevious.setText(_translate("Dialog", "Previous"))
        self.pushButtonNext.setText(_translate("Dialog", "Next"))
        self.pushButtonLast.setText(_translate("Dialog", "Last"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
