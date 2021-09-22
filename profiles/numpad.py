# numpad.py
# Numpad profile

from adafruit_hid.keycode import Keycode
from hotkeys.macro import Macro
from hotkeys.macro_action import S
from hotkeys.macro_profile import MacroProfile


profile = MacroProfile(
    name="numpad",
    order=1,
    macros=[
        # 1st row
        Macro("ENTER", [S(Keycode.KEYPAD_ENTER)]),
        Macro("NUM_0", [S(Keycode.KEYPAD_ZERO)]),
        Macro("NLOCK", [S(Keycode.KEYPAD_NUMLOCK)]),
        # 2nd row
        Macro("NUM_7", [S(Keycode.KEYPAD_SEVEN)]),
        Macro("NUM_8", [S(Keycode.KEYPAD_EIGHT)]),
        Macro("NUM_9", [S(Keycode.KEYPAD_NINE)]),
        # 3rd row
        Macro("NUM_4", [S(Keycode.KEYPAD_FOUR)]),
        Macro("NUM_5", [S(Keycode.KEYPAD_FIVE)]),
        Macro("NUM_6", [S(Keycode.KEYPAD_SIX)]),
        # 4th row
        Macro("NUM_1", [S(Keycode.KEYPAD_ONE)]),
        Macro("NUM_2", [S(Keycode.KEYPAD_TWO)]),
        Macro("NUM_3", [S(Keycode.KEYPAD_THREE)]),
    ],
)
