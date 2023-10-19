import sys, requests, gc, os
import configparser
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QDialog
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QSizePolicy, QTabWidget, QLineEdit, QFrame, QProgressDialog
from PyQt5.QtWidgets import QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from functools import partial
from MstItem.ItemDetail import Ui_ItemDetail
from MstItem.ItemList import Ui_FormList
from PyQt5.QtWidgets import QMessageBox
from MstItem.ItemPriceDetail.ItemPriceDetail import Ui_DialogItemPriceDetail
from MstItem.ItemComponentDetail.ItemComponentDetail import Ui_DialogItemComponentDetail
from MstItem.ItemPackageDetail.ItemPackageDetail import Ui_DialogItemPackageDetail
from MstItem.ItemAddOnDetail.ItemAddOnDetail import Ui_DialogItemAddOnDetail
from MstItem.ItemModifierDetail.ItemModifierDetail import Ui_DialogItemModifierDetail
from TrnPOS.TrnPOSTouchQuickService.POSTouchQuickServiceList import Ui_POSTouchQuickService
from TrnPOS.TrnPOSTouchQuickService.POSTouchQuickServiceDetail import Ui_POSTouchQuickServiceDetail
from TrnPOS.TrnPOSTouch.POSTouchSalesList import Ui_POSTouchSalesList
from TrnPOS.TrnPOSTouch.POSTouchSalesDetail import Ui_POSTouchSalesDetail
from MstCustomer.CustomerList import Ui_CustomerList
from MstCustomer.CustomerDetail import Ui_CustomerDetail
from MstDiscount.DiscountList import Ui_DiscountList
from MstDiscount.DiscountDetail import Ui_DiscountDetail
from MstDiscount.DiscountSearchItemDetail import Ui_DiscountSearchItemDetail
from TrnPOS.TrnPOSRetail.POSBarcode import Ui_POSBarcode
from TrnPOS.TrnPOSRetail.POSBarcodeDetail import Ui_POSBarcodeDetail
from TrnPOS.TrnPOSRetail.POSBarcodeTender import Ui_POSBarcodeTender
from MstUser.UserList import Ui_UserList
from MstUser.UserDetail import Ui_UserDetail
from SysTables.AccountDetail.AccountDetail import Ui_AccountDetail
from SysTables.AccountDetail.AccountDetail import Ui_AccountDetail
from SysTables.AccountDetail.AccountDetail import Ui_AccountDetail
from SysTables.AccountDetail.AccountDetail import Ui_AccountDetail
from SysTables.AccountDetail.AccountDetail import Ui_AccountDetail
from SysTables.AccountDetail.AccountDetail import Ui_AccountDetail


file_path = 'POS-type.ini'
# Usage
# pos_type_value = read_pos_type_from_ini(file_path)
# print(f"POS type is: {pos_type_value}")

def add_or_select_tab(tab_widget, widget, label):
    # Check if the tab exists
    for index in range(tab_widget.count()):
        if tab_widget.tabText(index) == label:
            # Tab exists, select it
            tab_widget.setCurrentIndex(index)
            return
    
    # If the tab does not exist, add and select
    tab_widget.addTab(widget, label)
    tab_widget.setCurrentWidget(widget)
    
class EmbeddedItemDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_ItemDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonAddItemPrice.clicked.connect(self.open_ItemPriceDetail)
        self.ui.pushButtonAddItemComponent.clicked.connect(self.open_ItemComponentDetail)
        self.ui.pushButtonAddItemPackage.clicked.connect(self.open_Ui_DialogItemPackageDetail)
        self.ui.pushButtonAddItemAddOns.clicked.connect(self.open_Ui_DialogItemAddOnDetail)
        self.ui.pushButtonAddItemModifier.clicked.connect(self.open_Ui_DialogItemModifierDetail)

    def open_ItemPriceDetail(self):
        self.dialog = QDialog(self)
        self.ui_dialog = Ui_DialogItemPriceDetail()
        self.ui_dialog.setupUi(self.dialog)
        self.ui_dialog.pushButton_7.clicked.connect(self.dialog.close)
        self.dialog.show()
    
    def open_ItemComponentDetail(self):
        self.dialog = QDialog(self)
        self.ui_ItemComponentDetail = Ui_DialogItemComponentDetail()
        self.ui_ItemComponentDetail.setupUi(self.dialog)        
        self.ui_ItemComponentDetail.pushButton_7.clicked.connect(self.dialog.close)
        self.dialog.show()

    def open_Ui_DialogItemPackageDetail(self):    
        self.dialog = QDialog(self)                    
        self.ui_ItemPackageDetail = Ui_DialogItemPackageDetail()
        self.ui_ItemPackageDetail.setupUi(self.dialog)   
        self.ui_ItemPackageDetail.pushButton_7.clicked.connect(self.dialog.close)
        self.dialog.show()

    def open_Ui_DialogItemAddOnDetail(self):               
        self.dialog = QDialog(self)              
        self.ui_ItemAddOnDetail = Ui_DialogItemAddOnDetail()
        self.ui_ItemAddOnDetail.setupUi(self.dialog)  
        self.ui_ItemAddOnDetail.pushButton_7.clicked.connect(self.dialog.close)
        self.dialog.show()
        
    def open_Ui_DialogItemModifierDetail(self):        
        self.dialog = QDialog(self)        
        self.ui_ItemModifierDetail = Ui_DialogItemModifierDetail()
        self.ui_ItemModifierDetail.setupUi(self.dialog)                          
        self.ui_ItemModifierDetail.pushButton_7.clicked.connect(self.dialog.close)        
        self.dialog.show()
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedItemList(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_FormList()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonAdd.clicked.connect(self.open_item_detail)

    def close_tab(self):
        # index = self.main_window.tab_widget.indexOf(self)
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

    def open_item_detail(self):  # New method
        tab_item = EmbeddedItemDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, tab_item, "Setup - Item Detail")

