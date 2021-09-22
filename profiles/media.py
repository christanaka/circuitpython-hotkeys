# media.py
# Media profile

from hotkeys.macro import Macro
from hotkeys.macro_action import CC, E
from hotkeys.macro_profile import MacroProfile


profile = MacroProfile(
    name="media",
    order=2,
    encoder_turn=Macro("VOL", [E("VOLUME")]),
    macros=[
        # 1st row
        Macro("PLAY", [CC("PLAY_PAUSE")]),
        Macro("PREV", [CC("SCAN_PREVIOUS_TRACK")]),
        Macro("NEXT", [CC("SCAN_NEXT_TRACK")]),
        # 2nd row
        Macro(),
        Macro(),
        Macro(),
        # 3rd row
        Macro(),
        Macro(),
        Macro(),
        # 4th row
        Macro(),
        Macro(),
        Macro(),
    ],
)
