import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTableWidgetItem, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from UserList import Ui_Form
import pyodbc
from UserDetailFunc import UserDetailFunc
from tkinter import *
from tkinter import messagebox
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class UserListFunc(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)

        # Embed the QTableWidget from Ui_Form into the main window
        self.grid_layout = QGridLayout(self.ui_form.frame)

        # Connect the textChanged signal of the search input to the search_data function
        self.ui_form.txtSearch.textChanged.connect(self.search_data)

        # Connect the clicked signals of the "Next" and "Previous" buttons to their respective methods
        self.ui_form.pushButtonNext.clicked.connect(self.load_next_data)
        self.ui_form.pushButtonPrevious.clicked.connect(self.load_previous_data)
        
        # Navigate to user details page
        self.ui_form.btnAdd.clicked.connect(self.btnAdd_clicked)

        # Initialize variables to keep track of the current page and number of items per page
        self.current_page = 1
        self.items_per_page = 20
        
        # hide column id
        self.ui_form.tblUserList.setColumnHidden(2, True)
        
        # Load data into the QTableWidget for the first page
        self.load_data(page=self.current_page)
        

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
                query = '''
                SELECT COUNT(*) as TotalRows
                FROM MstUser
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


    def load_data(self, page=1, custom_offset=None):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # Calculate the offset based on the current page or use the provided custom_offset
                offset = (page - 1) * self.items_per_page if custom_offset is None else custom_offset

                # Modify the SQL query based on filter options
                query = f'''
                SELECT Id, UserName, FullName, Designation, IsLocked FROM MstUser ORDER BY Id ASC OFFSET {offset} ROWS FETCH NEXT {self.items_per_page} ROWS ONLY
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Set the number of rows and columns for the QTableWidget
                self.ui_form.tblUserList.setRowCount(len(rows))
                self.ui_form.tblUserList.setColumnCount(7)  # Set the appropriate number of columns

                # Populate the QTableWidget with data
                col_array = [0, 1]
                for row_num, row_data in enumerate(rows):
                    for col_num, cell_value in enumerate(row_data[:7]):  # Use only the first 10 columns
                        for col in col_array:
                            if col == 0:
                                button = QPushButton(f"Edit")
                                button.setStyleSheet("background-color: #01A6F0; color: white;")
                                button.setFixedSize(70, 30)
                                widget = QWidget()
                                layout = QVBoxLayout()
                                layout.addWidget(button)
                                layout.setAlignment(Qt.AlignCenter)
                                widget.setLayout(layout)
                                self.ui_form.tblUserList.setCellWidget(row_num, col, widget)
                                button.clicked.connect(lambda _, row_data=row_data[0]: self.btnEdit_clicked(row_data))
                            else:
                                button = QPushButton(f"Delete")
                                button.setStyleSheet("background-color: #F34F1C; color: white;")
                                button.setFixedSize(70, 30)
                                widget = QWidget()
                                layout = QVBoxLayout()
                                layout.addWidget(button)
                                layout.setAlignment(Qt.AlignCenter)
                                widget.setLayout(layout)
                                self.ui_form.tblUserList.setCellWidget(row_num, col, widget)
                                button.clicked.connect(lambda _, row_data=row_data[0]: self.btnDelete_clicked(row_data))
                        item = QTableWidgetItem(str(cell_value))
                        self.ui_form.tblUserList.setRowHeight(row_num,50)
                        self.ui_form.tblUserList.setItem(row_num, col_num + 2, item)

                # Add checkboxes in columns 10 and 11 based on boolean values in the database
                for row_num, row_data in enumerate(rows):
                    for col_num in range(6, 7):
                        item = QTableWidgetItem()
                        item.setFlags(item.flags() | 0x0000100)  # Make it editable
                        # Check the value in columns 10 and 11 from the database
                        checkbox_value = bool(row_data[col_num - 2])  # Subtract 2 to align with the data index
                        item.setCheckState(2 if checkbox_value else 0)  # Set to checked (True) or unchecked (False)
                        self.ui_form.tblUserList.setItem(row_num, col_num, item)

                # Set each column width to fit the longest values from each row
                for col_num in range(7):
                    self.ui_form.tblUserList.resizeColumnToContents(col_num)

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
                search_text = self.ui_form.txtSearch.toPlainText().strip()

                # Modify the SQL query to filter based on the search_text and filter options
                query = f'''
                SELECT Id, UserName, FullName, Designation, IsLocked FROM MstUser WHERE FullName LIKE ?
                '''

                cursor.execute(query, ('%' + search_text + '%',))

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Set the number of rows and columns for the QTableWidget
                self.ui_form.tblUserList.setRowCount(len(rows))
                self.ui_form.tblUserList.setColumnCount(6)  # Set the appropriate number of columns

                # Populate the QTableWidget with data
                col_array = [0, 1]
                for row_num, row_data in enumerate(rows):
                    for col_num, cell_value in enumerate(row_data[:7]):  # Use only the first 10 columns
                        for col in col_array:
                            if col == 0:
                                button = QPushButton(f"Edit")
                                button.setStyleSheet("background-color: #01A6F0; color: white;")
                                button.setFixedSize(70, 30)
                                widget = QWidget()
                                layout = QVBoxLayout()
                                layout.addWidget(button)
                                layout.setAlignment(Qt.AlignCenter)
                                widget.setLayout(layout)
                                self.ui_form.tblUserList.setCellWidget(row_num, col, widget)
                                button.clicked.connect(lambda _, row_data=row_data[0]: self.btnEdit_clicked(row_data))
                            else:
                                button = QPushButton(f"Delete")
                                button.setStyleSheet("background-color: #F34F1C; color: white;")
                                button.setFixedSize(70, 30)
                                widget = QWidget()
                                layout = QVBoxLayout()
                                layout.addWidget(button)
                                layout.setAlignment(Qt.AlignCenter)
                                widget.setLayout(layout)
                                self.ui_form.tblUserList.setCellWidget(row_num, col, widget)
                                button.clicked.connect(lambda _, row_data=row_data[0]: self.btnDelete_clicked(row_data))
                        item = QTableWidgetItem(str(cell_value))
                        self.ui_form.tblUserList.setRowHeight(row_num,50)
                        self.ui_form.tblUserList.setItem(row_num, col_num + 2, item)

                # Add checkboxes in columns 10 and 11 based on boolean values in the database
                for row_num, row_data in enumerate(rows):
                    for col_num in range(5, 6):
                        item = QTableWidgetItem()
                        item.setFlags(item.flags() | 0x0000100)  # Make it editable
                        # Check the value in columns 10 and 11 from the database
                        checkbox_value = bool(row_data[col_num - 2])  # Subtract 2 to align with the data index
                        item.setCheckState(2 if checkbox_value else 0)  # Set to checked (True) or unchecked (False)
                        self.ui_form.tblUserList.setItem(row_num, col_num, item)

                # Set each column width to fit the longest values from each row
                for col_num in range(6):
                    self.ui_form.tblUserList.resizeColumnToContents(col_num)

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
        
        
    def btnAdd_clicked(self):
        self.destroy()
        self.ui_form = UserDetailFunc(0)
        self.ui_form.show()
        
        
    def btnEdit_clicked(self, cell_value):
        self.destroy()
        self.ui_form = UserDetailFunc(cell_value)
        self.ui_form.show()
        
        
    def btnDelete_clicked(self, cell_value):
        answer = messagebox.askquestion("Confirmation", "Delete record?") 
        
        if answer == "yes":
            conn, cursor = self.establish_db_connection()
            if conn and cursor:
                try:
                    # Modify the SQL query based on filter options
                    query = f'''
                    DELETE FROM MstUser WHERE Id = {cell_value}
                    '''
                    cursor.execute(query)
                    conn.commit()

                    # Close the cursor and connection
                    cursor.close()
                    conn.close()
                    self.load_data(page=self.current_page)

                except Exception as e:
                    print(f"Error: {str(e)}")
                    
                       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserListFunc()
    window.show()
    sys.exit(app.exec_())
