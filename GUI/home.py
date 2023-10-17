import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QSizePolicy, QTabWidget, QLineEdit, QFrame, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView, QDesktopWidget  # Import QHeaderView

from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt

from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()

# Add the folder containing db_connection.py to the Python path
from db_connection import establish_db_connection

class Menu(QMainWindow):
    def __init__(self, tab_widget):
        super().__init__()
        
        self.tab_widget = tab_widget  # Store the tab widget
        layout = QVBoxLayout(self)

        self.setWindowTitle("PyQt5 4x4 Grid of Buttons")
        # self.setGeometry(100, 100, 1366, 720)  # Set the window DEFAULT size to 1366x768 pixels

        # Move the window to the second monitor
        # second_screen = QDesktopWidget().screenGeometry(1)
        # self.setGeometry(second_screen.left(), second_screen.top(), 1366, 720)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        central_layout = QVBoxLayout(central_widget)

        grid_layout = QGridLayout()

        # Initialize variables to keep track of the current page and number of items per page
        self.current_page = 1
        self.items_per_page = 20
        self.current_offset = (self.current_page - 1) * self.items_per_page

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
                        pixmap = pixmap.scaledToHeight(128)
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
        
        # Load data into the QTableWidget for the first page
        self.load_data(page=self.current_page)
        
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
                pagination_layout.addWidget(next_button)
                pagination_layout.addWidget(last_button)

                # Connect the buttons to pagination logic
                first_button.clicked.connect(lambda: self.load_data(table_widget=table_widget, custom_offset=0))
                previous_button.clicked.connect(lambda: self.load_data(table_widget=table_widget, custom_offset=max(0, self.current_offset - self.items_per_page)))
                next_button.clicked.connect(lambda: self.load_data(table_widget=table_widget, custom_offset=self.current_offset + self.items_per_page))
                last_button.clicked.connect(lambda: self.load_last_data(table_widget=table_widget))

                new_tab_layout.addLayout(pagination_layout)

                new_tab.setLayout(new_tab_layout)

                # Pass the necessary elements to the load_data method
                self.load_data(table_widget=table_widget)

                    
    def load_data(self, page=1, custom_offset=None, is_locked_filter="All", is_inventory_filter="All", table_widget=None):
        conn, cursor = establish_db_connection()

        if conn and cursor:
            try:
                # Calculate the offset based on the current page or use the provided custom_offset
                offset = (page - 1) * self.items_per_page if custom_offset is None else custom_offset

                # Get the selected filter options

                # Modify the SQL query based on filter options
                query = f'''
                SELECT MI.ItemCode, MI.Barcode, MI.ItemDescription, MU.Unit AS Unit, MI.Category, MS.Supplier AS Supplier, MI.Price, MI.OnhandQuantity, MI.IsInventory, MI.IsLocked
                FROM MstItem AS MI
                LEFT JOIN MstUnit AS MU ON MI.UnitId = MU.Id
                LEFT JOIN MstSupplier AS MS ON MI.DefaultSupplierId = MS.Id
                WHERE (
                    ('{is_locked_filter}' = 'All' OR ('{is_locked_filter}' = 'Locked' AND MI.IsLocked = 1) OR ('{is_locked_filter}' = 'Unlocked' AND MI.IsLocked = 0))
                    AND ('{is_inventory_filter}' = 'All' OR ('{is_inventory_filter}' = 'Inventory' AND MI.IsInventory = 1) OR ('{is_inventory_filter}' = 'Non-Inventory' AND MI.IsInventory = 0))
                )
                ORDER BY MI.ItemDescription ASC
                OFFSET {offset} ROWS FETCH NEXT {self.items_per_page} ROWS ONLY
                '''

                cursor.execute(query)

                # Fetch all rows from the query result
                rows = cursor.fetchall()

                if table_widget is not None:
                    # Set the number of rows and columns for the QTableWidget
                    table_widget.setRowCount(len(rows))
                    table_widget.setColumnCount(12)

                    # Populate the QTableWidget with data
                    for row_num, row_data in enumerate(rows):
                        for col_num, cell_value in enumerate(row_data[:10]):
                            item = QTableWidgetItem(str(cell_value))
                            table_widget.setItem(row_num, col_num + 2, item)

                    # Add checkboxes in columns 10 and 11 based on boolean values in the database
                    for row_num, row_data in enumerate(rows):
                        for col_num in range(10, 12):
                            item = QTableWidgetItem()
                            item.setFlags(item.flags() | 0x0000100)  # Make it editable
                            checkbox_value = bool(row_data[col_num - 2])
                            item.setCheckState(2 if checkbox_value else 0)
                            table_widget.setItem(row_num, col_num, item)

                    # Set each column width to fit the longest values from each row
                    for col_num in range(12):
                        table_widget.resizeColumnToContents(col_num)

                # Check if there are more pages to load
                next_button_enabled = len(rows) == self.items_per_page
                next_button.setEnabled(next_button_enabled)

                # Check if there are previous pages to load
                previous_button_enabled = page > 1
                previous_button.setEnabled(previous_button_enabled)

                # Close the cursor and connection
                cursor.close()
                conn.close()

            except Exception as e:
                print(f"Error: {str(e)}")

    def load_next_data(self):
        try:
            # Increment the current page
            self.current_page += 1
            self.current_offset = (self.current_page - 1) * self.items_per_page  # Update the current_offset

            # Load data for the next page
            self.load_data(page=self.current_page)

        except Exception as e:
            print(f"Error: {str(e)}")

    def load_previous_data(self):
        try:
            # Decrement the current page
            if self.current_page > 1:
                self.current_page -= 1
                self.current_offset = (self.current_page - 1) * self.items_per_page  # Update the current_offset

                # Load data for the previous page
                self.load_data(page=self.current_page)

        except Exception as e:
            print(f"Error: {str(e)}")
            

    def update_data_on_filter_change(self, combo_box1):
        # When combo_box1 value changes, update the data immediately
        selected_option = combo_box1.currentText()
        
        # If you want to use the current value of combo_box1, you can pass it to the load_data function as an argument
        self.current_page = 1  # Reset to the first page
        self.load_data(page=self.current_page, is_inventory_filter=selected_option)
  
                   
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Tabbed Grid of Buttons")
        self.setGeometry(100, 100, 1366, 720)

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
