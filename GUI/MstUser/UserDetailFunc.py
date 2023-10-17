import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QDateTime
from UserDetail import Ui_Form
import pyodbc
from subprocess import call
from tkinter import *
from tkinter import messagebox
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class UserDetailFunc(QMainWindow):
    def __init__(self, userId):
        super().__init__()
        
        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)
        
        self.ui_form.btnLock.clicked.connect(self.btnLock_clicked)
        
        # Close
        self.ui_form.btnClose.clicked.connect(self.btnClose_clicked)
        
        # Load user details
        self.userId = userId
        self.load_user_detail()
        
        # Embed the QTableWidget from Ui_Form into the main window
        # self.grid_layout = QGridLayout(self.ui_form.frame)
        
        # # Connect the textChanged signal of the search input to the search_data function
        # self.ui_form.textEdit_2.textChanged.connect(self.search_data)
        
        # # Connect the clicked signals of the "Next" and "Previous" buttons to their respective methods
        # self.ui_form.pushButtonNext.clicked.connect(self.load_next_data)
        # self.ui_form.pushButtonPrevious.clicked.connect(self.load_previous_data)
        
        # # Initialize variables to keep track of the current page and number of items per page
        # self.current_page = 1
        # self.items_per_page = 20
        
        # # Load data into the QTableWidget for the first page
        # self.load_data(page=self.current_page)
        
        # try:
        #     # Get the total number of rows in the table
        #     total_rows = self.get_total_row_count()
        
        #     if total_rows > 0:
        #         # Calculate the offset to fetch the last 20 rows
        #         offset = max(total_rows - self.items_per_page, 0)
        
        #         # Load the last 20 data entries
        #         self.load_data(page=1, custom_offset=offset)
        
        # except Exception as e:
        #     print(f"Error: {str(e)}")
        
        # conn, cursor = self.establish_db_connection()
        
        # if conn and cursor:
        #     try:
        #         # Execute SQL query to count the total number of rows in the table
        #         query = '''
        #         SELECT COUNT(*) as TotalRows
        #         FROM MstUser
        #         '''
        
        #         cursor.execute(query)
        
        #         # Fetch the result of the count query
        #         result = cursor.fetchone()
        
        #         if result:
        #             total_rows = result.TotalRows
        #             return total_rows
        
        #     except Exception as e:
        #         print(f"Error: {str(e)}")
        #     finally:
        #         # Close the cursor and connection
        #         cursor.close()
        #         conn.close()
        
        # return 0  # Return 0 in case of an error or no rows found
        
        
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
        
        
    def btnLock_clicked(self):
        if self.userId > 0:
            self.update_data()
        else:
            self.insert_new()
            
            
    def insert_new(self):
        # Get the values from the UI widgets
        txtUserName = self.ui_form.txtUserName.toPlainText()
        txtPassword = self.ui_form.txtPassword.toPlainText()
        txtFullName = self.ui_form.txtFullName.toPlainText()
        txtUserCardNumber = self.ui_form.txtUserCardNumber.toPlainText()
        txtDesignation = self.ui_form.txtDesignation.toPlainText()
        txtEntryUserId = 1
        txtEntryDateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        txtUpdateUserId = 1
        txtUpdateDateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        txtIsLocked = True
        txtAspNetUserId = 'NA'
        txtPIN = self.ui_form.txtPIN.toPlainText()
        
        # Insert data into the 'easypos' table
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to insert data into 'easypos' table
                query = '''
                INSERT INTO MstUser
                            (UserName
                            ,Password
                            ,FullName
                            ,UserCardNumber
                            ,Designation
                            ,EntryUserId
                            ,EntryDateTime
                            ,UpdateUserId
                            ,UpdateDateTime
                            ,IsLocked
                            ,AspNetUserId
                            ,UserPIN)
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
                            ,?)
                '''

                # Execute the insert query with the provided values
                cursor.execute(query, (
                    txtUserName,
                    txtPassword,
                    txtFullName,
                    txtUserCardNumber,
                    txtDesignation,
                    txtEntryUserId,
                    txtEntryDateTime,
                    txtUpdateUserId,
                    txtUpdateDateTime,
                    txtIsLocked,
                    txtAspNetUserId,
                    txtPIN
                ))

                # Commit the transaction
                conn.commit()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Inform the user that the data has been inserted successfully
                messagebox.showinfo("Success", "Data inserted into table successfully!")

            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            print("Database connection error.")
            
            
    def update_data(self):
        # Get the values from the UI widgets
        txtUserName = self.ui_form.txtUserName.toPlainText()
        txtPassword = self.ui_form.txtPassword.toPlainText()
        txtFullName = self.ui_form.txtFullName.toPlainText()
        txtUserCardNumber = self.ui_form.txtUserCardNumber.toPlainText()
        txtDesignation = self.ui_form.txtDesignation.toPlainText()
        txtEntryUserId = 1
        txtEntryDateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        txtUpdateUserId = 1
        txtUpdateDateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        txtIsLocked = True
        txtAspNetUserId = 'NA'
        txtPIN = self.ui_form.txtPIN.toPlainText()
        
        # Insert data into the 'easypos' table
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to insert data into 'easypos' table
                query = f'''
                UPDATE MstUser
                SET UserName = ?
                        ,Password = ?
                        ,FullName = ?
                        ,UserCardNumber = ?
                        ,Designation = ?
                        ,UserPIN = ?
                WHERE Id = {self.userId}
                '''

                # Execute the insert query with the provided values
                cursor.execute(query, (
                    txtUserName,
                    txtPassword,
                    txtFullName,
                    txtUserCardNumber,
                    txtDesignation,
                    txtPIN
                ))

                # Commit the transaction
                conn.commit()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Inform the user that the data has been updated successfully
                messagebox.showinfo("Success", "Data updated successfully!")

            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            print("Database connection error.")
            
            
    def btnClose_clicked(self):
        self.destroy()
        call(["python", "Forms/Software/MstUser/UserListFunc.py"])
        
        
    def load_user_detail(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # Modify the SQL query based on filter options
                query = f'''
                SELECT * FROM MstUser WHERE Id = {self.userId}
                '''
                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()
                for row in rows:
                    self.ui_form.txtFullName.setText(row[3])
                    self.ui_form.txtUserName.setText(row[1])
                    self.ui_form.txtPassword.setText(row[2])
                    self.ui_form.txtUserCardNumber.setText(row[4])
                    self.ui_form.txtDesignation.setText(row[5])
                    self.ui_form.txtPIN.setText(row[12])
                    
                # Close the cursor and connection
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error: {str(e)}")
                
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserDetailFunc()
    window.show()
    sys.exit(app.exec_())
