import sys, requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QSizePolicy, QTabWidget, QLineEdit, QFrame, QProgressDialog
from PyQt5.QtWidgets import QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from functools import partial
from MstItem.ItemDetail import Ui_ItemDetail

class EmbeddedItemDetail(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ItemDetail()
        self.ui.setupUi(self)  # Setting up the Ui_Form inside this QWidget

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
            self.setGeometry(0, 0, 1350, 600)
        else:
            # Default size, can be adjusted
            self.setGeometry(0, 0, 1366, 600)
                            
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        central_layout = QVBoxLayout(central_widget)
        grid_layout = QGridLayout()  # We create this layout here, but it isn't attached yet.

        # Initialize variables to keep track of the current page and number of items per page
        self.current_page = 1
        self.items_per_page = 20
        # self.current_offset = (self.current_page - 1) * self.items_per_page

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
                        pixmap = pixmap.scaledToHeight(105)  # Adjusted to be 5% smaller
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

        # Create First, Previous, Next, and Last buttons for pagination
        self.first_button = QPushButton("First")
        self.previous_button = QPushButton("Previous")
        self.page_label = QLabel("1/1")  # default text, this will be updated later
        self.page_label.setAlignment(Qt.AlignCenter)
        self.next_button = QPushButton("Next")
        self.last_button = QPushButton("Last")
        self.first_button.clicked.connect(self.load_first_page)
        self.previous_button.clicked.connect(self.load_prev_page)
        self.next_button.clicked.connect(self.load_next_page)
        self.last_button.clicked.connect(self.load_last_page)

    
        self.rows = []  # Initialize rows as an empty list

        # Add the grid layout to the central layout
        central_layout.addLayout(grid_layout)
        
    def load_table_headers(self, table_widget, increment_page=0, filter_text=""):

        total_count = 0  # Calculate total count from your data source

        # if increment_page != 0:
        #     self.current_page += increment_page
        
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

        # Include the filter_text in the request if provided
        if filter_text:
            response = requests.get(f"http://localhost:8000/table-data/{table_name}?{indices_param}&skip={self.current_offset}&limit={self.items_per_page}&ItemDescription={filter_text}")
        else:
            response = requests.get(f"http://localhost:8000/table-data/{table_name}?{indices_param}&skip={self.current_offset}&limit={self.items_per_page}")

        
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
            table_widget.setRowCount(len(data))
            
            total_count = response.json().get("total_count", 0)
            
            for row_index, row_data in enumerate(data):
                for col_index, cell_data in enumerate(row_data):
                    if col_index in [20, 28]:  # For indices 20 and 28, add a checkbox
                        checkbox_item = QTableWidgetItem()
                        checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        checkbox_item.setCheckState(Qt.Unchecked)  # Set the default state to unchecked
                        table_widget.setItem(row_index, col_index, checkbox_item)
                    else:
                        table_widget.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))


        else:
            error_msg = f"Error getting data for table {table_name}: {response.text}"
            print(error_msg)
            self.show_error_message(error_msg)

        # Update the total_count attribute
        self.total_count = total_count            
        total_pages = max(1, -(-total_count // self.items_per_page))  # Calculate total pages dynamically
        self.page_label.setText(f"{self.current_page}/{total_pages}")

        # Update the Next button status based on the current page and total pages
        if self.current_page >= total_pages:
            self.next_button.setEnabled(False)
        else:
            self.next_button.setEnabled(True)

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

            new_tab = QWidget()
            self.tab_widget.addTab(new_tab, button_value)
            index = self.tab_widget.indexOf(new_tab)
            if index != -1:
                self.tab_widget.setCurrentIndex(index)

            if button_value == "Setup - Item List":
                # Create a QVBoxLayout for the new tab to organize its elements
                new_tab_layout = QVBoxLayout(new_tab)

                frame = QFrame()
                frame.setStyleSheet("background-color: rgb(255, 255, 255);")
                frame.setFrameShape(QFrame.Panel)
                frame.setFrameShadow(QFrame.Raised)
                new_tab_layout.addWidget(frame)

                # Create a QHBoxLayout for the search box and buttons
                search_layout = QHBoxLayout()

                search_box = QLineEdit()  # Create a search box
                add_button = QPushButton("ADD")  # Create a search button
                close_button = QPushButton("Close")  # Create a clear button

                search_layout.addWidget(search_box)
                search_layout.addWidget(add_button)
                search_layout.addWidget(close_button)
                search_box.textChanged.connect(lambda: self.load_table_headers(table_widget, filter_text=search_box.text()))

                new_tab_layout.addLayout(search_layout)

                # Create a QHBoxLayout for the two dropdown boxes
                dropdown_layout = QHBoxLayout()

                combo_box1 = QComboBox()  # Create the first dropdown
                combo_box2 = QComboBox()  # Create the second dropdown

                # Add items to the dropdown boxes
                combo_box1.addItems(["All", "Inventory", "Non-Inventory"])
                combo_box2.addItems(["All", "Locked", "Unlocked"])

                # Connect the currentIndexChanged signal of combo_box1 to the update_data_on_filter_change method
                combo_box1.currentIndexChanged.connect(lambda: self.update_data_on_filter_change(combo_box1))
                dropdown_layout.addWidget(combo_box1)
                dropdown_layout.addWidget(combo_box2)
                new_tab_layout.addLayout(dropdown_layout)

                # Create a QTableWidget and add it to the layout
                table_widget = QTableWidget()
                new_tab_layout.addWidget(table_widget)
                headers = ["", "", "Item Code", "Barcode", "Description", "Unit", "Category", "Supplier", "Price", "Quantity", "Inventory", "Locked"]
                table_widget.setColumnCount(len(headers))
                table_widget.setHorizontalHeaderLabels(headers)
                # Set the column resizing mode to stretch
                table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                # Create First, Previous, Next, and Last buttons for pagination
                first_button = QPushButton("First")
                previous_button = QPushButton("Previous")
                next_button = QPushButton("Next")
                last_button = QPushButton("Last")

                # Add them to a layout
                pagination_layout = QHBoxLayout()
                pagination_layout.addWidget(first_button)
                pagination_layout.addWidget(previous_button)
                pagination_layout.addWidget(self.page_label)  # Add the new label
                pagination_layout.addWidget(next_button)
                pagination_layout.addWidget(last_button)
                first_button.clicked.connect(partial(self.load_first_page, table_widget))
                previous_button.clicked.connect(partial(self.load_prev_page, table_widget))
                next_button.clicked.connect(partial(self.load_next_page, table_widget))
                last_button.clicked.connect(partial(self.load_last_page, table_widget))
                new_tab_layout.addLayout(pagination_layout)
                new_tab.setLayout(new_tab_layout)
                # self.load_table_headers(table_widget, increment_page=1)
                self.load_table_headers(table_widget)
                close_button.clicked.connect(self.close_current_tab)
                add_button.clicked.connect(self.add_item_detail_tab)  # Connect the add_button click event to a new function

    def add_item_detail_tab(self):
        item_detail_tab = EmbeddedItemDetail()
        self.tab_widget.addTab(item_detail_tab, "Item Detail")
        self.tab_widget.setCurrentWidget(item_detail_tab)

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

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Tabbed Grid of Buttons")
        self.setGeometry(0, 0, 1366, 720)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a tab widget
        self.tab_widget = QTabWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.tab_widget)

        # Add "Menu" tab and pass the tab_widget to the Menu class
        menu_tab = Menu(self.tab_widget)
        self.tab_widget.addTab(menu_tab, "Menu")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
