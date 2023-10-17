import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtCore import Qt

class FirstWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Window on Screen 1")
        self.setGeometry(0, 0, 1366, 700)
        self.adjustForTaskbar(0)

    def adjustForTaskbar(self, screen_index):
        screen = QDesktopWidget().screenGeometry(screen_index)
        desktop = QDesktopWidget().availableGeometry(screen_index)

class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.setWindowTitle("Window on Screen 2")
        self.setGeometry(0, 0, 1366, 700)
        self.adjustForTaskbar(1)

        # Remove and disable minimize and close buttons
        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        # self.setEnabled(False)  # Disable the entire window

    def adjustForTaskbar(self, screen_index):
        screen = QDesktopWidget().screenGeometry(screen_index)
        desktop = QDesktopWidget().availableGeometry(screen_index)
        taskbar_height = screen.height() - desktop.height()
        self.move(screen.x(), screen.y() + taskbar_height)

def main():
    app = QApplication(sys.argv)

    if QDesktopWidget().screenCount() >= 2:
        # Create the first window on the primary screen
        window1 = FirstWindow()
        window1.show()

        # Create the second window on the secondary screen
        window2 = SecondWindow()
        window2.show()

        sys.exit(app.exec_())
    else:
        print("Two screens are required to run this application.")

if __name__ == '__main__':
    main()