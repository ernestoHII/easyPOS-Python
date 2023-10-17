import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QProgressBar, QCheckBox, QPrintDialog
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtCore import QTimer

class POSReceipt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.printer = QPrinter(QPrinter.HighResolution)
        self.timer = QTimer(self)  # Define the timer here
        self.fake_printer = True  # Default to using a fake printer

    def initUI(self):
        self.setWindowTitle("POS Receipt")
        self.setGeometry(100, 100, 400, 600)

        layout = QVBoxLayout()

        self.receiptView = QTextEdit(self)
        self.receiptView.setText(self.generateReceipt())
        layout.addWidget(self.receiptView)

        self.printButton = QPushButton("Print Receipt", self)
        self.printButton.clicked.connect(self.printReceipt)
        layout.addWidget(self.printButton)

        # Add progress bar for printing animation
        self.printProgressBar = QProgressBar(self)
        self.printProgressBar.setMaximum(100)
        self.printProgressBar.setValue(0)
        layout.addWidget(self.printProgressBar)

        # Add a checkbox for choosing between fake and real printers
        self.printerCheckBox = QCheckBox("Use Fake Printer", self)
        self.printerCheckBox.setChecked(True)
        self.printerCheckBox.stateChanged.connect(self.toggleFakePrinter)
        layout.addWidget(self.printerCheckBox)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def generateReceipt(self):
        # Example receipt content. 
        receipt_content = """
        ---------------RECEIPT---------------
        Product 1:     $10
        Product 2:     $20
        ------------------------------------
        Total:         $30
        ------------------------------------
        Thank you for your purchase!
        ------------------------------------
        """
        return receipt_content

    def toggleFakePrinter(self):
        # Toggle between fake and real printer based on the checkbox state
        self.fake_printer = self.printerCheckBox.isChecked()

    def printReceipt(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.printProgressBar.setValue(0)
            if self.fake_printer:
                self.timer.start(50)  # Simulate printing with the fake printer
            else:
                self.printProgressBar.setValue(100)
                self.receiptView.print_(self.printer)  # Use the real printer


    def simulatePrinting(self, printer):
        # Reset progress bar
        self.printProgressBar.setValue(0)

        # Create a QTimer to simulate printing progress
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start(50)  # Update every 50ms

    def updateProgressBar(self):
        currentValue = self.printProgressBar.value()
        if currentValue >= 100:
            self.timer.stop()
            self.printProgressBar.setValue(100)
            self.receiptView.print_(self.printer)  # Use the member variable
        else:
            self.printProgressBar.setValue(currentValue + 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = POSReceipt()
    window.show()
    sys.exit(app.exec_())
