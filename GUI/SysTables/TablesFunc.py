import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTableWidgetItem, QCheckBox, QLineEdit,QPushButton,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt,QDateTime
from Tables import Ui_Form
from AccountDetail.AccountDetailFunc import AccountDetailCombinedApp
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

        # Embed the QTableWidget from Ui_Form into the main window
        self.grid_layout = QGridLayout(self.ui_form.frame)
        # hide column id
        self.ui_form.tableWidgetAccount.setColumnHidden(2, True)
        self.ui_form.tableWidgetPayType.setColumnHidden(2, True)
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
                if self.ui_form.tabWidget.currentIndex() == 0: 
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT Id, Code, Account, AccountType FROM MstAccount ORDER BY Id ASC OFFSET {offset} ROWS FETCH NEXT {self.items_per_page} ROWS ONLY
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
                elif self.ui_form.tabWidget.currentIndex() == 1:
                    # Modify the SQL query based on filter options
                    query = f'''
                    SELECT MstPayType.Id, MstPayType.PAYTYPECODE, MstAccount.Account, MstPayType.PayType
                    FROM MstPayType INNER JOIN
                         MstAccount ON MstPayType.AccountId = MstAccount.Id ORDER BY Id ASC OFFSET {offset} ROWS FETCH NEXT {self.items_per_page} ROWS ONLY
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
                # Close the cursor and connection
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
                self.load_account_data(page=self.current_page)

        except Exception as e:
            print(f"Error: {str(e)}")

    def load_previous_data(self):
        try:
            if self.ui_form.tabWidget.currentIndex() == 0:
                # Decrement the current page
                if self.current_page > 1:
                    self.current_page -= 1

                    # Load data for the previous page
                    self.load_account_data(page=self.current_page)

        except Exception as e:
            print(f"Error: {str(e)}")
            
    def btnClose_clicked(self):
        self.destroy()    
    
    def btnAdd_clicked(self):
        if self.ui_form.tabWidget.currentIndex() == 0:
            self.ui_form = AccountDetailCombinedApp(0)
            self.ui_form.show()
            self.destroy() 
    
    def click_edit(self, tab_id):
        if self.ui_form.tabWidget.currentIndex() == 0: 
            self.ui_form = AccountDetailCombinedApp(tab_id)
            self.ui_form.show()
            self.destroy() 
        
    def click_delete(self, tab_id):
        print(self.ui_form.tabWidget.currentIndex())
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
            except Exception as e:
                print(f"Error: {str(e)}")
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableCombinedApp()
    window.show()
    sys.exit(app.exec_())    