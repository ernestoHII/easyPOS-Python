import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTableWidgetItem, QCheckBox, QLineEdit
from PyQt5.QtCore import Qt, QDateTime
from CardTypeDetail.CardTypeDetail import Ui_Form
import pyodbc
from dotenv import load_dotenv
from tkinter import * 
from tkinter import messagebox 
from subprocess import call

load_dotenv()
class CardTypeDetailCombinedApp(QMainWindow):
    def __init__(self, id):
        super().__init__()
        
        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)
        
        # Save
        self.ui_form.btnSave.clicked.connect(self.btnSave_clicked)
        
        # Close
        self.ui_form.btnClose.clicked.connect(self.btnClose_clicked)
        
        # cboPayType
        self.populate_combo_box_pay_type()
        
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
        
        
    def btnSave_clicked(self):
        if self.id > 0:
            self.update_data()
        else:
            self.insert_new()
    
    
    def insert_new(self):
        # Get the values from the UI widgets
        cboPayType = selected_pay_type_id
        txtCardType = self.ui_form.txtCardType.toPlainText()
        
        # Insert data into the 'easypos' table
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to insert data into 'easypos' table
                query = '''
                INSERT INTO MstCardType
                    (PaytypeId
                    ,CardType)
                VALUES
                    (?
                    ,?)
                '''

                # Execute the insert query with the provided values
                cursor.execute(query, (
                    cboPayType,
                    txtCardType
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
        cboPayType = selected_pay_type_id
        txtCardType = self.ui_form.txtCardType.toPlainText()
        
        # Insert data into the 'easypos' table
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to insert data into 'easypos' table
                query = f'''
                UPDATE MstCardType
                SET PaytypeId = ?
                    ,CardType = ?
                WHERE Id = {self.id}
                '''

                # Execute the insert query with the provided values
                cursor.execute(query, (
                    cboPayType,
                    txtCardType
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
        
        
    def populate_combo_box_pay_type(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to fetch data from MstAccount table's term column
                query = '''
                SELECT Id, PayType
                FROM MstPayType
                ORDER BY Id DESC
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Close the cursor and connection
                cursor.close()
                conn.close()
                
                global pay_type_mapping
                # Create a dictionary to map Term values to their corresponding Ids
                pay_type_mapping = {row[1]: row[0] for row in rows}
                
                # Populate comboBox with the fetched data (displayed values)
                for pay_type in pay_type_mapping.keys():
                    self.ui_form.cboPayType.addItem(pay_type)

                # Connect an event (e.g., comboBoxTerm.currentIndexChanged) to a function
                self.ui_form.cboPayType.currentIndexChanged.connect(self.get_selected_pay_type_id)
                
                # Default value
                global selected_pay_type_id
                selected_pay_type = self.ui_form.cboPayType.currentText()
                selected_pay_type_id = pay_type_mapping.get(selected_pay_type)
            except Exception as e:
                print(f"Error: {str(e)}")
                
                
    def get_selected_pay_type_id(self):
        global selected_pay_type_id
        selected_pay_type = self.ui_form.cboPayType.currentText()
        selected_pay_type_id = pay_type_mapping.get(selected_pay_type)
        
        
    def load_detail(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # Modify the SQL query based on filter options
                query = f'''
                SELECT
                        MstCardType.Id,
                        MstPayType.PayType,
                        MstCardType.CardType
                FROM
                        MstCardType
                        INNER JOIN MstPayType ON MstCardType.PaytypeId = MstPayType.Id
                WHERE MstCardType.Id = {self.id}
                '''
                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()
                
                for row in rows:
                    self.ui_form.cboPayType.setCurrentText(row[1])
                    self.ui_form.txtCardType.setText(row[2])
                    
                # Close the cursor and connection
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error: {str(e)}")
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CardTypeDetailCombinedApp (0)
    window.show()
    sys.exit(app.exec_())