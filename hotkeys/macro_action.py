# macro.py
# Macro action classes
# Each macro action subclass represents a different type of action

from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse


# MacroAction base class
class MacroAction(object):
    def __init__(self, *items):
        self._items = items

    # Handle press method
    # Called on press and should be implemented in child classes
    def handle_press(self, *args):
        raise NotImplementedError("handle_press() not implemented")

    # Handle release method
    # Called on release and should be implemented in child classes
    def handle_release(self, *args):
        raise NotImplementedError("handle_release() not implemented")

    # Handle encoder method
    # Called on encoder turn and should be implemented in child classes
    def handle_encoder(self, *args):
        raise NotImplementedError("handle_encoder() not implemented")


# Shortcut macro action
# For keyboard keycodes (although string names
# for keycodes can be used)
class ShortcutAction(MacroAction):
    # Handle press implementation
    def handle_press(self, hotkeys):
        keycodes = self._items_to_keycodes(hotkeys._keyboard_layout)
        hotkeys._keyboard.press(*keycodes)

    # Handle release implementation
    def handle_release(self, hotkeys):
        keycodes = self._items_to_keycodes(hotkeys._keyboard_layout)
        hotkeys._keyboard.release(*keycodes)

    # Gets all shortcut items as an array of keycodes
    def _items_to_keycodes(self, keyboard_layout):
        result = []
        for item in self._items:
            # Just append items that are already keycodes
            if isinstance(item, int):
                result.append(item)
            # If items are strings lookup keycodes by name
            elif isinstance(item, str):
                if hasattr(Keycode, item):
                    result.append(getattr(Keycode, item))
                elif len(item) == 1:
                    result += keyboard_layout.keycodes(item)
        return result


# Text macro action
# For raw text
class TextAction(MacroAction):
    # Handle press implementation
    def handle_press(self, hotkeys):
        for item in self._items:
            hotkeys._keyboard_layout.write(item)

    # Handle release implementation
    def handle_release(self, hotkeys):
        pass


# Mouse macro action
# For mouse control
class MouseAction(MacroAction):
    def __init__(self, click=None, x=0, y=0, wheel=0):
        self._click = click
        self._x = x
        self._y = y
        self._wheel = wheel

    # Handle press implementation
    def handle_press(self, hotkeys):
        if self._click in [Mouse.LEFT_BUTTON, Mouse.RIGHT_BUTTON, Mouse.MIDDLE_BUTTON]:
            hotkeys._mouse.press(self._click)
        if self._x is not 0 or self._y is not 0 or self._wheel is not 0:
            hotkeys._mouse.move(self._x, self._y, self._wheel)

    # Handle release implementation
    def handle_release(self, hotkeys):
        if self._click in [Mouse.LEFT_BUTTON, Mouse.RIGHT_BUTTON, Mouse.MIDDLE_BUTTON]:
            hotkeys._mouse.release(self._click)


# Consumer control macro action
# For consumer control functions
# Only a single item may be passed
class ConsumerControlAction(MacroAction):
    # Handle press implementation
    def handle_press(self, hotkeys):
        code = self._items_to_code()
        hotkeys._consumer_control.press(code)

    # Handle release implementation
    def handle_release(self, hotkeys):
        hotkeys._consumer_control.release()

    # Gets consumer control items as code
    def _items_to_code(self):
        item = self._items[0]
        if isinstance(item, int):
            return item
        elif isinstance(item, str):
            return getattr(ConsumerControlCode, item)


# Tone macro action
# For tones (macropad only)
class ToneAction(MacroAction):
    # Handle press implementation
    def handle_press(self, hotkeys):
        if hotkeys._macropad:
            for item in self._items:
                if isinstance(item, tuple) and len(item) == 2:
                    hotkeys._macropad.play_tone(item[0], item[1])

    # Handle release implementation
    def handle_release(self, hotkeys):
        pass


# Special macro action
# For any custom actions
# Only a single item may be passed
class SpecialAction(MacroAction):
    PROFILE = "PROFILE"

    # Handle press implementation
    def handle_press(self, hotkeys):
        item = self._items[0]
        # Enable profile select mode
        if item == self.PROFILE and not hotkeys._profile_select_mode:
            hotkeys._profile_select_mode = True
            hotkeys._cheatsheet_index = hotkeys._index
            hotkeys._group.append(hotkeys._cheatsheet.group)

    # Handle release implementation
    def handle_release(self, hotkeys):
        item = self._items[0]
        # Disable profile select mode and update profile
        if item == self.PROFILE and hotkeys._profile_select_mode:
            hotkeys._profile_select_mode = False
            hotkeys._group.remove(hotkeys._cheatsheet.group)
            hotkeys._index = hotkeys._cheatsheet_index
            hotkeys._init_profile()


# Encoder macro action
# For encoder specific actions
class EncoderAction(MacroAction):
    MOUSE_WHEEL = "MOUSE_WHEEL"
    VOLUME = "VOLUME"

    # Handle encoder implementation
    def handle_encoder(self, hotkeys, delta):
        for item in self._items:
            # Mouse wheel up and down
            if item == self.MOUSE_WHEEL:
                hotkeys._mouse.move(wheel=delta * -2)
            # Volume increase/decrease
            elif item == self.VOLUME:
                if delta > 0:
                    hotkeys._consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT)
                elif delta < 0:
                    hotkeys._consumer_control.send(ConsumerControlCode.VOLUME_DECREMENT)


# Aliases
S = ShortcutAction
T = TextAction
M = MouseAction
CC = ConsumerControlAction
TN = ToneAction
SP = SpecialAction
E = EncoderAction
