import sys
from PyQt6 import QtCore
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QStyle, QWidget, QHBoxLayout, QLabel, QToolButton, QLineEdit, \
    QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QRect, QEasingCurve
from utils.loader import load_items
 # TODO:
 # [ ] JSON file to keep details of item
#       [ ] What quests used for, how many required
#       [ ] Keep or recycle?
#       [ ] Colour coded
# [ ] Fuzzy search by tags?
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
        self.cachedData = load_items()
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
        # Stacked Widget
        # self.stacked_widget = QStackedWidget(self)
        #minimize
        self.topbar = TopBar(self)

        # stacked
        self.view_stack = QStackedWidget(self)

        #central widget
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.topbar)
        self.expanded_height = 1000
        self.minimized_height = self.topbar.height() - 10

        # Search
        self.search = QLineEdit(self)
        self.search.setPlaceholderText("Search")
        self.layout.addWidget(self.search)

        # search bar
        items = self.cachedData
        # print(recyclables)
        font = QFont()
        font.setPointSize(16)
        self.search.setFont(font)
        self.list_widget = QListWidget(self)
        self.list_widget.setFont(font)
        for item in items['Name'].tolist():
            # QListWidgetItem(items.loc[items["Name"] == item], self.list_widget)
            QListWidgetItem(item, self.list_widget)

        self.detail_label = QLabel(self)
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.detail_label.setWordWrap(True)

        self.view_stack.addWidget(self.list_widget)
        self.view_stack.addWidget(self.detail_label)
        # self.layout.addWidget(self.list_widget)
        # self.layout.addWidget(self.detail_label)
        self.layout.addWidget(self.view_stack)
        self.setCentralWidget(self.central_widget)

        self.search.textChanged.connect(self.filter_list_and_check)
        # self.list_widget.addItems(recyclables)
        # self.list_widget.setGeometry(10, 10, 480, 980)
        self.is_minimized = False
        self.anim = None

    def filter_list_and_check(self, text: str):
        """Filters the list, updates the display and triggers the detail view"""
        query = text.strip().lower()
        visible_count = 0
        single_match_item = None

        # text = text.strip().lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item_name = item.text().lower()

            is_match = query in item_name

            item.setHidden(not is_match)

            if is_match:
                visible_count += 1
                single_match_item = item
            print(visible_count)

        if visible_count == 1:
            self.show_item_details(single_match_item, automatic=True)
            self.list_widget.setEnabled(False)
            self.view_stack.setCurrentIndex(1)
        else:
            self.detail_label.setText("")
            self.view_stack.setCurrentIndex(0)
            self.list_widget.clearSelection()
            self.list_widget.setEnabled(True)

    def show_item_details(self, item: QListWidgetItem, automatic: bool = False):
        name = item.text()
        item_row = self.cachedData[self.cachedData["Name"] == name]
        # This function can get called repeatedly as long as the user keeps typing.
        # Reset text everytime to prevent appending
        self.detail_label.setText("")
        for col in item_row:
            new_line = f"\n{col}: {item_row[col].item()}"
            self.detail_label.setText(self.detail_label.text() + f"{new_line}")

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
