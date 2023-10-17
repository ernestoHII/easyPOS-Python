import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTableWidgetItem, QCheckBox, QLineEdit
from PyQt5.QtCore import Qt, QDateTime
from CustomerDetail import Ui_Form
import pyodbc
from dotenv import load_dotenv
from tkinter import * 
from tkinter import messagebox 
from subprocess import call

# Load environment variables from the .env file
load_dotenv()
class CustomerDetailCombinedApp(QMainWindow):
    def __init__(self,customerId):
        super().__init__()
        self.customer_id = customerId
        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)

        # Embed the QTableWidget from Ui_Form into the main window
        self.grid_layout = QGridLayout(self.ui_form.frame)

        # Connect the textChanged signal of the search input to the search_data function
        # Connect the clicked signals of the "Next" and "Previous" buttons to their respective methods
        #self.ui_form.pushButtonNext.clicked.connect(self.load_next_data)
        #self.ui_form.pushButtonPrevious.clicked.connect(self.load_previous_data)
        self.ui_form.pushButtonLock.clicked.connect(self.btnLock_clicked)
        # Initialize variables to keep track of the current page and number of items per page
        self.current_page = 1
        self.items_per_page = 20
        
        self.populate_combo_box_term()
        self.populate_combo_box_gender()
        self.load_customer_detail()

        # Load data into the QTableWidget for the first page
        #self.load_data(page=self.current_page)
        #Close
        self.ui_form.pushButtonClose.clicked.connect(self.btnClose_clicked)
        
       
    def btnClose_clicked(self):
        self.destroy()
        call(["python", "Forms/Software/MstCustomer/CustomerListFunc.py"])
    def populate_combo_box_gender(self):
        try:
            # Populate comboBoxUnit with the fetched data
            rows = ['male', 'female']
            for row in rows:
                self.ui_form.comboBoxGender.addItem(row)

        except Exception as e:
            print(f"Error: {str(e)}")
    term_mapping = []
    selected_term_id = 0
    def populate_combo_box_term(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to fetch data from MstTerm table's term column
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
                
                # Populate comboBoxTerm with the fetched data (displayed values)
                for term in term_mapping.keys():
                    self.ui_form.comboBoxTerm.addItem(term)

                # Connect an event (e.g., comboBoxTerm.currentIndexChanged) to a function
                self.ui_form.comboBoxTerm.currentIndexChanged.connect(self.get_selected_term_id)
                # Default value
                global selected_term_id
                selected_term = self.ui_form.comboBoxTerm.currentText()
                selected_term_id = term_mapping.get(selected_term)
            except Exception as e:
                print(f"Error: {str(e)}")
    def load_customer_detail(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # Modify the SQL query based on filter options
                query = f'''
                SELECT  MstCustomer.Customer, MstCustomer.Address, MstCustomer.ContactPerson, MstCustomer.ContactNumber, MstCustomer.CreditLimit, MstTerm.Term, MstCustomer.TIN, 
                        MstCustomer.WithReward, MstCustomer.RewardNumber, MstCustomer.RewardConversion, MstCustomer.AvailableReward, MstCustomer.DefaultPriceDescription, MstCustomer.CustomerCode, 
                        MstCustomer.BusinessStyle, MstCustomer.Birthday, MstCustomer.Age, MstCustomer.Gender, MstCustomer.EmailAddress
                FROM    MstCustomer INNER JOIN
                        MstTerm ON MstCustomer.TermId = MstTerm.Id
                WHERE   MstCustomer.Id = {self.customer_id}
                '''
                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()
                for row in rows:
                    print(row[13])
                    self.ui_form.textEditCustomerCOde.setText(row[12])
                    self.ui_form.textEditCustomer.setText(row[0])
                    self.ui_form.textEditAddress.setText(row[1])
                    self.ui_form.textEditContactPerson.setText(row[2])
                    self.ui_form.textEditContactNo.setText(row[3])
                    self.ui_form.textEditCreditLimit.setText(f'{row[4] : .2f}')
                    self.ui_form.comboBoxTerm.setCurrentText(row[5])
                    self.ui_form.textEditTIN.setText(row[6])
                    self.ui_form.checkBoxIsWithReward.setChecked(row[7])
                    self.ui_form.textEditRewardNo.setText(row[8])
                    self.ui_form.textEditRewardConversion.setText(f'{row[9] : .2f}')
                    self.ui_form.textEditAvailableReward.setText(f'{row[10] : .2f}')
                    self.ui_form.textEditBusinessStyle.setText(row[13])
                    self.ui_form.textEditDefaultPrice.setText(row[11])
                    self.ui_form.textEditEmailAddress.setText(row[17])
                    self.ui_form.dateEditBirthday.setDate(row[14])
                    self.ui_form.textEditAge.setText(str(row[15]))
                    self.ui_form.comboBoxGender.setCurrentText(row[16])
                    
                # Close the cursor and connection
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error: {str(e)}")    
    def get_selected_term_id(self):
        global selected_term_id
        selected_term = self.ui_form.comboBoxTerm.currentText()
        selected_term_id = term_mapping.get(selected_term)
        
        if selected_term_id is not None:
            print(f"Selected Term: {selected_term}, ID: {selected_term_id}")
        else:
            print("Selected term not found in the mapping.")  
                      
    def btnLock_clicked(self):
        # Get the values from the UI widgets
        customer_code = self.ui_form.textEditCustomerCOde.toPlainText()
        customer = self.ui_form.textEditCustomer.toPlainText()
        address = self.ui_form.textEditAddress.toPlainText()
        contact_person = self.ui_form.textEditContactPerson.toPlainText()
        customer_number = self.ui_form.textEditContactNo.toPlainText()
        credit_limit = float(self.ui_form.textEditCreditLimit.toPlainText())
        term_id = selected_term_id
        tin = self.ui_form.textEditTIN.toPlainText()
        is_with_reward = self.ui_form.checkBoxIsWithReward.isChecked()
        reward_number = self.ui_form.textEditRewardNo.toPlainText()
        reward_conversion = float(self.ui_form.textEditRewardConversion.toPlainText())
        available_reward = float(self.ui_form.textEditAvailableReward.toPlainText())
        business_style = self.ui_form.textEditBusinessStyle.toPlainText()
        account_id = 64
        entry_user_id = 1
        entry_user_date = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        update_user_id = 1
        update_user_date = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        is_locked = True
        default_price = self.ui_form.textEditDefaultPrice.toPlainText()
        email_address = self.ui_form.textEditEmailAddress.toPlainText()
        birthdate = self.ui_form.dateEditBirthday.date().toString("yyyy-MM-dd")
        age = int(self.ui_form.textEditAge.toPlainText())
        gender = self.ui_form.comboBoxGender.currentText()
        # Insert data into the 'easypos' table
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to insert data into 'easypos' table
                query = f'''
                UPDATE MstCustomer
                SET CustomerCode = ?
                    ,Customer = ?
                    ,Address = ?
                    ,ContactPerson = ?
                    ,ContactNumber = ?
                    ,CreditLimit = ?
                    ,TermId = ?
                    ,TIN = ?
                    ,WithReward = ?
                    ,RewardNumber = ?
                    ,RewardConversion = ?
                    ,AvailableReward = ?
                    ,BusinessStyle = ?
                    ,AccountId = ?
                    ,EntryUserId = ?
                    ,EntryDateTime = ?
                    ,UpdateUserId = ?
                    ,UpdateDateTime = ?
                    ,IsLocked = ?
                    ,DefaultPriceDescription = ?
                    ,EmailAddress = ?
                    ,Birthday = ?
                    ,Age = ?
                    ,Gender = ?
                WHERE Id = {self.customer_id}
                '''
                # Execute the insert query with the provided values
                cursor.execute(query, (
                    customer_code,
                    customer,
                    address,
                    contact_person,
                    customer_number,
                    credit_limit,
                    term_id,
                    tin,
                    is_with_reward,
                    reward_number,
                    reward_conversion,
                    available_reward,
                    business_style,
                    account_id,
                    entry_user_id,
                    entry_user_date,
                    update_user_id,
                    update_user_date,
                    is_locked,
                    default_price,
                    email_address,
                    birthdate,
                    age,
                    gender
                ))

                # Commit the transaction
                conn.commit()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Inform the user that the data has been inserted successfully
                messagebox.showinfo("EasyPOS","Data inserted into table successfully.")

            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            messagebox.showerror("EasyPOS","Database connection error.")  
              
    # def load_last_data(self):
    #     try:
    #         # Get the total number of rows in the table
    #         total_rows = self.get_total_row_count()

    #         if total_rows > 0:
    #             # Calculate the offset to fetch the last 20 rows
    #             offset = max(total_rows - self.items_per_page, 0)

    #             # Load the last 20 data entries
    #             self.load_data(page=1, custom_offset=offset)

    #     except Exception as e:
    #         print(f"Error: {str(e)}")


    # def get_total_row_count(self):
    #     conn, cursor = self.establish_db_connection()

    #     if conn and cursor:
    #         try:
    #             # Execute SQL query to count the total number of rows in the table
    #             query = f'''
    #             SELECT COUNT(*) as TotalRows
    #             FROM TrnSales
    #             '''

    #             cursor.execute(query)

    #             # Fetch the result of the count query
    #             result = cursor.fetchone()

    #             if result:
    #                 total_rows = result.TotalRows
    #                 return total_rows

    #         except Exception as e:
    #             print(f"Error: {str(e)}")
    #         finally:
    #             # Close the cursor and connection
    #             cursor.close()
    #             conn.close()

    #     return 0  # Return 0 in case of an error or no rows found


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

    #For Customer Transaction History
    #def load_data(self, page=1, custom_offset=None):
        #conn, cursor = self.establish_db_connection()

        # if conn and cursor:
        #     try:
        #         # Calculate the offset based on the current page or use the provided custom_offset
        #         offset = (page - 1) * self.items_per_page if custom_offset is None else custom_offset
        #         # SQL QUERY
        #         query = f'''
        #         SELECT TrnSales.SalesNumber, TrnSales.CollectionNumber, MstUser.FullName, TrnSales.Amount, TrnSales.IsLocked, TrnSales.IsTendered, TrnSales.IsCancelled, TrnSales.Remarks
        #         FROM MstCustomer
        #         INNER JOIN TrnSales ON MstCustomer.Id = TrnSales.CustomerId
        #         INNER JOIN MstUser ON TrnSales.SalesAgent = MstUser.Id
        #         WHERE TrnSales.IsLocked = 1
        #         ORDER BY TrnSales.Id ASC
        #         OFFSET {offset} ROWS
        #         FETCH NEXT {self.items_per_page} ROWS ONLY
        #         '''
        #         cursor.execute(query)

        #         # Fetch all rows from the query result
        #         rows = cursor.fetchall()

        #         # Set the number of rows and columns for the QTableWidget
        #         self.ui_form.tableWidgetCustomerHistory.setRowCount(len(rows))
        #         self.ui_form.tableWidgetCustomerHistory.setColumnCount(8)  # Set the appropriate number of columns

        #         # Populate the QTableWidget with data
        #         for row_num, row_data in enumerate(rows):
        #             for col_num, cell_value in enumerate(row_data[:8]):  # Use only the first 10 columns
        #                 item = QTableWidgetItem(str(cell_value))
        #                 self.ui_form.tableWidgetCustomerHistory.setItem(row_num, col_num + 2, item)

        #         # Add checkboxes in columns 10 and 11 based on boolean values in the database
        #         for row_num, row_data in enumerate(rows):
        #             for col_num in range(4, 7):
        #                 item = QTableWidgetItem()
        #                 item.setFlags(item.flags() | 0x0000100)  # Make it editable
        #                 # Check the value in columns 10 and 11 from the database
        #                 checkbox_value = bool(row_data[col_num - 2])  # Subtract 2 to align with the data index
        #                 item.setCheckState(2 if checkbox_value else 0)  # Set to checked (True) or unchecked (False)
        #                 self.ui_form.tableWidgetCustomerHistory.setItem(row_num, col_num, item)

        #         # Set each column width to fit the longest values from each row
        #         for col_num in range(8):
        #             self.ui_form.tableWidgetCustomerHistory.resizeColumnToContents(col_num)

        #         # Check if there are more pages to load
        #         has_more_pages = len(rows) == self.items_per_page
        #         self.ui_form.pushButtonNext.setEnabled(has_more_pages)

        #         # Check if there are previous pages to load
        #         self.ui_form.pushButtonPrevious.setEnabled(page > 1)

        #         # Close the cursor and connection
        #         cursor.close()
        #         conn.close()

        #     except Exception as e:
        #         print(f"Error: {str(e)}")

    # def load_next_data(self):
    #     try:
    #         # Increment the current page
    #         self.current_page += 1

    #         # Load data for the next page
    #         self.load_data(page=self.current_page)

    #     except Exception as e:
    #         print(f"Error: {str(e)}")


    # def load_previous_data(self):
    #     try:
    #         # Decrement the current page
    #         if self.current_page > 1:
    #             self.current_page -= 1

    #             # Load data for the previous page
    #             self.load_data(page=self.current_page)

    #     except Exception as e:
    #         print(f"Error: {str(e)}")
        
if __name__ == "__main__":
    customer_id = 0
    app = QApplication(sys.argv)
    window = CustomerDetailCombinedApp(customer_id)
    window.show()
    sys.exit(app.exec_())