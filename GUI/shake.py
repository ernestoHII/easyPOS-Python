from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from PyQt5.QtCore import QTimer, QPoint

class ShakeExample(QWidget):
    def __init__(self):
        super().__init__()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.perform_shake)
        
        self.init_ui()

    def init_ui(self):
        btn = QPushButton("Shake", self)
        btn.clicked.connect(self.init_shake)
        layout = QVBoxLayout()
        layout.addWidget(btn)
        self.setLayout(layout)
        self.setGeometry(100, 100, 200, 100)

    def init_shake(self):
        if not self.timer.isActive():
            self.start_pos = self.pos()
            self.shake_step = 0
            self.shake_max = 10
            self.timer.start(20)  # 20ms intervals

    def perform_shake(self):
        shake_positions = [QPoint(self.shake_max, 0), QPoint(-self.shake_max, 0), QPoint(0, self.shake_max), QPoint(0, -self.shake_max)]
        self.move(self.start_pos + shake_positions[self.shake_step % 4])
        self.shake_step += 1
        if self.shake_step > self.shake_max * 2:  # shake for a fixed number of times
            self.timer.stop()
            self.move(self.start_pos)

if __name__ == '__main__':
    app = QApplication([])
    window = ShakeExample()
    window.show()
    app.exec_()
