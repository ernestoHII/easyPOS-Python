import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5 import QtGui, QtWidgets

from dotenv import load_dotenv
from POSTouchQuickServiceList import Ui_Form
import POSTouchQuickServiceActivity  # Import the module

# Add the folder containing db_connection.py to the Python path
sys.path.append("C:/hii/POS-Python/src")

# Now you can import the db_connection module
from db_connection import establish_db_connection

# Load environment variables from the .env file
load_dotenv()

class POSTouchQuickServiceList(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)

        # Load data into the table widget
        self.load_data_into_table()

        # Connect the itemClicked signal to the open_selected method
        self.ui_form.tableWidgetOpenSalesList.itemClicked.connect(self.open_selected)

    def load_data_into_table(self):
        conn, cursor = establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to fetch only the last 4 rows from TrnSales table
                query = '''
                SELECT * FROM (
                    SELECT TOP 4 * FROM TrnSales ORDER BY SalesNumber DESC
                ) AS Last4Rows
                ORDER BY SalesNumber DESC
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Clear any existing data in the table widget
                self.ui_form.tableWidgetOpenSalesList.setRowCount(0)

                # Populate the table widget with data
                for row_index, row_data in enumerate(rows):
                    self.ui_form.tableWidgetOpenSalesList.insertRow(row_index)
                    for column_index, column_data in enumerate(row_data):
                        item = QTableWidgetItem(str(column_data))
                        self.ui_form.tableWidgetOpenSalesList.setItem(row_index, column_index, item)

            except Exception as e:
                print(f"Error: {str(e)}")

    def open_selected(self, item):
        selected_row = item.row()
        if selected_row >= 0:
            order_num = self.ui_form.tableWidgetOpenSalesList.item(selected_row, 3).text()

            # Create and show the destination GUI
            self.destination_gui = Ui_Form2()
            self.destination_gui.setWindowTitle(order_num)  # Set the window title
            self.destination_gui.show()

            
class Ui_Form2(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Destination GUI")

        # Set the GUI size to 700x500
        self.resize(700, 500)
        
        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Create and configure the QLabel for the title
        title_label = QLabel("POS Touch Quick Service Activity")
        title_label.setFont(QtGui.QFont("Segoe UI", 15, QtGui.QFont.Bold))

        # Create and configure the QPushButton for closing
        close_button = QPushButton("Esc - Close")
        close_button.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
        close_button.setStyleSheet("background-color: rgb(243, 79, 28); color: rgb(255, 255, 255);")

        # Add title label and close button to the layout
        layout.addWidget(title_label)
        layout.addWidget(close_button)

        # Set the layout for the central widget
        central_widget.setLayout(layout)

        # Set the central widget for the main window
        self.setCentralWidget(central_widget)

        # Create the remaining UI elements
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(0, 60, 701, 441))
        self.frame_2.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(10, 5, 681, 31))
        self.frame_3.setStyleSheet("background-color: rgb(127, 188, 0);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.pushButtonEditOrder = QtWidgets.QPushButton(self.frame_2)
        self.pushButtonEditOrder.setGeometry(QtCore.QRect(15, 50, 271, 251))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonEditOrder.setFont(font)
        self.pushButtonEditOrder.setStyleSheet("background-color: rgb(240, 80, 128); color: rgb(255, 255, 255);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/editOrder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonEditOrder.setIcon(icon)
        self.pushButtonEditOrder.setIconSize(QtCore.QSize(100, 100))
        self.pushButtonEditOrder.setObjectName("pushButtonEditOrder")

        # Add more QPushButton elements and their configurations here

        self.retranslateUi()

    def retranslateUi(self):
        # The retranslateUi method can remain as it is
        pass
                                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = POSTouchQuickServiceList()
    window.show()
    sys.exit(app.exec_())
