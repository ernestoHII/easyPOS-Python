import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QDate
from ItemDetail import Ui_Form
import pyodbc
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class GeneralInformation(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of Ui_Form
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self)

        # Disable the textEditItemCode widget
        self.ui_form.textEditItemCode.setEnabled(False)
        self.ui_form.textEditBarcode.setText("N/A")
        self.ui_form.textEditItemDescription.setText("N/A")
        self.ui_form.textEditAlias.setText("N/A")
        self.ui_form.textEditGenericName.setText("N/A")
        self.ui_form.textEditRemarks.setText("N/A")
        self.ui_form.textEditLotNo.setText("N/A")

        self.ui_form.textEditCost.setText("{:.2f}".format(0.00))
        self.ui_form.textEditMarkUp.setText("{:.2f}".format(0.00))
        self.ui_form.textEditPrice.setText("{:.2f}".format(0.00))
        self.ui_form.textEditStockLevelQty.setText("{:.2f}".format(0.00))
        self.ui_form.textEditOnHandQty.setText("{:.2f}".format(0.00))        
        self.ui_form.textEditConversionValue.setText("{:.2f}".format(0.00))

        # Set the current date as the date value for dateEditExpiryDate
        current_date = QDate.currentDate()
        self.ui_form.dateEditExpiryDate.setDate(current_date)

        # Make dateEditExpiryDate display a calendar popup when clicked
        self.ui_form.dateEditExpiryDate.setCalendarPopup(True)
                
        self.ui_form.checkBoxIsInventory.setChecked(True)
        
        # comboBoxChildItem
        self. populate_combo_box_child_item()
    
        # Fetch data from MstCategory table's CategoryName column and populate comboBoxCategory
        self.populate_combo_box_category()

        # Fetch data from MstUnit table's Unit column and populate comboBoxUnit
        self.populate_combo_box_unit()

        # Fetch data from MstSupplier table's SupplierName column and populate comboBoxSupplier
        self.populate_combo_box_supplier()
                    
        # Fetch data from MstTax table's Code column and populate comboBoxVAT
        self.populate_combo_box_vat()

        # Connect the pushButtonUploadImage clicked signal to the open_file_dialog function
        self.ui_form.pushButtonUploadImage.clicked.connect(self.open_file_dialog)
        # Get a reference to the QLineEdit widget for the image path
        self.textEditImageFilePath = self.ui_form.textEditImageFilePath  # Add this line

        # Connect the pushButtonLock clicked signal to the lock_button_clicked function
        self.ui_form.pushButtonLock.clicked.connect(self.lock_button_clicked)
        
        # Fetch the last data from the ItemCode column and populate textEditItemCode
        self.load_data()
        
        self.ui_form.pushButtonClose.clicked.connect(self.handle_close_clicked)

    def handle_close_clicked(self):
        # Get the item code from textEditItemCode
        item_code = self.ui_form.textEditItemCode.toPlainText()

        # Delete the row with the specified item code from the MstItem table
        if self.delete_item_from_database(item_code):
            # Refresh textEditItemCode with a new value (e.g., increment by 1)
            self.refresh_item_code()

    def delete_item_from_database(self, item_code):
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

            # SQL query to delete the item with the specified item code
            query = f'DELETE FROM MstItem WHERE ItemCode = ?'
            cursor.execute(query, (item_code,))

            # Commit the transaction
            conn.commit()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            print(f"Item with ItemCode {item_code} deleted successfully.")
            return True

        except Exception as e:
            print(f"Error deleting item: {str(e)}")
            return False

    def refresh_item_code(self):
        # You can implement the logic to refresh textEditItemCode here.
        # For example, increment the item code by 1 and set it in textEditItemCode.
        # You can fetch the last item code from the database and add 1 to it.
        pass
    
    def lock_button_clicked(self):
        
        # Get the value of ItemCode from textEditItemCode
        item_code = self.ui_form.textEditItemCode.toPlainText()        
        # Get the values from the UI widgets
        item_code = self.ui_form.textEditItemCode.toPlainText()
        barcode = self.ui_form.textEditBarcode.toPlainText()
        item_description = self.ui_form.textEditItemDescription.toPlainText()
        alias = self.ui_form.textEditAlias.toPlainText()
        generic_name = self.ui_form.textEditGenericName.toPlainText()
        remarks = self.ui_form.textEditRemarks.toPlainText()
        lot_no = self.ui_form.textEditLotNo.toPlainText()
        cost = self.ui_form.textEditCost.toPlainText()  # Use toPlainText() for QTextEdit
        markup = self.ui_form.textEditMarkUp.toPlainText()  # Use toPlainText() for QTextEdit
        price = self.ui_form.textEditPrice.toPlainText()  # Use toPlainText() for QTextEdit
        stock_level_qty = self.ui_form.textEditStockLevelQty.toPlainText()  # Use toPlainText() for QTextEdit
        on_hand_qty = self.ui_form.textEditOnHandQty.toPlainText()  # Use toPlainText() for QTextEdit
        conversion_value = self.ui_form.textEditConversionValue.toPlainText()  # Use toPlainText() for QTextEdit
        expiry_date = self.ui_form.dateEditExpiryDate.date().toString("yyyy-MM-dd")
        is_inventory = self.ui_form.checkBoxIsInventory.isChecked()
        is_sticker_printed = self.ui_form.checkBoxIsStickerPrinted.isChecked()
        category = self.ui_form.comboBoxCategory.currentText()
        unit = self.ui_form.comboBoxUnit.currentText()
        supplier = self.ui_form.comboBoxSupplier.currentText()
        vat = self.ui_form.comboBoxVAT.currentText()
        child_item = self.ui_form.comboBoxChildItem.currentText()
        image_path = self.ui_form.textEditImageFilePath.toPlainText()  # Use toPlainText() for QTextEdit

        # Insert data into the 'easypos' table
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to insert data into 'easypos' table
                # query = '''
                # INSERT INTO MstItem (
                #     ItemCode, Barcode, ItemDescription, Alias, GenericName, Remarks, LotNo, Cost, MarkUp, Price,
                #     StockLevelQty, OnHandQty, ConversionValue, ExpiryDate, IsInventory, IsStickerPrinted,
                #     Category, Unit, Supplier, VAT, ChildItem, ImagePath
                # ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                # '''
                query = '''
                INSERT INTO MstItem (
                    ImagePath
                ) VALUES (?)
                '''
                
                # Execute the insert query with the provided values
                # cursor.execute(query, (
                #     item_code, barcode, item_description, alias, generic_name, remarks, lot_no, cost, markup, price,
                #     stock_level_qty, on_hand_qty, conversion_value, expiry_date, is_inventory, is_sticker_printed,
                #     category, unit, supplier, vat, child_item, image_path
                # ))
                cursor.execute(query, (
                    image_path
                ))
                # Commit the transaction
                conn.commit()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Inform the user that the data has been inserted successfully
                print("Data inserted into 'easypos' table successfully.")

            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            print("Database connection error.")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Optional: Allow read-only access
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp);;All Files (*)", options=options)

        if file_name:
            # Set the selected file's path in the QLineEdit
            self.textEditImageFilePath.setText(file_name)  # Use self.textEditImageFilePath

    def populate_combo_box_child_item(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to fetch data from the child item table's ChildItemName column
                query = '''
                SELECT Alias
                FROM MstItem
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Populate comboBoxChildItem with the fetched data
                for row in rows:
                    self.ui_form.comboBoxChildItem.addItem(row[0])

            except Exception as e:
                print(f"Error: {str(e)}")


    def populate_combo_box_category(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to fetch data from MstCategory table's CategoryName column
                query = '''
                SELECT Category
                FROM MstItemCategory
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Populate comboBoxCategory with the fetched data
                for row in rows:
                    self.ui_form.comboBoxCategory.addItem(row[0])

            except Exception as e:
                print(f"Error: {str(e)}")

    def populate_combo_box_unit(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to fetch data from MstUnit table's Unit column
                query = '''
                SELECT Unit
                FROM MstUnit
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Populate comboBoxUnit with the fetched data
                for row in rows:
                    self.ui_form.comboBoxUnit.addItem(row[0])

            except Exception as e:
                print(f"Error: {str(e)}")

    def populate_combo_box_supplier(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to fetch data from MstSupplier table's Supplier column
                query = '''
                SELECT Supplier
                FROM MstSupplier
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Populate comboBoxSupplier with the fetched data
                for row in rows:
                    self.ui_form.comboBoxSupplier.addItem(row[0])

            except Exception as e:
                print(f"Error: {str(e)}")
                                    
    def populate_combo_box_vat(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to fetch data from MstTax table's Code column
                query = '''
                SELECT Code
                FROM MstTax
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Populate comboBoxVAT with the fetched data
                for row in rows:
                    self.ui_form.comboBoxVAT.addItem(row[0])

            except Exception as e:
                print(f"Error: {str(e)}")
            
    def load_data(self):
        conn, cursor = self.establish_db_connection()

        if conn and cursor:
            try:
                # SQL query to fetch the last row's ItemCode
                query = '''
                SELECT TOP 1 MI.ItemCode
                FROM MstItem AS MI
                ORDER BY MI.ItemCode DESC
                '''

                cursor.execute(query)

                # Fetch the last row from the query result
                row = cursor.fetchone()

                # Close the cursor and connection
                cursor.close()
                conn.close()

                # Set the textEditItemCode widget's text using the data from the last row
                if row:
                    last_item_code = row[0]
                    new_item_code = int(last_item_code) - 2  # Increment the last item code
                    print(new_item_code - 2)
                    formatted_item_code = str(new_item_code).zfill(10)  # Pad with leading zeros to a width of 10
                    self.ui_form.textEditItemCode.setText(formatted_item_code)
                else:
                    # If there are no rows in the table, start with item code 1
                    self.ui_form.textEditItemCode.setText("0000000001")

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
                                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneralInformation()
    window.show()
    sys.exit(app.exec_())