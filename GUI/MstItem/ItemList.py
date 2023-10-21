from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FormList(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1300, 500)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1366, 60))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 10, 38, 32))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../Documents/GitHub/python-pos/img/Item.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(60, 10, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setObjectName("label_2")
        self.pushButtonAdd = QtWidgets.QPushButton(self.frame)
        self.pushButtonAdd.setGeometry(QtCore.QRect(1200, 10, 70, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonAdd.setFont(font)
        self.pushButtonAdd.setAutoFillBackground(False)
        self.pushButtonAdd.setStyleSheet("background-color: rgb(240, 80, 128);\n"
"color: rgb(255, 255, 255);")
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.pushButtonClose = QtWidgets.QPushButton(self.frame)
        self.pushButtonClose.setGeometry(QtCore.QRect(1280, 10, 70, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonClose.setFont(font)
        self.pushButtonClose.setStyleSheet("background-color: rgb(243, 79, 28);\n"
"color: rgb(255, 255, 255);")
        self.pushButtonClose.setFlat(False)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(0, 60, 1361, 711))
        self.frame_2.setStyleSheet("background-color: rgb(240,240,240);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.textEditItemFilter = QtWidgets.QTextEdit(self.frame_2)
        self.textEditItemFilter.setGeometry(QtCore.QRect(5, 5, 1041, 31))
        self.textEditItemFilter.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.textEditItemFilter.setObjectName("textEditItemFilter")
        self.comboBoxIsInventoryFilter = QtWidgets.QComboBox(self.frame_2)
        self.comboBoxIsInventoryFilter.setGeometry(QtCore.QRect(1060, 5, 151, 31))
        self.comboBoxIsInventoryFilter.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.comboBoxIsInventoryFilter.setObjectName("comboBoxIsInventoryFilter")
        self.comboBoxIsLockedFilter = QtWidgets.QComboBox(self.frame_2)
        self.comboBoxIsLockedFilter.setGeometry(QtCore.QRect(1210, 5, 151, 31))
        self.comboBoxIsLockedFilter.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.comboBoxIsLockedFilter.setObjectName("comboBoxIsLockedFilter")
        self.tableWidget = QtWidgets.QTableWidget(self.frame_2)
        self.tableWidget.setGeometry(QtCore.QRect(0, 40, 1361, 631))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(12)
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
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(0, 670, 1361, 37))
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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def load_table_data(self, data):
        # 'data' should be a list or data source containing the data to be loaded
        table = self.tableWidget
        table.setRowCount(len(data))
        table.setColumnCount(len(data[0]))  # Assuming all rows have the same number of columns

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(cell_data))
                table.setItem(row_idx, col_idx, item)
                    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Item List"))
        self.pushButtonAdd.setText(_translate("Form", "Add"))
        self.pushButtonClose.setText(_translate("Form", "Close"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Item Code"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Barcode"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Item Description"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Unit"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Category"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Default Supplier"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Price"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Form", "Qty."))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("Form", "I"))
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText(_translate("Form", "L"))
        self.pushButtonFirst.setText(_translate("Form", "First"))
        self.pushButtonPrevious.setText(_translate("Form", "Previous"))
        self.pushButtonNext.setText(_translate("Form", "Next"))
        self.pushButtonLast.setText(_translate("Form", "Last"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_FormList()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
