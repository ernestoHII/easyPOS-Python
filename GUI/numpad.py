import sys
import ast

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QGridLayout, 
                             QWidget, QDesktopWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QLineEdit)
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QFont

class NumpadWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the main widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Create the input box
        self.input_box = QLineEdit(self)
        self.input_box.setAlignment(Qt.AlignRight)  # Align the text to the right, typical for calculators

        # Increase font size by 50%
        font = self.input_box.font()      # Get current font
        current_size = font.pointSize()   # Get current size
        font.setPointSize(round(current_size * 1.50))  # Increase size by 50% and round to nearest integer
        self.input_box.setFont(font)     # Set the modified font
        # Increase the height of the input box by 50%
        current_height = self.input_box.height()
        new_height = int(current_height * 2)
        self.input_box.setStyleSheet(f"QLineEdit {{height: {new_height}px;}}")
        # Create a main horizontal layout
        main_layout = QHBoxLayout(self.main_widget)

        # Create a grid layout
        layout = QGridLayout()
        
        # Adjust grid layout properties
        layout.setSpacing(5)  # Spacing between buttons
        layout.setContentsMargins(10, 10, 10, 10)  # Margins around the layout
        
        # Add the input box to the layout
        layout.addWidget(self.input_box, 0, 0, 1, 4)  # Spanning 4 columns

        # Create numpad buttons
        buttons = [
            ('Del', 1, 1), ('/', 1, 1), ('*', 1, 1), ('-', 1, 1),
            ('7', 1, 1), ('8', 1, 1), ('9', 1, 1), ('+', 2, 1),
            ('4', 1, 1), ('5', 1, 1), ('6', 1, 1),
            ('1', 1, 1), ('2', 1, 1), ('3', 1, 1), ('Enter', 2, 2),
            ('0', 1, 2), ('.', 1, 1)
        ]

        positions = [
            (1, 0), (1, 1), (1, 2), (1, 3),
            (2, 0), (2, 1), (2, 2), (2, 3),
            (3, 0), (3, 1), (3, 2),
            (4, 0), (4, 1), (4, 2), (4, 3),
            (5, 0), (5, 2)
        ]

        for position, (button_text, rowspan, colspan) in zip(positions, buttons):
            button = QPushButton(button_text)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.clicked.connect(self.on_button_clicked)  # Connect button click to a slot
            layout.addWidget(button, position[0], position[1], rowspan, colspan)

        # Add grid layout to main layout
        main_layout.addStretch()  # This will push the grid to the center horizontally
        main_layout.addLayout(layout)
        main_layout.addStretch()  # This will push the grid to the center horizontally

        # Set the main widget's layout
        self.main_widget.setLayout(main_layout)

        # Get the available screen height excluding the taskbar
        available_screen_height = QApplication.desktop().availableGeometry().height()

        # Create the slide animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)  # Duration in milliseconds
        self.animation.setStartValue(QRect(0, available_screen_height, QApplication.desktop().screenGeometry().width(), 500))
        self.animation.setEndValue(QRect(0, available_screen_height - 500, QApplication.desktop().screenGeometry().width(), 500))
        self.animation.start()

    def on_button_clicked(self):
        sender = self.sender()
        if sender.text() == 'Del':
            current_text = self.input_box.text()            
            new_text = current_text[:-1]                    
            self.input_box.setText(new_text)                
        elif sender.text() == 'Enter':
            expression = self.input_box.text()
            try:
                # Safely evaluate the mathematical expression
                result = ast.literal_eval(expression)
                self.input_box.setText(str(result))
            except (ValueError, SyntaxError):
                # Handle invalid expression
                self.input_box.setText("Error")
        else:
            self.input_box.insert(sender.text())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NumpadWindow()
    window.show()
    sys.exit(app.exec_())
