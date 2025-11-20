from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPaintEvent


class OverlayWindow(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.text = "Loading..."

        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool
            # QtCore.Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(300, 200)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QColor(255, 255, 255, 220))
        painter.setFont(QtGui.QFont("Arial", 14))
        painter.drawText(10, 25, self.text)

    def update_text(self, text):
        self.text = text
        self.update()
