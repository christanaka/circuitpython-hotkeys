# macro_profile.py
# Macro profile class
# Profiles are made up of a collection of macros, usually
# related in the context of the profile.

from hotkeys.macro import Macro
from hotkeys.macro_action import SP, E


class MacroProfile(object):
    def __init__(
        self,
        name,
        encoder_turn=Macro("MWHEEL", [E("MOUSE_WHEEL")]),
        encoder_press=Macro("PROF", [SP("PROFILE")]),
        macros=[],
        order=99,
    ):
        self._name = name
        self.order = order
        self._encoder_turn = encoder_turn
        self._encoder_press = encoder_press
        self._macros = macros

    # Profile name
    @property
    def name(self):
        return self._name

    # Encoder turn macro
    @property
    def encoder_turn(self):
        return self._encoder_turn

    # Encoder press
    @property
    def encoder_press(self):
        return self._encoder_press

    # Key macros
    @property
    def macros(self):
        return self._macros
