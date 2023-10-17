import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QSizePolicy, QTabWidget, QDesktopWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
from ItemList import ItemList
from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindow(QMainWindow):

    def __init__(self, tab_widget):
        super().__init__()
        self.initUI(tab_widget)  # Pass the tab_widget to initUI

    def create_item_list_tab(self, tab_name="Setup - Item List"):
        for index in range(self.tab_widget.count()):
            if self.tab_widget.tabText(index) == tab_name:
                self.tab_widget.setCurrentIndex(index)
                return

        if tab_name == "Setup - Item List":
            item_list_widget = ItemList()
            self.tab_widget.addTab(item_list_widget, tab_name)
            self.tab_widget.setCurrentWidget(item_list_widget)
        # If you have other tabs, you can add further conditions to handle them here.

    def initUI(self, tab_widget):

        self.tab_widget = tab_widget  # Store the tab widget
        self.setWindowTitle("POS - GPT")
        
        # Get the screen resolution
        screen_resolution = QDesktopWidget().screenGeometry(0)  # For the primary screen

        # Adjust geometry based on resolution
        if screen_resolution.width() == 1280 and screen_resolution.height() == 1024:
            self.setGeometry(0, 0, 1280, 956)
        elif screen_resolution.width() == 1366 and screen_resolution.height() == 768:
            self.setGeometry(0, 0, 1350, 700)
        else:
            # Default size, can be adjusted
            self.setGeometry(0, 0, 1366, 700)
                            
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        central_layout = QVBoxLayout(central_widget)
        grid_layout = QGridLayout()  # We create this layout here, but it isn't attached yet.

        # Initialize variables to keep track of the current page and number of items per page
        self.current_page = 1
        self.items_per_page = 20
        self.current_offset = (self.current_page - 1) * self.items_per_page

        # Create and add buttons to the grid layout
        button_info = [
            ("Item", "img/Item.png"), ("POS - F2", "img/POS.png"), ("Sales Report", "img/Reports.png"), ("POS Report", "img/Reports.png"),
            ("Discounting", "img/Discounting.png"), ("Cash In/Out", "img/Disbursement.png"), ("Remittance Report", "img/Reports.png"),
            ("Settings", "img/Settings.png"), ("Customer", "img/Customer.png"), ("Stock In", "img/Stock In.png"),
            ("Inventory Report", "img/Reports.png"), ("Utilities", "img/Utilities.png"), ("User", "img/User.png"), ("Stock Out", "img/Stock Out.png"),
            ("Stock Count", "img/Stock Count.png"), ("System Tables", "img/System Tables.png")]

        # Create a list of values for the buttons
        button_values = [
            "Setup - Item List", "POS - F2", "Sales Report", "POS Report", "Discounting", "Cash In/Out", "Remittance Report", "Settings", "Customer", "Stock In",
            "Inventory Report", "Utilities", "User", "Stock Out", "Stock Count", "System Tables"]

        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                if index < len(button_info):
                    button_text, icon_path = button_info[index]
                    button_value = button_values[index]  # Get the value for this button

                    container = QWidget()
                    layout = QVBoxLayout(container)
                    button = QPushButton()
                    size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    button.setSizePolicy(size_policy)

                    pixmap = QPixmap()
                    if not pixmap.load(icon_path):
                        print("Error loading image:", pixmap.isNull())
                    else:
                        pixmap = pixmap.scaledToHeight(122)  # Adjusted to be 5% smaller
                        icon = QIcon(pixmap)
                        button.setIcon(icon)
                        button.setIconSize(pixmap.size())

                    # Create a label for the button title (text)
                    title_label = QLabel(button_text)
                    title_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)  # Align text to the bottom center

                    # Make the text bold
                    font = QFont()
                    font.setBold(True)
                    title_label.setFont(font)

                    layout.addWidget(button)
                    layout.addWidget(title_label)

                    grid_layout.addWidget(container, row, col)

                    if button_value == "-Setup - Item List":
                        button.clicked.connect(self.create_item_list_tab)
                    else:
                        button.clicked.connect(lambda _, value=button_value: self.create_item_list_tab(value))

        self.rows = []  # Initialize rows as an empty list
        # Add the grid layout to the central layout
        central_layout.addLayout(grid_layout)
        self.create_item_list_tab()  # Create and add the Item List tab at the end

    def adjustForTaskbar(self, screen_index):
        screen = QDesktopWidget().screenGeometry(screen_index)
        desktop = QDesktopWidget().availableGeometry(screen_index)
        # taskbar_height = screen.height() - desktop.height()
        # self.move(screen.x(), screen.y() + taskbar_height)
        
class ItemList(QtWidgets.QWidget):  # Inherit from QWidget
    def __init__(self):
        super().__init__()  # Call the QWidget constructor
        self.setupUi()  # Set up the UI for this widget


    def setupUi(self):
        self.setObjectName("ItemListWidget")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 38, 32))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../Documents/GitHub/python-pos/img/Item.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 171, 41))
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
        self.frame_2 = QtWidgets.QFrame()
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

        # self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Window on Screen 2")
        self.setGeometry(0, 0, 1366, 768)
        self.adjustForTaskbar(1)


    def adjustForTaskbar(self, screen_index):
        screen = QDesktopWidget().screenGeometry(screen_index)
        desktop = QDesktopWidget().availableGeometry(screen_index)
        taskbar_height = screen.height() - desktop.height()
        self.move(screen.x(), screen.y() + taskbar_height)
        
def main():
    app = QApplication(sys.argv)

    if QDesktopWidget().screenCount() >= 2:
        tab_widget = QTabWidget()  # Create a QTabWidget object
        # Create the first window on the primary screen
        window1 = MainWindow(tab_widget)  # Pass the tab_widget to MainWindow
        window1.show()

        # Create the second window on the secondary screen
        window2 = SecondWindow()
        window2.show()

        sys.exit(app.exec_())
    else:
        print("Two screens are required to run this application.")

        
if __name__ == "__main__":
    main()


