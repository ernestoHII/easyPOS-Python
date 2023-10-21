import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton, QFrame, QLineEdit
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect

class RGBKeyboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Remove title bar and stay on top
        self.setGeometry(QRect(0, QApplication.desktop().screenGeometry().height(), QApplication.desktop().screenGeometry().width(), 300))  # Initial position
        
        # Create main layout
        layout = QVBoxLayout()

        # Create frame to resemble a real keyboard
        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frameLayout = QVBoxLayout(frame)

        # Create an input box to display the clicked values
        self.inputBox = QLineEdit(self)
        self.inputBox.setFont(QFont("Arial", 18, QFont.Bold))  # Set the font size to 18 and bold
        layout.addWidget(self.inputBox)

        # Characters to be displayed on the buttons in QWERTY arrangement with corresponding Japanese characters
        rows = [
            list(zip('1234567890', '一二三四五六七八九零')),  # Using Kanji values for numbers
            list(zip('QWERTYUIOP', 'たていすかんなにらせ')),
            list(zip('ASDFGHJKL', 'ちとしはきくまのりれ')),
            list(zip('ZXCVBNM', 'つさそひこみも')),
            list(zip([',', '.', '/', 'DEL'], ['、', '。', '/', '削除']))
        ]

        # Create buttons and add them to the frame's layout
        for row in rows:
            h_layout = QHBoxLayout()
            for char, jp_char in row:
                btn = QPushButton(f"{char}\n{jp_char}")
                btn.setFont(QFont("Arial", 14, QFont.Bold))
                btn.setStyleSheet("color: black")
                btn.clicked.connect(self.appendCharacter)
                h_layout.addWidget(btn)
            frameLayout.addLayout(h_layout)

        # Add the space and enter button on the same row
        h_layout = QHBoxLayout()
        spaceBtn = QPushButton(' \n　')  # Space character and its Japanese equivalent
        spaceBtn.setFont(QFont("Arial", 14, QFont.Bold))
        spaceBtn.setStyleSheet("color: black")
        spaceBtn.clicked.connect(self.appendCharacter)
        h_layout.addWidget(spaceBtn, 5)  # Stretch factor of 5 to make it stretch more

        enterBtn = QPushButton('ENTER\nエンター')
        enterBtn.setFont(QFont("Arial", 14, QFont.Bold))
        enterBtn.setStyleSheet("color: black")
        enterBtn.clicked.connect(self.captureAndClose)
        h_layout.addWidget(enterBtn)

        frameLayout.addLayout(h_layout)
        layout.addWidget(frame)

        self.setLayout(layout)
    
        # Set window properties
        self.setWindowTitle('RGB Keyboard')
        self.show()

        # Create the slide animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)  # Duration in milliseconds
        self.animation.setStartValue(QRect(0, QApplication.desktop().screenGeometry().height(), QApplication.desktop().screenGeometry().width(), 300))
        self.animation.setEndValue(QRect(0, QApplication.desktop().screenGeometry().height() - 300, QApplication.desktop().screenGeometry().width(), 300))
        self.animation.start()       

    def appendCharacter(self):
        char = self.sender().text().split("\n")[0]  # Only capture the English character
        if char == "Delete":
            self.inputBox.setText(self.inputBox.text()[:-1])  # Remove the last character
        else:
            currentText = self.inputBox.text()
            self.inputBox.setText(currentText + char)

    def captureAndClose(self):
        # Placeholder for capturing the input. Currently, it just prints to the console.
        print(self.inputBox.text())
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RGBKeyboard()
    sys.exit(app.exec_())
