# test.py
# Test profile

from hotkeys.macro import Macro
from hotkeys.macro_profile import MacroProfile

profile = MacroProfile(
    name="test_mode",
    order=5,
    macros=[
        # 1st row
        Macro("KEY_1", led_pressed=0xFFFFFF, tone=196),
        Macro("KEY_2", led_pressed=0xFFFFFF, tone=220),
        Macro("KEY_3", led_pressed=0xFFFFFF, tone=246),
        # 2nd row
        Macro("KEY_4", led_pressed=0xFFFFFF, tone=262),
        Macro("KEY_5", led_pressed=0xFFFFFF, tone=294),
        Macro("KEY_6", led_pressed=0xFFFFFF, tone=330),
        # 3rd row
        Macro("KEY_7", led_pressed=0xFFFFFF, tone=349),
        Macro("KEY_8", led_pressed=0xFFFFFF, tone=392),
        Macro("KEY_9", led_pressed=0xFFFFFF, tone=440),
        # 4th row
        Macro("KEY_10", led_pressed=0xFFFFFF, tone=494),
        Macro("KEY_11", led_pressed=0xFFFFFF, tone=523),
        Macro("KEY_12", led_pressed=0xFFFFFF, tone=587),
    ],
)
