# emotes.py
# Emotes profile

from hotkeys.macro import Macro
from hotkeys.macro_action import T
from hotkeys.macro_profile import MacroProfile


profile = MacroProfile(
    name="emotes",
    order=3,
    macros=[
        # 1st row
        Macro("<3", [T("<3")]),
        Macro("LUL", [T("LUL")]),
        Macro("Kappa", [T("Kappa")]),
        # 2nd row
        Macro("PepeL", [T("PepeLaugh")]),
        Macro("MonkS", [T("MonkaS")]),
        Macro("MonkW", [T("MonkaW")]),
        # 3rd row
        Macro("Jbait", [T("Jebaited")]),
        Macro("4Head", [T("4Head")]),
        Macro("4Wrd", [T("4Weird")]),
        # 4th row
        Macro("PogC", [T("PogChamp")]),
        Macro("PogO", [T("PogO")]),
        Macro("PogU", [T("PogU")]),
    ],
)
