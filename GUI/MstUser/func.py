import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QTableWidgetItem
from PyQt5.QtCore import Qt
from UserList import Ui_Form
import pyodbc
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class CombinedApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)

        # Embed the QTableWidget from Ui_Form into the main window
        self.grid_layout = QGridLayout(self.ui_form.frame)

        # # Connect the textChanged signal of the search input to the search_data function
        # self.ui_form.textEditItemFilter.textChanged.connect(self.search_data)

        # # Connect the clicked signals of the "Next" and "Previous" buttons to their respective methods
        # self.ui_form.pushButtonNext.clicked.connect(self.load_next_data)
        # self.ui_form.pushButtonPrevious.clicked.connect(self.load_previous_data)

        # Initialize variables to keep track of the current page and number of items per page
        self.current_page = 1
        self.items_per_page = 20

        # # Populate the comboBoxIsInventoryFilter with options
        # self.ui_form.comboBoxIsInventoryFilter.addItems(["All", "Inventory", "Non-Inventory"])
        # # Connect the currentIndexChanged signal to update the data
        # self.ui_form.comboBoxIsInventoryFilter.currentIndexChanged.connect(self.update_data_on_filter_change)

        # # Populate the comboBoxIsLockedFilter with options
        # self.ui_form.comboBoxIsLockedFilter.addItems(["All", "Locked", "Unlocked"])
        # # Connect the currentIndexChanged signal to update the data
        # self.ui_form.comboBoxIsLockedFilter.currentIndexChanged.connect(self.update_data_on_filter_change)

        # Load data into the QTableWidget for the first page
        self.load_data(page=self.current_page)
        
        self.load_data(page=self.current_page)
        

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
    #             query = '''
    #             SELECT COUNT(*) as TotalRows
    #             FROM MstItem
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

    def load_data(self, page=1, custom_offset=None):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # Calculate the offset based on the current page or use the provided custom_offset
                # offset = (page - 1) * self.items_per_page if custom_offset is None else custom_offset

                # # Get the selected filter options
                # is_locked_filter = self.ui_form.comboBoxIsLockedFilter.currentText()
                # is_inventory_filter = self.ui_form.comboBoxIsInventoryFilter.currentText()

                # Modify the SQL query based on filter options
                query = f'''
                SELECT UserName, FullName, Designation, IsLocked FROM MstUser
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Set the number of rows and columns for the QTableWidget
                self.ui_form.tableWidget.setRowCount(len(rows))
                self.ui_form.tableWidget.setColumnCount(4)  # Set the appropriate number of columns

                # Populate the QTableWidget with data
                for row_num, row_data in enumerate(rows):
                    for col_num, cell_value in enumerate(row_data[:4]):  # Use only the first 10 columns
                        item = QTableWidgetItem(str(cell_value))
                        self.ui_form.tableWidget.setItem(row_num, col_num, item)

                # # Add checkboxes in columns 10 and 11 based on boolean values in the database
                # for row_num, row_data in enumerate(rows):
                #     for col_num in range(10, 12):
                #         item = QTableWidgetItem()
                #         item.setFlags(item.flags() | 0x0000100)  # Make it editable
                #         # Check the value in columns 10 and 11 from the database
                #         checkbox_value = bool(row_data[col_num - 2])  # Subtract 2 to align with the data index
                #         item.setCheckState(2 if checkbox_value else 0)  # Set to checked (True) or unchecked (False)
                #         self.ui_form.tableWidget.setItem(row_num, col_num, item)

                # Set each column width to fit the longest values from each row
                for col_num in range(4):
                    self.ui_form.tableWidget.resizeColumnToContents(col_num)

                # # Check if there are more pages to load
                # has_more_pages = len(rows) == self.items_per_page
                # self.ui_form.pushButtonNext.setEnabled(has_more_pages)

                # # Check if there are previous pages to load
                # self.ui_form.pushButtonPrevious.setEnabled(page > 1)

                # Close the cursor and connection
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error: {str(e)}")


    # def search_data(self):
    #     conn, cursor = self.establish_db_connection()

    #     if conn and cursor:
    #         try:
    #             # Get the search text from the input box
    #             search_text = self.ui_form.textEditItemFilter.toPlainText().strip()

    #             # Get the selected filter options
    #             is_locked_filter = self.ui_form.comboBoxIsLockedFilter.currentText()
    #             is_inventory_filter = self.ui_form.comboBoxIsInventoryFilter.currentText()

    #             # Modify the SQL query to filter based on the search_text and filter options
    #             query = f'''
    #             SELECT TOP 20 MI.ItemCode, MI.Barcode, MI.ItemDescription, MU.Unit AS Unit, MI.Category, MS.Supplier AS Supplier, MI.Price, MI.OnhandQuantity, MI.IsInventory, MI.IsLocked
    #             FROM MstItem AS MI
    #             LEFT JOIN MstUnit AS MU ON MI.UnitId = MU.Id
    #             LEFT JOIN MstSupplier AS MS ON MI.DefaultSupplierId = MS.Id
    #             WHERE (
    #                 (MI.ItemDescription LIKE ?)
    #                 AND ('{is_locked_filter}' = 'All' OR ('{is_locked_filter}' = 'Locked' AND MI.IsLocked = 1) OR ('{is_locked_filter}' = 'Unlocked' AND MI.IsLocked = 0))
    #                 AND ('{is_inventory_filter}' = 'All' OR ('{is_inventory_filter}' = 'Inventory' AND MI.IsInventory = 1) OR ('{is_inventory_filter}' = 'Non-Inventory' AND MI.IsInventory = 0))
    #             )
    #             ORDER BY MI.ItemDescription ASC
    #             '''

    #             cursor.execute(query, ('%' + search_text + '%',))

    #             # Fetch all rows from the query result
    #             rows = cursor.fetchall()

    #             # Set the number of rows and columns for the QTableWidget
    #             self.ui_form.tableWidget.setRowCount(len(rows))
    #             self.ui_form.tableWidget.setColumnCount(12)  # Set the appropriate number of columns

    #             # Populate the QTableWidget with data
    #             for row_num, row_data in enumerate(rows):
    #                 for col_num, cell_value in enumerate(row_data[:10]):  # Use only the first 10 columns
    #                     item = QTableWidgetItem(str(cell_value))
    #                     self.ui_form.tableWidget.setItem(row_num, col_num + 2, item)

    #             # Add checkboxes in columns 10 and 11 based on boolean values in the database
    #             for row_num, row_data in enumerate(rows):
    #                 for col_num in range(10, 12):
    #                     item = QTableWidgetItem()
    #                     item.setFlags(item.flags() | 0x0000100)  # Make it editable
    #                     # Check the value in columns 10 and 11 from the database
    #                     checkbox_value = bool(row_data[col_num - 2])  # Subtract 2 to align with the data index
    #                     item.setCheckState(2 if checkbox_value else 0)  # Set to checked (True) or unchecked (False)
    #                     self.ui_form.tableWidget.setItem(row_num, col_num, item)

    #             # Set each column width to fit the longest values from each row
    #             for col_num in range(12):
    #                 self.ui_form.tableWidget.resizeColumnToContents(col_num)

    #             # Close the cursor and connection
    #             cursor.close()
    #             conn.close()

    #         except Exception as e:
    #             print(f"Error: {str(e)}")


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
            

    # def update_data_on_filter_change(self):
        # When filter options change, update the data immediately
        # self.current_page = 1  # Reset to the first page
        # self.load_data(page=self.current_page)
        
                                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CombinedApp()
    window.show()
    sys.exit(app.exec_())