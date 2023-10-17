import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTableWidgetItem, QCheckBox, QLineEdit,QPushButton,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt,QDateTime
from CustomerList import Ui_Form
from CustomerDetailFunc import CustomerDetailCombinedApp
import pyodbc
from dotenv import load_dotenv
from tkinter import * 
from tkinter import messagebox 

# Load environment variables from the .env file
load_dotenv()

class CustomerListCombinedApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)

        # Embed the QTableWidget from Ui_Form into the main window
        self.grid_layout = QGridLayout(self.ui_form.frame)
        # hide column id
        self.ui_form.tableWidgetCustomer.setColumnHidden(2, True)
        # Connect the textChanged signal of the search input to the search_data function
        self.ui_form.textEditCustomerFilter.textChanged.connect(self.search_data)

        # Connect the clicked signals of the "Next" and "Previous" buttons to their respective methods
        self.ui_form.pushButtonNext.clicked.connect(self.load_next_data)
        self.ui_form.pushButtonPrevious.clicked.connect(self.load_previous_data)
        
        # Initialize variables to keep track of the current page and number of items per page
        self.current_page = 1
        self.items_per_page = 20
        self.ui_form.pushButtonAdd.clicked.connect(self.openDetail)
        # Load data into the QTableWidget for the first page
        self.load_data(page=self.current_page)
        # Close
        self.ui_form.pushButtonClose.clicked.connect(self.btnClose_clicked)
        
    def btnClose_clicked(self):
        self.destroy()    
    def openDetail(self):
        self.destroy()
        # Insert data into the 'easypos' table
        conn, cursor = self.establish_db_connection()
        self
        if conn and cursor:
            try:
                 # SQL query to fetch the last row's ItemCode
                query_customer = '''
                SELECT TOP 1 MI.CustomerCode
                FROM MstCustomer AS MI
                ORDER BY MI.CustomerCode DESC
                '''

                cursor.execute(query_customer)

                # Fetch the last row from the query result
                row_customer = cursor.fetchone()
                # Commit the transaction
                conn.commit()
                # Set the textEditItemCode widget's text using the data from the last row
                if row_customer:
                    last_customer_code = row_customer[0]
                    new_customer_code = int(last_customer_code) + 1  # Increment the last customer code
                    formatted_customer_code = str(new_customer_code).zfill(10)  # Pad with leading zeros to a width of 10
                    customer_code = formatted_customer_code
                else:
                    # If there are no rows in the table, start with customer code 1
                    customer_code = "0000000001"
             
                # SQL query to insert data into 'easypos' table
                query = '''
                INSERT INTO MstCustomer
                            (CustomerCode
                            ,Customer 
                            ,Address
                            ,ContactPerson
                            ,ContactNumber
                            ,CreditLimit
                            ,TermId
                            ,TIN
                            ,WithReward
                            ,RewardNumber
                            ,RewardConversion
                            ,AvailableReward
                            ,BusinessStyle
                            ,AccountId
                            ,EntryUserId
                            ,EntryDateTime
                            ,UpdateUserId
                            ,UpdateDateTime
                            ,IsLocked
                            ,DefaultPriceDescription
                            ,EmailAddress
                            ,Birthday
                            ,Age
                            ,Gender
                            )
                        VALUES
                            (?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?
                            ,?)
                '''
                # Execute the insert query with the provided values
                cursor.execute(query, (
                    customer_code,
                    "",
                    "",
                    "",
                    "",
                    0.00,
                    7,
                    "",
                    False,
                    "",
                    0.00,
                    0.00,
                    "",
                    64,
                    1,
                    QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"),
                    1,
                    QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"),
                    False,
                    "",
                    "",
                    QDateTime.currentDateTime().toString("yyyy-MM-dd"),
                    0,
                    "",
                ))
                # Commit the transaction
                conn.commit()
                query_get_customer_id = f'''
                    SELECT Id
                    FROM MstCustomer
                    WHERE CustomerCode = '{customer_code}'
                '''
                # Execute the query
                cursor.execute(query_get_customer_id)

                # Fetch the result
                result = cursor.fetchone()
                self.ui_form = CustomerDetailCombinedApp(result[0])
                self.ui_form.show()
                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Inform the user that the data has been inserted successfully
                print("Data updated into table successfully.")
               
            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            print("Database connection error.")
                 
    def load_last_data(self):
        try:
            # Get the total number of rows in the table
            total_rows = self.get_total_row_count()

            if total_rows > 0:
                # Calculate the offset to fetch the last 20 rows
                offset = max(total_rows - self.items_per_page, 0)

                # Load the last 20 data entries
                self.load_data(page=1, custom_offset=offset)

        except Exception as e:
            print(f"Error: {str(e)}")

    def get_total_row_count(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # Execute SQL query to count the total number of rows in the table
                query = f'''
                SELECT COUNT(*) as TotalRows
                FROM MstCustomer
                '''

                cursor.execute(query)

                # Fetch the result of the count query
                result = cursor.fetchone()

                if result:
                    total_rows = result.TotalRows
                    return total_rows

            except Exception as e:
                print(f"Error: {str(e)}")
            finally:
                # Close the cursor and connection
                cursor.close()
                conn.close()

        return 0  # Return 0 in case of an error or no rows found

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

    def click_edit(self, customer_id):
        self.destroy()
        self.ui_form = CustomerDetailCombinedApp(customer_id)
        self.ui_form.show()
    def click_delete(self, customer_id):
        conn, cursor = self.establish_db_connection()
        if conn and cursor:
            try:
                answer = messagebox.askquestion("EasyPOS","Are you sure you want to delete this customer?")
                if answer == 'yes':
                    # Modify the SQL query based on filter options
                    query = f'''
                    DELETE FROM MstCustomer WHERE Id = {customer_id}
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
        
    def load_data(self, page=1, custom_offset=None):
        conn, cursor = self.establish_db_connection()
        if conn and cursor:
            try:
                # Calculate the offset based on the current page or use the provided custom_offset
                offset = (page - 1) * self.items_per_page if custom_offset is None else custom_offset

                # Modify the SQL query based on filter options
                query = f'''
                SELECT Id,CustomerCode, Customer, ContactNumber,Address,AvailableReward,IsLocked FROM MstCustomer ORDER BY Id ASC OFFSET {offset} ROWS FETCH NEXT {self.items_per_page} ROWS ONLY
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Set the number of rows and columns for the QTableWidget
                self.ui_form.tableWidgetCustomer.setRowCount(len(rows))
                self.ui_form.tableWidgetCustomer.setColumnCount(9)  # Set the appropriate number of columns
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
                                
                                self.ui_form.tableWidgetCustomer.setCellWidget(row_num, col, widget)
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
                                self.ui_form.tableWidgetCustomer.setCellWidget(row_num, col, widget)
                                button.clicked.connect(lambda _, row_data=row_data[0]: self.click_delete(row_data))
                            item = QTableWidgetItem(str(cell_value))
                            self.ui_form.tableWidgetCustomer.setRowHeight(row_num,50)
                            self.ui_form.tableWidgetCustomer.setItem(row_num, col_num + 2, item)

                # Add checkboxes in columns 10 and 11 based on boolean values in the database
                for row_num, row_data in enumerate(rows):
                    for col_num in range(8, 9):
                        item = QTableWidgetItem()
                        item.setFlags(item.flags() | 0x0000100)  # Make it editable
                        # Check the value in columns 10 and 11 from the database
                        checkbox_value = bool(row_data[col_num - 2])  # Subtract 2 to align with the data index
                        item.setCheckState(2 if checkbox_value else 0)  # Set to checked (True) or unchecked (False)
                        self.ui_form.tableWidgetCustomer.setItem(row_num, col_num, item)

                # Set each column width to fit the longest values from each row
                for col_num in range(9):
                    self.ui_form.tableWidgetCustomer.resizeColumnToContents(col_num)

                # Check if there are more pages to load
                has_more_pages = len(rows) == self.items_per_page
                self.ui_form.pushButtonNext.setEnabled(has_more_pages)

                # Check if there are previous pages to load
                self.ui_form.pushButtonPrevious.setEnabled(page > 1)

                # Close the cursor and connection
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error: {str(e)}")

    def search_data(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # Get the search text from the input box
                search_text = self.ui_form.textEditCustomerFilter.toPlainText().strip()

                # # Get the selected filter options
                # is_locked_filter = self.ui_form.comboBoxIsLockedFilter.currentText()
                # is_inventory_filter = self.ui_form.comboBoxIsInventoryFilter.currentText()

                # Modify the SQL query to filter based on the search_text and filter options
                query = f'''
                SELECT CustomerCode, Customer, ContactNumber,Address,AvailableReward,IsLocked FROM MstCustomer WHERE Customer LIKE ?
                '''

                cursor.execute(query, ('%' + search_text + '%',))

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Set the number of rows and columns for the QTableWidget
                self.ui_form.tableWidgetCustomer.setRowCount(len(rows))
                self.ui_form.tableWidgetCustomer.setColumnCount(8)  # Set the appropriate number of columns

                # Populate the QTableWidget with data
                for row_num, row_data in enumerate(rows):
                    for col_num, cell_value in enumerate(row_data[:8]):  # Use only the first 10 columns
                        item = QTableWidgetItem(str(cell_value))
                        self.ui_form.tableWidgetCustomer.setItem(row_num, col_num + 2, item)

                # Add checkboxes in columns 10 and 11 based on boolean values in the database
                for row_num, row_data in enumerate(rows):
                    for col_num in range(7, 8):
                        item = QTableWidgetItem()
                        item.setFlags(item.flags() | 0x0000100)  # Make it editable
                        # Check the value in columns 10 and 11 from the database
                        checkbox_value = bool(row_data[col_num - 2])  # Subtract 2 to align with the data index
                        item.setCheckState(2 if checkbox_value else 0)  # Set to checked (True) or unchecked (False)
                        self.ui_form.tableWidgetCustomer.setItem(row_num, col_num, item)

                # Set each column width to fit the longest values from each row
                for col_num in range(8):
                    self.ui_form.tableWidgetCustomer.resizeColumnToContents(col_num)

                # Close the cursor and connection
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error: {str(e)}")

    def load_next_data(self):
        try:
            # Increment the current page
            self.current_page += 1

            # Load data for the next page
            self.load_data(page=self.current_page)

        except Exception as e:
            print(f"Error: {str(e)}")

    def load_previous_data(self):
        try:
            # Decrement the current page
            if self.current_page > 1:
                self.current_page -= 1

                # Load data for the previous page
                self.load_data(page=self.current_page)

        except Exception as e:
            print(f"Error: {str(e)}")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomerListCombinedApp()
    window.show()
    sys.exit(app.exec_())
