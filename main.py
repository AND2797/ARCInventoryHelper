import sys
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QStyle
from PyQt6.QtCore import Qt, QSize

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.X11BypassWindowManagerHint
            )
        self.setGeometry(QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight,
            Qt.AlignmentFlag.AlignCenter,
            QSize(220, 32),
            QApplication.instance().primaryScreen().availableGeometry(),
            ))


    def mousePressEvent(self, event):
        QApplication.instance().quit()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
