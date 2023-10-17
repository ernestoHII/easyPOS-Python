import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_widget = QTableWidget()
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_button = QPushButton("Load Headers")
        self.load_button.clicked.connect(self.load_table_headers)
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.load_button)
        self.next_button = QPushButton("Next")
        self.prev_button = QPushButton("Previous")
        self.next_button.clicked.connect(self.load_next_page)
        self.prev_button.clicked.connect(self.load_prev_page)
        # Add to layout
        layout.addWidget(self.prev_button)
        layout.addWidget(self.next_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.resize(600, 400)
        self.current_page = 0
        self.rows_per_page = 10

    def load_table_headers(self, increment_page=0):
        self.current_page += increment_page        
        table_name = "MstItem"  # Replace with the desired table name
        # Column Names:
        # 0. Id, 1. ItemCode, 2. BarCode, 3. ItemDescription, 4. Alias, 5. GenericName, 6. Category, 
        # 7. SalesAccountId, 8. AssetAccountId, 9. CostAccountId, 10. InTaxId, 11. OutTaxId, 
        # 12. UnitId, 13. DefaultSupplierId, 14. Cost, 15. MarkUp, 16. Price, 17. ImagePath, 
        # 18. ReorderQuantity, 19. OnhandQuantity, 20. IsInventory, 21. ExpiryDate, 22. LotNumber, 
        # 23. Remarks, 24. EntryUserId, 25. EntryDateTime, 26. UpdateUserId, 27. UpdateDateTime, 
        # 28. IsLocked, 29. DefaultKitchenReport, 30. IsPackage, 31. cValue, 32. ChildItemId, 
        # 33. IsMonitored, 34. IsStickerPrinted
        desired_indices = [2, 3, 13, 6, 14, 16, 19, 20, 28]
        indices_param = "&".join([f"column_indices={i}" for i in desired_indices])
        response = requests.get(f"http://localhost:8000/table-data/{table_name}?{indices_param}&skip={self.current_page * self.rows_per_page}&limit={self.rows_per_page}")
        if response.status_code == 200:
            headers = response.json().get("headers", [])
            data = response.json().get("data", [])
            
            # Load headers
            headers = ["", ""] + headers
            self.table_widget.setColumnCount(len(headers))
            self.table_widget.setHorizontalHeaderLabels(headers)

            # Load data
            self.table_widget.setRowCount(len(data))
            for row_index, row_data in enumerate(data):
                for col_index, cell_data in enumerate(row_data):
                    self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))

        else:
            print(f"Error getting data for table {table_name}: {response.text}")

        # Check if more data is available
        if response.status_code == 200:
            has_more = response.json().get("has_more", True) # Default to True if not present
            self.next_button.setEnabled(has_more)
        
    def load_next_page(self):
        self.load_table_headers(increment_page=1)

    def load_prev_page(self):
        if self.current_page > 0:  # Avoid going into negative pages
            self.load_table_headers(increment_page=-1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
