# mouse.py
# Mouse profile

from adafruit_hid.mouse import Mouse
from hotkeys.macro import Macro
from hotkeys.macro_action import M
from hotkeys.macro_profile import MacroProfile


profile = MacroProfile(
    name="mouse",
    order=4,
    macros=[
        # 1st row
        Macro("LCLIK", [M(click=Mouse.LEFT_BUTTON)]),
        Macro("RCLIK", [M(click=Mouse.RIGHT_BUTTON)]),
        Macro("MCLIK", [M(click=Mouse.MIDDLE_BUTTON)]),
        # 2nd row
        Macro("W-", [M(wheel=2)]),
        Macro("UP", [M(y=-10)]),
        Macro("W+", [M(wheel=-2)]),
        # 3rd row
        Macro("LEFT", [M(x=-10)]),
        Macro(),
        Macro("RIGHT", [M(x=10)]),
        # 4th row
        Macro(),
        Macro("DOWN", [M(y=10)]),
        Macro(),
    ],
)