class EmbeddedPOSTouchQuickServiceList(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSTouchQuickService()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonWalkIn.clicked.connect(self.open_POSTouchQuickServiceDetail)

    def open_POSTouchQuickServiceDetail(self):
        pos_tab = EmbeddedPOSTouchQuickServiceDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, pos_tab, "Quick Service Detail")
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedPOSTouchQuickServiceDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSTouchQuickServiceDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonTender.clicked.connect(self.open_Tender)  # Changed this line
        self.ui.pushButtonSearchItem.clicked.connect(self.open_discount_search_item_detail)

    def open_discount_search_item_detail(self):  # New method to open the dialog
        self.popup = EmbeddedDiscountSearchItemDetail(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()
    def open_Tender(self):  # New method to open the dialog
        self.popup = EmbeddedPOSBarcodeTender(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()                
    def open_tab(self):
        openTab = Ui_POSTouchQuickServiceDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Quick Service Detail")
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here
                                                                   
class EmbeddedPOSTouchSalesList(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSTouchSalesList()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonWalkIn.clicked.connect(self.open_POSTouchSalesDetail)

    def open_POSTouchSalesDetail(self):
        openTab = EmbeddedPOSTouchSalesDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Activity - POS Touch Detail")
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedPOSTouchSalesDetail(QWidget): #dodo
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSTouchSalesDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonTender.clicked.connect(self.open_Tender)

    def open_Tender(self):  # New method to open the dialog
        self.popup = EmbeddedPOSBarcodeTender(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()           
    def open_tab(self):
        openTab = Ui_POSTouchQuickServiceDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Quick Service Detail")        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedPOSBarcode(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSBarcode()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButton_11.clicked.connect(self.open_POSBarcodeDetail)
        self.ui.pushButton_10.clicked.connect(self.open_Tender)  # Changed this line
    
    def open_Tender(self):  # New method to open the dialog
        self.popup = EmbeddedPOSBarcodeTender(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()   
    def open_POSBarcodeDetail(self):
        openTab = EmbeddedPOSBarcodeDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Activity - POS Barcode Detail")
                        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedPOSBarcodeDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_POSBarcodeDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButton_3.clicked.connect(self.open_Tender)
        self.ui.pushButton_35.clicked.connect(self.open_discount_search_item_detail)

    def open_discount_search_item_detail(self):  # New method to open the dialog
        self.popup = EmbeddedDiscountSearchItemDetail(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()
    def open_Tender(self):  # New method to open the dialog
        self.popup = EmbeddedPOSBarcodeTender(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()    
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedPOSBarcodeTender(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.tab_widget = tab_widget
        self.ui = Ui_POSBarcodeTender()
        self.ui.setupUi(self)                
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        # self.ui.pushButton_3.clicked.connect(self.open_pos_barcode_detail)
        self.ui.pushButtonClose.clicked.connect(self.close)  # 'self.close' is a method provided by QWidget to close the widget
        
    # def open_pos_barcode_detail(self):
    #     openTab = EmbeddedPOSBarcodeDetail(self.main_window, self.tab_widget)
    #     add_or_select_tab(self.main_window.tab_widget, openTab, "Activity - POS Barcode Detail")
                
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here                
class EmbeddedCustomerListCombinedApp(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_CustomerList()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonAdd.clicked.connect(self.open_CustomerDetailCombinedApp)

    def open_CustomerDetailCombinedApp(self):
        openTab = EmbeddedCustomerDetailCombinedApp(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Setup - Customer List")
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedCustomerDetailCombinedApp(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_CustomerDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)

    def open_tab(self):
        openTab = Ui_POSTouchQuickServiceDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Setup - Customer Detail")
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedDiscountList(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_DiscountList()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonAdd.clicked.connect(self.open_CustomerDetailCombinedApp)

    def open_CustomerDetailCombinedApp(self):
        openTab = EmbeddedDiscountDetail(self.main_window, self.tab_widget)
        add_or_select_tab(self.main_window.tab_widget, openTab, "Setup - Discounting Detail")
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here

class EmbeddedDiscountDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_DiscountDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.btnSearch.clicked.connect(self.open_discount_search_item_detail)

    def open_discount_search_item_detail(self):  # New method to open the dialog
        self.popup = EmbeddedDiscountSearchItemDetail(self.main_window, self.tab_widget)  # Pass both required arguments
        self.popup.show()
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here    

class EmbeddedDiscountSearchItemDetail(QWidget):
    def __init__(self, main_window, tab_widget):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_DiscountSearchItemDetail()
        self.ui.setupUi(self)
        self.tab_widget = tab_widget
        self.ui.pushButtonClose.clicked.connect(self.close_tab)
        self.ui.pushButtonClose.clicked.connect(self.close)  # 'self.close' is a method provided by QWidget to close the widget
        
    def close_tab(self):
        index = self.tab_widget.indexOf(self)
        if index != -1:
            self.tab_widget.removeTab(index)
            self.deleteLater()  # Ensure the widget and its children are marked for deletion
        gc.collect()  # <-- Add it here  
                    
class Menu(QMainWindow):
    def __init__(self, tab_widget):
        super().__init__()
        self.tab_widget = tab_widget  # Store the tab widget
        self.total_count = 0  # Initialize total_count        
        self.setWindowTitle("POS - GPT")

        # Get the screen resolution
        screen_resolution = QDesktopWidget().screenGeometry(0)  # For the primary screen
        # Adjust geometry based on resolution
        if screen_resolution.width() == 1280 and screen_resolution.height() == 1024:
            self.setGeometry(0, 0, 1280, 956)
        elif screen_resolution.width() == 1366 and screen_resolution.height() == 768:
            self.setGeometry(0, 0, 1366, 500)
        else:
            # Default size, can be adjusted
            self.setGeometry(0, 0, 1366, 500)   
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Create a layout for the central widget
        central_layout = QVBoxLayout(central_widget)
        grid_layout = QGridLayout()  # We create this layout here, but it isn't attached yet.
        # Initialize variables to keep track of the current page and number of items per page
        self.current_page = 1
        self.items_per_page = 20

        # Create and add buttons to the grid layout
        button_info = [
            ("Item", "img/Item.png"), ("POS - F2", "img/POS.png"), ("Sales Report", "img/Reports.png"), ("POS Report", "img/Reports.png"),
            ("Discounting", "img/Discounting.png"), ("Cash In/Out", "img/Disbursement.png"), ("Remittance Report", "img/Reports.png"),
            ("Settings", "img/Settings.png"), ("Customer", "img/Customer.png"), ("Stock In", "img/Stock In.png"),
            ("Inventory Report", "img/Reports.png"), ("Utilities", "img/Utilities.png"), ("User", "img/User.png"), ("Stock Out", "img/Stock Out.png"),
            ("Stock Count", "img/Stock Count.png"), ("System Tables", "img/System Tables.png")]

        # Create a list of values for the buttons
        button_values = [
            "Setup - Item List", "POS - F2", "Sales Report", "POS Report", "Discounting", "Cash In/Out", "Remittance Report", "Settings", "Customer", "Stock In",
            "Inventory Report", "Utilities", "User", "Stock Out", "Stock Count", "System Tables"]

        for row in range(4):
            for col in range(4):
                index = row * 4 + col
                if index < len(button_info):
                    button_text, icon_path = button_info[index]
                    button_value = button_values[index]  # Get the value for this button
                    container = QWidget()
                    layout = QVBoxLayout(container)
                    button = QPushButton()
                    size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    button.setSizePolicy(size_policy)
                    pixmap = QPixmap()
                    if not pixmap.load(icon_path):
                        print("Error loading image:", pixmap.isNull())
                    else:
                        pixmap = pixmap.scaledToHeight(90)  # Adjusted to be 5% smaller
                        icon = QIcon(pixmap)
                        button.setIcon(icon)
                        button.setIconSize(pixmap.size())
                    # Create a label for the button title (text)
                    title_label = QLabel(button_text)
                    title_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)  # Align text to the bottom center
                    # Make the text bold
                    font = QFont()
                    font.setBold(True)
                    title_label.setFont(font)
                    layout.addWidget(button)
                    layout.addWidget(title_label)
                    grid_layout.addWidget(container, row, col)
                    # Connect a function to the button's clicked signal
                    button.clicked.connect(lambda _, value=button_value: self.create_tab(value))
        self.rows = []  # Initialize rows as an empty list
        # Add the grid layout to the central layout
        central_layout.addLayout(grid_layout)

    def load_table_headers(self, table_widget, increment_page=0):
        # total_count = 0  # Calculate total count from your data source

        self.current_offset = (self.current_page - 1) * self.items_per_page
        table_name = "MstItem"
        # Column Names:
        # 0. Id, 1. ItemCode, 2. BarCode, 3. ItemDescription, 4. Alias, 5. GenericName, 6. Category, 
        # 7. SalesAccountId, 8. AssetAccountId, 9. CostAccountId, 10. InTaxId, 11. OutTaxId, 
        # 12. UnitId, 13. DefaultSupplierId, 14. Cost, 15. MarkUp, 16. Price, 17. ImagePath, 
        # 18. ReorderQuantity, 19. OnhandQuantity, 20. IsInventory, 21. ExpiryDate, 22. LotNumber, 
        # 23. Remarks, 24. EntryUserId, 25. EntryDateTime, 26. UpdateUserId, 27. UpdateDateTime, 
        # 28. IsLocked, 29. DefaultKitchenReport, 30. IsPackage, 31. cValue, 32. ChildItemId, 
        # 33. IsMonitored, 34. IsStickerPrinted
        desired_indices = [1, 2, 3, 13, 6, 14, 16, 19, 20, 28]
        indices_param = "&".join([f"column_indices={i}" for i in desired_indices])
        response = requests.get(f"http://localhost:8000/table-data/{table_name}?{indices_param}&skip={self.current_offset}&limit={self.items_per_page}")
        total_count = response.json().get("total_count", 0)
        
        if response.status_code == 200:
            # For debugging purposes:
            # print(response.json())
            headers = response.json().get("headers", [])
            data = response.json().get("data", [])
            headers = headers
            # headers = ["", ""] + headers
            # self.table_widget.setColumnCount(len(headers))
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            # table_widget.setRowCount(len(data))
            # total_count = response.json().get("total_count", 0)
            # for row_index, row_data in enumerate(data):
            #     for col_index, cell_data in enumerate(row_data):
            #         if col_index in [20, 28]:  # For indices 20 and 28, add a checkbox
            #             checkbox_item = QTableWidgetItem()
            #             checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            #             checkbox_item.setCheckState(Qt.Unchecked)  # Set the default state to unchecked
            #             table_widget.setItem(row_index, col_index, checkbox_item)
            #         else:
            #             table_widget.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))
            max_rows = 15  # Maximum rows to display
            displayed_rows = min(len(data), max_rows)  # The number of rows to actually display, which is the lesser of the length of data or 18

            table_widget.setRowCount(displayed_rows)  # Set the table row count to displayed_rows
            total_count = response.json().get("total_count", 0)

            for row_index, row_data in enumerate(data[:displayed_rows]):  # Loop only through the first displayed_rows of data
                for col_index, cell_data in enumerate(row_data):
                    if col_index in [20, 28]:  # For indices 20 and 28, add a checkbox
                        checkbox_item = QTableWidgetItem()
                        checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        checkbox_item.setCheckState(Qt.Unchecked)  # Set the default state to unchecked
                        table_widget.setItem(row_index, col_index, checkbox_item)
                    else:
                        # table_widget.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))
                        table_item = QTableWidgetItem(str(cell_data))

                        # Center align if the data is integer or boolean
                        if isinstance(cell_data, (int, bool, float)):
                            table_item.setTextAlignment(Qt.AlignCenter)
                            
                        if col_index not in [20, 28]:
                            table_widget.setItem(row_index, col_index, table_item)
                                                
            additional_space = 20  # Number of pixels to add, adjust as needed

            table_widget.resizeColumnsToContents()  # Auto-resize columns based on content

            for col in range(table_widget.columnCount()):
                current_width = table_widget.columnWidth(col)
                table_widget.setColumnWidth(col, current_width + additional_space)
        
        else:
            error_msg = f"Error getting data for table {table_name}: {response.text}"
            print(error_msg)
            # self.show_error_message(error_msg)

        # Update the total_count attribute
        self.total_count = total_count            
        gc.collect()  # <-- Add it here after loading and processing data

    def load_next_page(self, table_widget):
        # Check if there are more pages to load
        total_pages = max(1, -(-self.total_count // self.items_per_page))
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_table_headers(table_widget)

    def load_prev_page(self, table_widget):
        if self.current_page > 1:  # Avoid going into negative or zero pages
            self.current_page -= 1  # decrement the current page here
            self.load_table_headers(table_widget)
      
    def create_tab(self, button_value):
        if self.tab_widget is not None:
            for index in range(self.tab_widget.count()):
                if self.tab_widget.tabText(index) == button_value:
                    self.tab_widget.setCurrentIndex(index)
                    return

            if button_value == "Setup - Item List":
                listTab = EmbeddedItemList(self, self.tab_widget)
                add_or_select_tab(self.tab_widget, listTab, "Setup - Item List")
            elif button_value == "POS - F2":
                pos_type_value = read_pos_type_from_ini(file_path)
                print(pos_type_value)
                if pos_type_value == 3:
                    posTab = EmbeddedPOSTouchQuickServiceList(self, self.tab_widget)
                    add_or_select_tab(self.tab_widget, posTab, "Activity - POS Touch Quick Service")
                elif pos_type_value == 2:
                    PTSLTab = EmbeddedPOSTouchSalesList(self, self.tab_widget)
                    add_or_select_tab(self.tab_widget, PTSLTab, "Activity - POS Touch")           
                elif pos_type_value == 1:
                    barcodeTab = EmbeddedPOSBarcode(self, self.tab_widget)
                    add_or_select_tab(self.tab_widget, barcodeTab, "Activity - POS Barcode")                        
            elif button_value == "Customer":
                customerTab = EmbeddedCustomerListCombinedApp(self, self.tab_widget)
                add_or_select_tab(self.tab_widget, customerTab, "Setup - Customer")                                
            elif button_value == "Discounting":
                discountTab = EmbeddedDiscountList(self, self.tab_widget)
                add_or_select_tab(self.tab_widget, discountTab, "Setup - Discounting List")                                    
            elif button_value == "User": #dldl
                User_Tab = Ui_UserList(self, self.tab_widget)
                add_or_select_tab(self.tab_widget, User_Tab, "Setup - User List")    
            elif button_value == "System Tables": #dldl
                systemTab = Ui_AccountDetail(self, self.tab_widget)
                add_or_select_tab(self.tab_widget, systemTab, "System - System Tables")    
                                                                                                                  
    def load_first_page(self, table_widget):
        self.current_page = 1
        self.load_table_headers(table_widget)

    def load_last_page(self, table_widget):
        self.current_page = -(-self.total_count // self.items_per_page)  # Calculate total pages dynamically
        self.load_table_headers(table_widget)

    def close_current_tab(self):
        # Get the index of the current tab
        current_index = self.tab_widget.currentIndex()
        
        # Remove the current tab
        self.tab_widget.removeTab(current_index)

    def show_error_message(self, msg):
        QMessageBox.critical(self, "Error", msg)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Tabbed Grid of Buttons")
        self.setGeometry(0, 0, 1366, 690)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Create a tab widget
        self.tab_widget = QTabWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.tab_widget)
        # Add "Menu" tab and pass the tab_widget to the Menu class
        menu_tab = Menu(self.tab_widget)
        self.tab_widget.addTab(menu_tab, "Menu")

def read_pos_type_from_ini(file_path):
    config = configparser.ConfigParser()

    # Check if the file exists
    if not os.path.exists(file_path):
        # If it doesn't exist, create it with default values
        config['POStype'] = {'type': '3'}
        with open(file_path, 'w') as configfile:
            config.write(configfile)

    config.read(file_path)

    try:
        pos_type = config.get('POStype', 'type')
        return int(pos_type)
    except configparser.NoSectionError:
        print(f"Error: No section 'POStype' found in {file_path}")
    except configparser.NoOptionError:
        print(f"Error: No option 'type' found in section 'POStype' of {file_path}")
    except ValueError:
        print(f"Error: Invalid value for 'type' in {file_path}. It should be an integer.")
    except Exception as e:
        print(f"Unexpected error reading {file_path}: {e}")

    return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

