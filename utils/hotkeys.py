import keyboard

def register_hotkeys(controller):
    keyboard.add_hotkey("F6", controller.next_item)
    keyboard.add_hotkey("F7", controller.prev_item)
    keyboard.add_hotkey("F8", controller.reload_items)
