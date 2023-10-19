import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTableWidgetItem, QCheckBox, QLineEdit
from PyQt5.QtCore import Qt, QDateTime
from AccountDetail.AccountDetail import UI_AccountDetail
import pyodbc
from dotenv import load_dotenv
from tkinter import * 
from tkinter import messagebox 
from subprocess import call

# Load environment variables from the .env file
load_dotenv()
class AccountDetailCombinedApp(QMainWindow):
    def __init__(self,accountId):
        super().__init__()
        self.account_id = accountId
        # Create an instance of Ui_Form
        self.ui_form = UI_AccountDetail()
        self.ui_form.setupUi(self)
        # Embed the QTableWidget from Ui_Form into the main window
        self.grid_layout = QGridLayout(self.ui_form.frame)
        #Close
        self.ui_form.pushButtonClose.clicked.connect(self.btnClose_clicked)
        #Initialized comboBox Data
        self.populate_combo_box_account()
        #Load Data
        self.load_account_detail()
        #Click Save
        self.ui_form.pushButtonSave.clicked.connect(self.btnSave_clicked)
        
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
        
    account_mapping = []
    selected_account_id = 0
            
    def populate_combo_box_account(self):
        try:
            # Populate comboBoxUnit with the fetched data
            rows = ['ASSET', 'LIABILITY','EQUITY','INCOME','EXPENSES','COST OF GOODS', 'OTHER INCOME', 'OTHER EXPENSE', 'INCOME TAX']
            for row in rows:
                self.ui_form.comboBoxAccountType.addItem(row)

        except Exception as e:
            print(f"Error: {str(e)}")
                
    def load_account_detail(self):
        conn, cursor = self.establish_db_connection()
        if conn and cursor:
            try:  
                 # Modify the SQL query based on filter options
                query = f'''
                SELECT Code, Account, AccountType
                FROM MstAccount
                WHERE Id = {self.account_id}
                '''
                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()
                
                for row in rows:
                    self.ui_form.textEditAccountCode.setText(row[0])
                    self.ui_form.textEditAccount.setText(row[1])
                    self.ui_form.comboBoxAccountType.setCurrentText(row[2])
                    
                # Close the cursor and connection
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error: {str(e)}")       
    def btnSave_clicked(self):
        code = self.ui_form.textEditAccountCode.toPlainText()
        account =self.ui_form.textEditAccount.toPlainText()
        account_type = self.ui_form.comboBoxAccountType.currentText()     
        # Insert data into the 'easypos' table
        conn, cursor = self.establish_db_connection()    
        print(self.account_id)
        if conn and cursor:
            try:
                if self.account_id == 0:
                    # SQL query to insert data into 'easypos' table
                    query = '''
                    INSERT INTO MstAccount
                                (Code
                                ,Account 
                                ,IsLocked
                                ,AccountType
                                )
                            VALUES
                                (?
                                ,?
                                ,?
                                ,?)
                    '''
                    # Execute the insert query with the provided values
                    cursor.execute(query, (
                        code,
                        account,
                        True,
                        account_type,
                    ))
                    # Commit the transaction
                    conn.commit()
                 
                    # Close the cursor and connection
                    cursor.close()
                    conn.close()
                    # Inform the user that the data has been inserted successfully
                    messagebox.showinfo("EasyPOS","Add successfully.")
                    self.destroy()
                    call(["python", "Forms/Software/Systables/TablesFunc.py"])
                else:    
                    # SQL query to insert data into 'easypos' table
                    query = f'''
                    UPDATE MstAccount
                    SET Code = ?
                        ,Account = ?
                        ,AccountType = ?
                    WHERE Id = {self.account_id}
                    '''
                    # Execute the insert query with the provided values
                    cursor.execute(query, (
                        code,
                        account,
                        account_type
                    ))

                    # Commit the transaction
                    conn.commit()

                    # Close the cursor and connection
                    cursor.close()
                    conn.close()

                    # Inform the user that the data has been inserted successfully
                    messagebox.showinfo("EasyPOS","Update successfully.")
                    self.destroy()
                    call(["python", "Forms/Software/Systables/TablesFunc.py"])
            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            messagebox.showerror("EasyPOS","Database connection error.")            
    def btnClose_clicked(self):
        self.destroy()
        
if __name__ == "__main__":
    account_id = 0
    app = QApplication(sys.argv)
    window = AccountDetailCombinedApp(account_id)
    window.show()
    sys.exit(app.exec_())