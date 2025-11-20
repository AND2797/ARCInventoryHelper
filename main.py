import sys
from PyQt6 import QtCore
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QStyle, QWidget, QHBoxLayout, QLabel, QToolButton, QLineEdit, \
    QVBoxLayout, QListWidget, QListWidgetItem, QPushButton
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QRect, QEasingCurve
from utils.loader import load_items
 # TODO:
 # [ ] How to make it more user friendly?
 # [ ] Include images?
 # [ ] Quest details?
 # [ ] Descriptions?
class CustomTitleBar(QWidget):
    def __init__(self  , parent):
        super().__init__(parent)
        self.setFixedHeight(32)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("My App", self)
        layout.addWidget(title)
        layout.addStretch()
        close_btn = QToolButton(self)
        close_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton))
        close_btn.clicked.connect(parent.close)
        layout.addWidget(close_btn)

        self.setStyleSheet("background: #444; color: white;")

class Window(QMainWindow):
    # TODO: Window management
    # - Need to minimise / cross out
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.X11BypassWindowManagerHint
            )

        self.setGeometry(QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight,
            Qt.AlignmentFlag.AlignLeft,
            QSize(500, 1000),
            QApplication.instance().primaryScreen().availableGeometry(),
        ))
        # WA_TranslucentBackground makes it completely transparent?
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(0.6)

        #minimize
        self.topbar = TopBar(self)

        #central widget
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.topbar)
        self.setCentralWidget(self.central_widget)
        self.expanded_height = 1000
        self.minimized_height = self.topbar.height() - 10

        self.search = QLineEdit(self)
        self.search.setPlaceholderText("Search")
        self.layout.addWidget(self.search)

        # search bar
        recyclables = load_items()
        # print(recyclables)
        font = QFont()
        font.setPointSize(16)
        self.search.setFont(font)
        self.list_widget = QListWidget(self)
        self.list_widget.setFont(font)
        for item in recyclables:
            QListWidgetItem(item, self.list_widget)
        self.layout.addWidget(self.list_widget)

        self.search.textChanged.connect(self.filter_list)
        # self.list_widget.addItems(recyclables)
        # self.list_widget.setGeometry(10, 10, 480, 980)
        self.is_minimized = False
        self.anim = None

    def filter_list(self, text: str):
        text = text.strip().lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text not in item.text().lower())

    def toggle_minimize(self):
        geo = self.geometry()
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(100)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        if self.is_minimized:
            self.anim.setEndValue(QRect(geo.x(), geo.y(), geo.width(), self.expanded_height))
        else:
            self.anim.setEndValue(QRect(geo.x(), geo.y(), geo.width(), self.minimized_height))
        self.is_minimized = not self.is_minimized
        self.anim.start()


        # self.searchbar = QLineEdit(self)
        # title_bar = CustomTitleBar(self)
        # central = QWidget()
        # layout = QHBoxLayout(central)
        # layout.addWidget(title_bar)
        # self.setCentralWidget(central)


    # def mousePressEvent(self, event):
    #     QApplication.instance().quit()

class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.min_btn = QPushButton("_")
        self.close_btn = QPushButton("x")
        layout.addWidget(self.min_btn)
        layout.addWidget(self.close_btn)
        self.setFixedHeight(40)
        layout.setContentsMargins(0, 0, 0, 0)
        self.min_btn.clicked.connect(parent.toggle_minimize)
        self.close_btn.clicked.connect(parent.close)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
