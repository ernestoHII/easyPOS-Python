import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import requests
from PyQt5.QtGui import QDoubleValidator, QColor, QDoubleValidator, QValidator
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.product_name = QLineEdit(self)
        self.product_price = QLineEdit(self)
        validator = QDoubleValidator(0, 1000000, 2)  # range from 0 to 1,000,000 with 2 decimal places
        self.product_price.setValidator(validator)
        self.product_price.textChanged.connect(self.check_price_input)


        add_product_button = QPushButton("Add Product", self)
        add_product_button.clicked.connect(self.add_product)

        layout.addWidget(QLabel("Product Name:"))
        layout.addWidget(self.product_name)
        layout.addWidget(QLabel("Product Price:"))
        layout.addWidget(self.product_price)
        layout.addWidget(add_product_button)

        self.central_widget.setLayout(layout)

    def check_price_input(self):
        state = self.product_price.validator().validate(self.product_price.text(), 0)[0]
        if state == QValidator.Acceptable:
            color = '#c4df9b'  # green
        elif state == QValidator.Intermediate:
            color = '#fff79a'  # yellow
        else:
            color = '#f6989d'  # red
        self.product_price.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def add_product(self):
        product_name = self.product_name.text()
        
        try:
            product_price = float(self.product_price.text())
        except ValueError:
            print("Invalid product price entered!")
            return
        
        payload = {"name": product_name, "price": product_price}
        try:
            response = requests.post("http://localhost:8000/create-product/", json=payload)
            response.raise_for_status()  # Raise an exception for bad responses (4xx, 5xx)
            if response.status_code == 200:
                self.product_name.clear()
                self.product_price.clear()
                print("Product added successfully")
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
