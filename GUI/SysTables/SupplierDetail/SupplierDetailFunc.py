import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTableWidgetItem, QCheckBox, QLineEdit
from PyQt5.QtCore import Qt, QDateTime
from SupplierDetail.SupplierDetail import Ui_Form
import pyodbc
from dotenv import load_dotenv
from tkinter import * 
from tkinter import messagebox 
from subprocess import call

load_dotenv()
class SupplierDetailCombinedApp(QMainWindow):
    def __init__(self, id):
        super().__init__()
        
        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)
        
        # Save
        self.ui_form.btnLock.clicked.connect(self.btnLock_clicked)
        
        # Close
        self.ui_form.btnClose.clicked.connect(self.btnClose_clicked)
        
        # cboTerm
        self.populate_combo_box_term()
        
        # cboAccount
        self.populate_combo_box_account()
        
        # Load details
        self.id = id
        self.load_detail()
    
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
        if self.id > 0:
            self.update_data()
        else:
            self.insert_new()
    
    
    def insert_new(self):
        # Get the values from the UI widgets
        txtSupplier = self.ui_form.txtSupplier.toPlainText()
        txtAddress = self.ui_form.txtAddress.toPlainText()
        txtTelephoneNumber = self.ui_form.txtTelephoneNumber.toPlainText()
        txtCellphoneNumber = self.ui_form.txtCellphoneNumber.toPlainText()
        txtFaxNumber = self.ui_form.txtFaxNumber.toPlainText()
        cboTerm = selected_term_id
        txtTIN = self.ui_form.txtTIN.toPlainText()
        cboAccount = selected_account_id
        txtEntryUserId = 1
        txtEntryDateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        txtUpdateUserId = 1
        txtUpdateDateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        txtIsLocked = True
        
        # Insert data into the 'easypos' table
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to insert data into 'easypos' table
                query = '''
                INSERT INTO MstSupplier
                    (Supplier
                    ,Address
                    ,TelephoneNumber
                    ,CellphoneNumber
                    ,FaxNumber
                    ,TermId
                    ,TIN
                    ,AccountId
                    ,EntryUserId
                    ,EntryDateTime
                    ,UpdateUserId
                    ,UpdateDateTime
                    ,IsLocked)
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
                    ,?)
                '''

                # Execute the insert query with the provided values
                cursor.execute(query, (
                    txtSupplier,
                    txtAddress,
                    txtTelephoneNumber,
                    txtCellphoneNumber,
                    txtFaxNumber,
                    cboTerm,
                    txtTIN,
                    cboAccount,
                    txtEntryUserId,
                    txtEntryDateTime,
                    txtUpdateUserId,
                    txtUpdateDateTime,
                    txtIsLocked
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
        txtSupplier = self.ui_form.txtSupplier.toPlainText()
        txtAddress = self.ui_form.txtAddress.toPlainText()
        txtTelephoneNumber = self.ui_form.txtTelephoneNumber.toPlainText()
        txtCellphoneNumber = self.ui_form.txtCellphoneNumber.toPlainText()
        txtFaxNumber = self.ui_form.txtFaxNumber.toPlainText()
        cboTerm = selected_term_id
        txtTIN = self.ui_form.txtTIN.toPlainText()
        cboAccount = selected_account_id
        
        # Insert data into the 'easypos' table
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to insert data into 'easypos' table
                query = f'''
                UPDATE MstSupplier
                SET Supplier = ?
                    ,Address = ?
                    ,TelephoneNumber = ?
                    ,CellphoneNumber = ?
                    ,FaxNumber = ?
                    ,TermId = ?
                    ,TIN = ?
                    ,AccountId = ?
                WHERE Id = {self.id}
                '''

                # Execute the insert query with the provided values
                cursor.execute(query, (
                    txtSupplier,
                    txtAddress,
                    txtTelephoneNumber,
                    txtCellphoneNumber,
                    txtFaxNumber,
                    cboTerm,
                    txtTIN,
                    cboAccount
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
        call(["python", "Forms/Software/SysTables/TablesFunc.py"])
        
        
    def populate_combo_box_term(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to fetch data from MstAccount table's term column
                query = '''
                SELECT Id, Term
                FROM MstTerm
                ORDER BY Id DESC
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Close the cursor and connection
                cursor.close()
                conn.close()
                
                global term_mapping
                # Create a dictionary to map Term values to their corresponding Ids
                term_mapping = {row[1]: row[0] for row in rows}
                
                # Populate comboBox with the fetched data (displayed values)
                for term in term_mapping.keys():
                    self.ui_form.cboTerm.addItem(term)

                # Connect an event (e.g., comboBoxTerm.currentIndexChanged) to a function
                self.ui_form.cboTerm.currentIndexChanged.connect(self.get_selected_term_id)
                
                # Default value
                global selected_term_id
                selected_term = self.ui_form.cboTerm.currentText()
                selected_term_id = term_mapping.get(selected_term)
            except Exception as e:
                print(f"Error: {str(e)}")
                
                
    def get_selected_term_id(self):
        global selected_term_id
        selected_term = self.ui_form.cboTerm.currentText()
        selected_term_id = term_mapping.get(selected_term)
        
        
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
                # Create a dictionary to map values to their corresponding Ids
                account_mapping = {row[1]: row[0] for row in rows}
                
                # Populate comboBox with the fetched data (displayed values)
                for account in account_mapping.keys():
                    self.ui_form.cboAccount.addItem(account)

                # Connect an event (e.g., comboBox.currentIndexChanged) to a function
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
        
        
    def load_detail(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # Modify the SQL query based on filter options
                query = f'''
                SELECT
                        MstSupplier.Id,
                        MstSupplier.Supplier,
                        MstSupplier.Address,
                        MstSupplier.TelephoneNumber,
                        MstSupplier.CellphoneNumber,
                        MstSupplier.FaxNumber,
                        MstTerm.Term,
                        MstSupplier.TIN, 
                        MstAccount.Account,
                        MstSupplier.EntryUserId,
                        MstSupplier.EntryDateTime,
                        MstSupplier.UpdateUserId,
                        MstSupplier.UpdateDateTime,
                        MstSupplier.IsLocked
                FROM
                        MstSupplier
                        INNER JOIN MstTerm ON MstSupplier.TermId = MstTerm.Id
                        INNER JOIN MstAccount ON MstSupplier.AccountId = MstAccount.Id
                WHERE MstSupplier.Id = {self.id}
                '''
                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()
                
                for row in rows:
                    self.ui_form.txtSupplier.setText(row[1])
                    self.ui_form.txtAddress.setText(row[2])
                    self.ui_form.txtTelephoneNumber.setText(row[3])
                    self.ui_form.txtCellphoneNumber.setText(row[4])
                    self.ui_form.txtFaxNumber.setText(row[5])
                    self.ui_form.cboTerm.setCurrentText(row[6])
                    self.ui_form.txtTIN.setText(row[7])
                    self.ui_form.cboAccount.setCurrentText(row[8])
                    
                # Close the cursor and connection
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error: {str(e)}")
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SupplierDetailCombinedApp(0)
    window.show()
    sys.exit(app.exec_())