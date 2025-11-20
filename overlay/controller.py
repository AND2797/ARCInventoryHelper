from PyQt6.QtCore import QTimer
from utils.loader import load_items

class OverlayController:
    def __init__(self):
        self.items = load_items()
        self.index = 0
        self.overlay = None

    def set_overlay(self, overlay):
        self.overlay = overlay
        # QTimer.singleShot(0, self.set_overlay(overlay))
        self.update_overlay()


    def next_item(self):
        if not self.items:
            return

        self.index = (self.index + 1) % len(self.items)
        self.update_overlay()


    def prev_item(self):
        if not self.items:
            return
        self.index = (self.index - 1) % len(self.items)
        self.update_overlay()


    def reload_items(self):
        self.items = load_items()
        self.index = 0
        self.update_overlay()

    def update_overlay(self):
        if not self.overlay:
            return

        if not self.items:
            self.overlay.update_text("No items loaded")
        else:
            self.overlay.update_text("Recycle:")

