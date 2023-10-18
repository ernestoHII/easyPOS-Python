import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTableWidgetItem, QCheckBox, QLineEdit,QPushButton,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt,QDateTime
from Tables import Ui_Form
from AccountDetail.AccountDetailFunc import AccountDetailCombinedApp
from PayTypeDetail.PayTypeDetailFunc import PayTypeDetailCombinedApp
from TaxDetail.TaxDetailFunc import TaxDetailCombinedApp
from UnitDetail.UnitDetailFunc import UnitDetailCombinedApp
from PeriodDetail.PeriodDetailFunc import PeriodDetailCombinedApp
from TerminalDetail.TerminalDetailFunc import TerminalDetailCombinedApp
from SupplierDetail.SupplierDetailFunc import SupplierDetailCombinedApp
from FormDetail.FormDetailFunc import FormDetailCombinedApp
from ItemCategoryDetail.ItemCategoryDetailFunc import ItemCategoryDetailCombinedApp
from CardTypeDetail.CardTypeDetailFunc import CardTypeDetailCombinedApp
# from VoidReasonDetail.VoidReasonDetailFunc import VoidReasonDetailCombineApp
from BankDetail.BankDetailFunc import BankDetailCombinedApp

import pyodbc
from dotenv import load_dotenv
from tkinter import * 
from tkinter import messagebox 

# Load environment variables from the .env file
load_dotenv()

class TableCombinedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        #Globalized variable

        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)
        self.ui_form.tabWidget.setCurrentIndex(0)
        # Embed the QTableWidget from Ui_Form into the main window
        self.grid_layout = QGridLayout(self.ui_form.frame)
        # hide column id
        self.ui_form.tableWidgetAccount.setColumnHidden(2, True)
        self.ui_form.tableWidgetPayType.setColumnHidden(2, True)
        self.ui_form.tableWidgetTax.setColumnHidden(2, True)
        self.ui_form.tableWidgetUnit.setColumnHidden(2, True)
        self.ui_form.tableWidgetPeriod.setColumnHidden(2, True)
        self.ui_form.tableWidgetTerminal.setColumnHidden(2, True)
        self.ui_form.tableWidgetSupplier.setColumnHidden(2, True)
        self.ui_form.tableWidgetForm.setColumnHidden(2, True)
        self.ui_form.tableWidgetCategory.setColumnHidden(2, True)
        self.ui_form.tableWidgetCardType.setColumnHidden(2, True)
        self.ui_form.tableWidgetBank.setColumnHidden(2, True)
        # Initialize variables to keep track of the current page and number of items per page
        self.current_page = 1
        self.items_per_page = 20
        # Load data into the QTableWidget for the first page
        self.load_data(page=self.current_page)
        # Close
        self.ui_form.pushButtonClose.clicked.connect(self.btnClose_clicked)
        # Search Data Function
        self.ui_form.textEditAccountFilter.textChanged.connect(self.search_data)
        #tabWidgetIndexChange
        self.ui_form.tabWidget.currentChanged.connect(self.load_data)
        # Connect the clicked signals of the "Next" and "Previous" buttons to their respective methods
        self.ui_form.pushButtonAccountNext.clicked.connect(self.load_next_data)
        self.ui_form.pushButtonAccountPrevious.clicked.connect(self.load_previous_data)
        self.ui_form.pushButtonAdd.clicked.connect(self.btnAdd_clicked)
        
    def establish_db_connection(self):
        try:
            # Get database credentials from environment variables
            db_server = os.getenv("DB_SERVER")
            db_database = os.getenv("DB_DATABASE")
            db_username = os.getenv("DB_USERNAME")
            db_password = os.getenv("DB_PASSWORD")

            # Establish a connection to the database
            connection_string = f'DRIVER={{SQL Server}};SERVER={db_server};DATABASE={db_database};UID={db_username};PWD={db_password}'
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            return conn, cursor

        except Exception as e:
            print(f"Error: {str(e)}")
            return None, None
            
    def load_data(self, page=1, custom_offset=None):
        conn, cursor = self.establish_db_connection()
        if conn and cursor:
            try:
                # Calculate the offset based on the current page or use the provided custom_offset
                offset = (page - 1) * self.items_per_page if custom_offset is None else custom_offset
                #To load account data
                if self.ui_form.tabWidget.currentIndex() == 0: 
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT Id, Code, Account, AccountType FROM MstAccount ORDER BY Id
                    '''

                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetAccount.setRowCount(len(rows))
                    self.ui_form.tableWidgetAccount.setColumnCount(6)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:6]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetAccount.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetAccount.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetAccount.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetAccount.setItem(row_num, col_num + 2, item)


                    # Set each column width to fit the longest values from each row
                    for col_num in range(6):
                        self.ui_form.tableWidgetAccount.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonAccountNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonAccountPrevious.setEnabled(page > 1)
                    
                #To load pay type data
                elif self.ui_form.tabWidget.currentIndex() == 1:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT MstPayType.Id, MstPayType.PAYTYPECODE, MstAccount.Account, MstPayType.PayType
                    FROM MstPayType INNER JOIN
                         MstAccount ON MstPayType.AccountId = MstAccount.Id ORDER BY MstPayType.Id 
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetPayType.setRowCount(len(rows))
                    self.ui_form.tableWidgetPayType.setColumnCount(6)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:6]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetPayType.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetPayType.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetPayType.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetPayType.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(6):
                        self.ui_form.tableWidgetPayType.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonPayTypeNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonPayTypePrevious.setEnabled(page > 1) 
                    
                #To load tax data     
                elif self.ui_form.tabWidget.currentIndex() == 2:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT MstTax.Id, MstTax.Code, MstTax.Tax, MstTax.Rate, MstAccount.Account
                    FROM MstTax INNER JOIN
                         MstAccount ON MstTax.AccountId = MstAccount.Id
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetTax.setRowCount(len(rows))
                    self.ui_form.tableWidgetTax.setColumnCount(7)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:7]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetTax.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetTax.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetTax.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetTax.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(7):
                        self.ui_form.tableWidgetTax.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonTaxNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonTaxPrevious.setEnabled(page > 1) 
                
                #To load unit data     
                elif self.ui_form.tabWidget.currentIndex() == 3:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT Id, Unit
                    FROM MstUnit
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetUnit.setRowCount(len(rows))
                    self.ui_form.tableWidgetUnit.setColumnCount(4)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:4]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetUnit.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetUnit.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetUnit.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetUnit.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(4):
                        self.ui_form.tableWidgetUnit.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonUnitNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonUnitPrevious.setEnabled(page > 1)
                    
                #To load period data     
                elif self.ui_form.tabWidget.currentIndex() == 4:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT Id, Period
                    FROM MstPeriod
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetPeriod.setRowCount(len(rows))
                    self.ui_form.tableWidgetPeriod.setColumnCount(4)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:4]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetPeriod.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetPeriod.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetPeriod.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetPeriod.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(4):
                        self.ui_form.tableWidgetPeriod.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonPeriodNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonPeriodPrevious.setEnabled(page > 1)
                
                #To load terminal data     
                elif self.ui_form.tabWidget.currentIndex() == 5:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT Id, Terminal
                    FROM MstTerminal
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetTerminal.setRowCount(len(rows))
                    self.ui_form.tableWidgetTerminal.setColumnCount(4)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:4]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetTerminal.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetTerminal.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetTerminal.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetTerminal.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(4):
                        self.ui_form.tableWidgetTerminal.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonTerminalNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonTerminalPrevious.setEnabled(page > 1)

                #To load supplier data     
                elif self.ui_form.tabWidget.currentIndex() == 6:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT Id, Supplier, Address, TelephoneNumber, CellphoneNumber, TIN, IsLocked
                    FROM MstSupplier
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetSupplier.setRowCount(len(rows))
                    self.ui_form.tableWidgetSupplier.setColumnCount(9)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:9]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetSupplier.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetSupplier.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetSupplier.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetSupplier.setItem(row_num, col_num + 2, item)
                                
                    # Add checkboxes in columns 10 and 11 based on boolean values in the database
                    for row_num, row_data in enumerate(rows):
                        for col_num in range(8, 9):
                            item = QTableWidgetItem()
                            item.setFlags(item.flags() | 0x0000100)  # Make it editable
                            # Check the value in columns 10 and 11 from the database
                            checkbox_value = bool(row_data[col_num - 2])  # Subtract 2 to align with the data index
                            item.setCheckState(2 if checkbox_value else 0)  # Set to checked (True) or unchecked (False)
                            self.ui_form.tableWidgetSupplier.setItem(row_num, col_num, item)
                            
                    # Set each column width to fit the longest values from each row
                    for col_num in range(9):
                        self.ui_form.tableWidgetSupplier.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonSupplierNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonSupplierPrevious.setEnabled(page > 1)
                    
                #To load form data     
                elif self.ui_form.tabWidget.currentIndex() == 7:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT Id, Form
                    FROM SysForm
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetForm.setRowCount(len(rows))
                    self.ui_form.tableWidgetForm.setColumnCount(4)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:4]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetForm.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetForm.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetForm.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetForm.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(4):
                        self.ui_form.tableWidgetForm.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonFormNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonFormPrevious.setEnabled(page > 1)
                    
                #To load item category data
                elif self.ui_form.tabWidget.currentIndex() == 8:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT Id, Category
                    FROM MstItemCategory
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetCategory.setRowCount(len(rows))
                    self.ui_form.tableWidgetCategory.setColumnCount(4)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:4]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetCategory.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetCategory.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetCategory.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetCategory.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(4):
                        self.ui_form.tableWidgetCategory.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonCategoryNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonCategoryPrevious.setEnabled(page > 1)
                    
                #To load card type data
                elif self.ui_form.tabWidget.currentIndex() == 9:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT MstCardType.Id, MstPayType.PayType, MstCardType.CardType
                    FROM MstCardType INNER JOIN
                         MstPayType ON MstCardType.PaytypeId = MstPayType.Id
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetCardType.setRowCount(len(rows))
                    self.ui_form.tableWidgetCardType.setColumnCount(5)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:5]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetCardType.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetCardType.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetCardType.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetCardType.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(5):
                        self.ui_form.tableWidgetCardType.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonCardTypeNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonCardTypePrevious.setEnabled(page > 1)
                #To load bank data    
                elif self.ui_form.tabWidget.currentIndex() == 10:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT Id, Bank
                    FROM MstBank
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetBank.setRowCount(len(rows))
                    self.ui_form.tableWidgetBank.setColumnCount(4)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:4]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetBank.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetBank.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetBank.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetBank.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(4):
                        self.ui_form.tableWidgetBank.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonBankNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonBankPrevious.setEnabled(page > 1)
                    
                #To load currency data    
                elif self.ui_form.tabWidget.currentIndex() == 11:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT Id, CurrencyName
                    FROM MstCurrency
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetCurrency.setRowCount(len(rows))
                    self.ui_form.tableWidgetCurrency.setColumnCount(4)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:4]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetCurrency.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetCurrency.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetCurrency.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetCurrency.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(4):
                        self.ui_form.tableWidgetCurrency.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonCurrencyNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonCurrencyPrevious.setEnabled(page > 1)
                    
                #To load void reason data    
                else:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT Id, Reason, Category
                    FROM MstVoidReason
                    '''
                    cursor.execute(query)

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()
                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetVoidReason.setRowCount(len(rows))
                    self.ui_form.tableWidgetVoidReason.setColumnCount(5)  # Set the appropriate number of columns
                    col_array = [0, 1]
                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:4]):  # Use only the first 10 columns
                            for col in col_array:
                                if col == 0:
                                    button = QPushButton(f"Edit")
                                    button.setStyleSheet("background-color: #01A6F0; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    
                                    self.ui_form.tableWidgetVoidReason.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_edit(row_data))
                                else:
                                    button = QPushButton(f"Delete")
                                    button.setStyleSheet("background-color: #F34F1C; color: white;")
                                    button.setFixedSize(70, 30)  # Set the size to 30x32
                                    widget = QWidget()
                                    layout = QVBoxLayout()
                                    layout.addWidget(button)
                                    layout.setAlignment(Qt.AlignCenter)
                                    widget.setLayout(layout)
                                    self.ui_form.tableWidgetVoidReason.setCellWidget(row_num, col, widget)
                                    button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                                item = QTableWidgetItem(str(cell_value))
                                self.ui_form.tableWidgetVoidReason.setRowHeight(row_num,50)
                                self.ui_form.tableWidgetVoidReason.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(5):
                        self.ui_form.tableWidgetVoidReason.resizeColumnToContents(col_num)

                    # Check if there are more pages to load
                    has_more_pages = len(rows) == self.items_per_page
                    self.ui_form.pushButtonVoidReasonNext.setEnabled(has_more_pages)

                    # Check if there are previous pages to load
                    self.ui_form.pushButtonVoidReasonPrevious.setEnabled(page > 1)
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error: {str(e)}")
                                
    def search_data(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                if self.ui_form.tabWidget.currentIndex() == 0:
                    # Get the search text from the input box
                    search_text = self.ui_form.textEditAccountFilter.toPlainText().strip()

                    # Modify the SQL query to filter based on the search_text and filter options
                    query = f'''
                    SELECT Id, Code, Account, IsLocked FROM MstAccount WHERE Account LIKE ?
                    '''
                    cursor.execute(query, ('%' + search_text + '%',))

                    # Fetch all rows from the query result
                    rows = cursor.fetchall()

                    # Set the number of rows and columns for the QTableWidget
                    self.ui_form.tableWidgetAccount.setRowCount(len(rows))
                    self.ui_form.tableWidgetAccount.setColumnCount(6)  # Set the appropriate number of columns

                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:6]):  # Use only the first 10 columns
                            item = QTableWidgetItem(str(cell_value))
                            self.ui_form.tableWidgetAccount.setItem(row_num, col_num + 2, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(6):
                        self.ui_form.tableWidgetAccount.resizeColumnToContents(col_num)

                # Close the cursor and connection
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error: {str(e)}")    
                
    def load_next_data(self):
        try:
            if self.ui_form.tabWidget.currentIndex() == 0:
                # Increment the current page
                self.current_page += 1

                # Load data for the next page
                self.load_data(page=self.current_page)

        except Exception as e:
            print(f"Error: {str(e)}")

    def load_previous_data(self):
        try:
            if self.ui_form.tabWidget.currentIndex() == 0:
                # Decrement the current page
                if self.current_page > 1:
                    self.current_page -= 1

                    # Load data for the previous page
                    self.load_data(page=self.current_page)

        except Exception as e:
            print(f"Error: {str(e)}")
            
    def btnClose_clicked(self):
        self.destroy()    
    
    def btnAdd_clicked(self):
        if self.ui_form.tabWidget.currentIndex() == 0:
            self.ui_form = AccountDetailCombinedApp(0)
            self.ui_form.show()
            self.destroy() 
        elif self.ui_form.tabWidget.currentIndex() == 1:
             self.ui_form = PayTypeDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 2:
             self.ui_form = TaxDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 3:
             self.ui_form = UnitDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 4:
             self.ui_form = PeriodDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 5:
             self.ui_form = TerminalDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 6:
             self.ui_form = SupplierDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 7:
             self.ui_form = FormDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 8:
             self.ui_form = ItemCategoryDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 9:
             self.ui_form = CardTypeDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 10:
             self.ui_form = BankDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 7:
             self.ui_form = FormDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 8:
             self.ui_form = ItemCategoryDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 9:
             self.ui_form = CardTypeDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 10:
             self.ui_form = BankDetailCombinedApp(0)
             self.ui_form.show()
             self.destroy()   
        # else:
            #  self.ui_form = VoidReasonDetailCombinedApp(0)
            #  self.ui_form.show()
            #  self.destroy()
                            
    def click_edit(self, tab_id):
        if self.ui_form.tabWidget.currentIndex() == 0: 
            self.ui_form = AccountDetailCombinedApp(tab_id)
            self.ui_form.show()
            self.destroy() 
        elif self.ui_form.tabWidget.currentIndex() == 1: 
             self.ui_form = PayTypeDetailCombinedApp(tab_id)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 2:
             self.ui_form = TaxDetailCombinedApp(tab_id)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 3:
             self.ui_form = UnitDetailCombinedApp(tab_id)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 4:
             self.ui_form = PeriodDetailCombinedApp(tab_id)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 5:
             self.ui_form = TerminalDetailCombinedApp(tab_id)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 6:
             self.ui_form = SupplierDetailCombinedApp(tab_id)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 7:
             self.ui_form = FormDetailCombinedApp(tab_id)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 8:
             self.ui_form = ItemCategoryDetailCombinedApp(tab_id)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 9:
             self.ui_form = CardTypeDetailCombinedApp(tab_id)
             self.ui_form.show()
             self.destroy()
        elif self.ui_form.tabWidget.currentIndex() == 10:
             self.ui_form = BankDetailCombinedApp(tab_id)
             self.ui_form.show()
             self.destroy()
        # elif self.ui_form.tabWidget.currentIndex() == 11:
        #      self.ui_form = CurrencyDetailCombinedApp(tab_id)
        #      self.ui_form.show()
        #      self.destroy()
        # else:
        #     self.ui_form = VoidReasonDetailCombinedApp(tab_id)
        #     self.ui_form.show()
        #     self.destroy()
             
    def click_delete(self, tab_id):
        conn, cursor = self.establish_db_connection()
        if conn and cursor:
            try:
                if self.ui_form.tabWidget.currentIndex() == 0: 
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this account?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM MstAccount WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)
                elif self.ui_form.tabWidget.currentIndex() == 1:
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this pay type?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM MstPayType WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)
                elif self.ui_form.tabWidget.currentIndex() == 2:
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this tax?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM MstTax WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)
                elif self.ui_form.tabWidget.currentIndex() == 3:
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this unit?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM MstUnit WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)
                elif self.ui_form.tabWidget.currentIndex() == 4:
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this period?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM MstPeriod WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)
                elif self.ui_form.tabWidget.currentIndex() == 5:
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this terminal?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM MstTerminal WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)
                elif self.ui_form.tabWidget.currentIndex() == 6:
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this supplier?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM MstSupplier WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)
                elif self.ui_form.tabWidget.currentIndex() == 7:
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this form?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM SysForm WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)
                elif self.ui_form.tabWidget.currentIndex() == 8:
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this item category?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM MstItemCategory WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)
                elif self.ui_form.tabWidget.currentIndex() == 9:
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this card type?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM MstCardType WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)
                elif self.ui_form.tabWidget.currentIndex() == 10:
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this bank?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM MstBank WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)
                elif self.ui_form.tabWidget.currentIndex() == 11:
                    answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this currency?")
                    if answer == 'yes':
                        # Modify the SQL query based on filter options
                        query = f'''
                        DELETE FROM MstCurrency WHERE Id = {tab_id}
                        '''
                        cursor.execute(query)
                        conn.commit()

                        # Close the cursor and connection
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                        self.load_data(page=self.current_page)    
                # else:
                    # answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this VoidReason?")
                    # if answer == 'yes':
                    #     # Modify the SQL query based on filter options
                    #     query = f'''
                    #     DELETE FROM MstVoidReason WHERE Id = {tab_id}
                    #     '''
                    #     cursor.execute(query)
                    #     conn.commit()

                    #     # Close the cursor and connection
                    #     cursor.close()
                    #     conn.close()
                    #     messagebox.showinfo("EasyPOS", "Deleted successfully.")                    
                    #     self.load_data(page=self.current_page)
                    
            except Exception as e:
                print(f"Error: {str(e)}")
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableCombinedApp()
    window.show()
    sys.exit(app.exec_())