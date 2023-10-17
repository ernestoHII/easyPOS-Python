import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTableWidgetItem, QCheckBox, QLineEdit, QFileDialog, QCalendarWidget, QDateEdit, QPushButton,QToolTip
from PyQt5.QtCore import Qt, QDate
from POSTouchQuickServiceDetail import Ui_Form
from PyQt5.QtCore import QDate
import pyodbc
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
class POSTouchQuickServiceCombinedApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)
        # Load data into the QTableWidget for the first page
        # self.load_data()
        itemGroupItemNoOfButtons = 30
        self.ItemGroupNoOfButtons = 6
        self.ItemGroupPages = 1
        self.ItemGroupPage = 1
        self.fill_push_button_item_group()
        # self.ItemGroupToolTip = QPushButton()
        itemGroupItemButtons =[
                self.ui_form.pushButtonItem1,
                self.ui_form.pushButtonItem2,
                self.ui_form.pushButtonItem3,
                self.ui_form.pushButtonItem4,
                self.ui_form.pushButtonItem5,
                self.ui_form.pushButtonItem6,
                self.ui_form.pushButtonItem7,
                self.ui_form.pushButtonItem8,
                self.ui_form.pushButtonItem9,
                self.ui_form.pushButtonItem10,
                self.ui_form.pushButtonItem11,
                self.ui_form.pushButtonItem12,
                self.ui_form.pushButtonItem13,
                self.ui_form.pushButtonItem14,
                self.ui_form.pushButtonItem15,
                self.ui_form.pushButtonItem16,
                self.ui_form.pushButtonItem17,
                self.ui_form.pushButtonItem18,
                self.ui_form.pushButtonItem19,
                self.ui_form.pushButtonItem20,
                self.ui_form.pushButtonItem21,
                self.ui_form.pushButtonItem22,
                self.ui_form.pushButtonItem23,
                self.ui_form.pushButtonItem24,
                self.ui_form.pushButtonItem25,
                self.ui_form.pushButtonItem26,
                self.ui_form.pushButtonItem27,
                self.ui_form.pushButtonItem28,
                self.ui_form.pushButtonItem29,
                self.ui_form.pushButtonItem30
        ]
        # for button in range(itemGroupItemNoOfButtons):
        #     itemGroupItemButtons[button].clicked.connect()
        
    def fill_push_button_item_group(self):
        conn, cursor = self.establish_db_connection()
        
        if conn and cursor:
            try:
                 # SQL query to fetch data from MstUnit table's term column
                query = '''
                SELECT Id, ItemGroup
                FROM MstItemGroup
                ORDER BY Id DESC
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Close the cursor and connection
                cursor.close()
                conn.close()
                
                global item_group_mapping
                # Create a dictionary to map Term values to their corresponding Ids
                item_group_mapping = {row[1]: row[0] for row in rows}
                # Assuming you have a list named 'listItemGroups'
                start_index = (self.ItemGroupPage - 1) * self.ItemGroupNoOfButtons
                end_index = start_index + self.ItemGroupNoOfButtons

                # Slice the list to get the desired portion
                sliced_list = rows[start_index:end_index]
                # Converted to a new list
                result_list = list(sliced_list)
                
                # button = QPushButton[
                #     self.ui_form.pushButtonItemGroup1,
                #     self.ui_form.pushButtonItemGroup2,
                #     self.ui_form.pushButtonItemGroup3,
                #     self.ui_form.pushButtonItemGroup4,
                #     self.ui_form.pushButtonItemGroup1,
                #     self.ui_form.pushButtonItemGroup1,
                #     self.ui_form.pushButtonItemGroup1,
                # ]
                
                # for index in range(self.ItemGroupNoOfButtons):
                #     button[index].setText("")
                # if(result_list is not None):
                #     for i , item in enumerate(result_list):
                        # self.ItemGroupToolTip.setToolTip(str(item.Id))
                        # button[i].setText(item.ItemGroup)
                        
                    
            except Exception as e:
                print(f"Error: {str(e)}")
            
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
        
        
    def load_data(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # Modify the SQL query based on filter options
                query = f'''
                SELECT MstItem.ItemDescription, TrnSalesLine.Quantity, MstUnit.Unit, TrnSalesLine.Price, TrnSalesLine.DiscountAmount, TrnSales.Amount
                FROM TrnSales INNER JOIN
                     TrnSalesLine ON TrnSales.Id = TrnSalesLine.SalesId INNER JOIN
                     MstItem ON TrnSalesLine.ItemId = MstItem.Id INNER JOIN
                     MstUnit ON TrnSalesLine.UnitId = MstUnit.Id AND MstItem.UnitId = MstUnit.Id
                WHERE TrnSales.Id = 9391
                '''
                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Set the number of rows and columns for the QTableWidget
                self.ui_form.tableWidgetSaleDetailList.setRowCount(len(rows))
                self.ui_form.tableWidgetSaleDetailList.setColumnCount(6)  # Set the appropriate number of columns

                # Populate the QTableWidget with data
                for row_num, row_data in enumerate(rows):
                    for col_num, cell_value in enumerate(row_data[:6]):  # Use only the first 10 columns
                        item = QTableWidgetItem(str(cell_value))
                        self.ui_form.tableWidgetSaleDetailList.setItem(row_num, col_num, item)

                # Set each column width to fit the longest values from each row
                for col_num in range(6):
                    self.ui_form.tableWidgetSaleDetailList.resizeColumnToContents(col_num)

                # Close the cursor and connection
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error: {str(e)}")
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = POSTouchQuickServiceCombinedApp()
    window.show()
    sys.exit(app.exec_())