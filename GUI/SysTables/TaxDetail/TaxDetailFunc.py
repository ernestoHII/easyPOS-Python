import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTableWidgetItem, QCheckBox, QLineEdit
from PyQt5.QtCore import Qt, QDateTime
from TaxDetail.TaxDetail import Ui_Form
import pyodbc
from dotenv import load_dotenv
from tkinter import * 
from tkinter import messagebox 
from subprocess import call

# Load environment variables from the .env file
load_dotenv()
class TaxDetailCombinedApp(QMainWindow):
    def __init__(self,taxId):
        super().__init__()
        self.tax_id = taxId
        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)
        # Embed the QTableWidget from Ui_Form into the main window
        self.grid_layout = QGridLayout(self.ui_form.frame)
    #Close
        self.ui_form.btnClose.clicked.connect(self.btnClose_clicked)
        #Initialized comboBox Data
        self.populate_combo_box_account()
        #Load Data
        self.load_tax_detail()
        #Click Save
        self.ui_form.btnSave.clicked.connect(self.btnSave_clicked)
        
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
        
    tax_mapping = []
    selected_tax_id = 0
            
    account_mapping = []
    selected_account_id = 0
            
    def populate_combo_box_account(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to fetch data from MstAccount table's term column
                query = '''
                SELECT Id, Account
                FROM MstAccount
                ORDER BY Id DESC
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Close the cursor and connection
                cursor.close()
                conn.close()
                global account_mapping
                # Create a dictionary to map Term values to their corresponding Ids
                account_mapping = {row[1]: row[0] for row in rows}
                
                # Populate comboBoxTerm with the fetched data (displayed values)
                for account in account_mapping.keys():
                    self.ui_form.cboAccount.addItem(account)

                # Connect an event (e.g., comboBoxTerm.currentIndexChanged) to a function
                self.ui_form.cboAccount.currentIndexChanged.connect(self.get_selected_account_id)
                # Default value
                global selected_account_id
                selected_account = self.ui_form.cboAccount.currentText()
                selected_account_id = account_mapping.get(selected_account)
            except Exception as e:
                print(f"Error: {str(e)}")    
                
    def get_selected_account_id(self):
        global selected_account_id
        selected_account = self.ui_form.cboAccount.currentText()
        selected_account_id = account_mapping.get(selected_account)
        
    def load_tax_detail(self):
        conn, cursor = self.establish_db_connection()
        if conn and cursor:
            try:  
                 # Modify the SQL query based on filter options
                query = f'''
                SELECT MstTax.Id, MstTax.Code, MstTax.Tax, MstTax.Rate, MstAccount.Account
                    FROM MstTax INNER JOIN
                         MstAccount ON MstTax.AccountId = MstAccount.Id
                WHERE MstTax.Id = {self.tax_id}
                '''
                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()
                
                for row in rows:
                    self.ui_form.txtCode.setText(row[1])
                    self.ui_form.txtTax.setText(row[2])
                    self.ui_form.txtRate.setText(f'{row[3] : .2f}')
                    self.ui_form.cboAccount.setCurrentText(row[4])
                    
                # Close the cursor and connection
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error: {str(e)}") 
                
    def btnSave_clicked(self):
        code = self.ui_form.txtCode.toPlainText()
        tax =self.ui_form.txtTax.toPlainText()
        rate =float(self.ui_form.txtRate.toPlainText())
        account_id = selected_account_id  
        # Insert data into the 'easypos' table
        conn, cursor = self.establish_db_connection()    
        if conn and cursor:
            try:
                if self.tax_id == 0:
                    # SQL query to insert data into 'easypos' table
                    query = '''
                    INSERT INTO MstTax
                                (Code
                                ,Tax 
                                ,Rate
                                ,AccountId
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
                        tax,
                        rate,
                        account_id
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
                    UPDATE MstTax
                    SET Code = ?
                        ,Tax = ?
                        ,Rate = ?
                        ,AccountId = ?
                    WHERE Id = {self.tax_id}
                    '''
                    # Execute the insert query with the provided values
                    cursor.execute(query, (
                        code,
                        tax,
                        rate,
                        account_id
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
    app = QApplication(sys.argv)
    window = TaxDetailCombinedApp(0)
    window.show()
    sys.exit(app.exec_())    