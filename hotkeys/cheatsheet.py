# cheatsheet.py
# Cheatsheet class
# Cheatsheets allow you to visually see what each
# key is bound to.

import board
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label


class Cheatsheet:
    def __init__(self, profile=None, total_keys=None, keys_per_row=None):
        self._profile = profile
        self._group = displayio.Group()

        width = board.DISPLAY.width
        height = board.DISPLAY.height

        # Init background
        self._group.append(
            Rect(
                0,
                0,
                width - 1,
                height - 1,
                fill=0x000000,
            )
        )

        # Init header
        self._header = displayio.Group()
        self._header.append(Rect(0, 0, width, 12, fill=0xFFFFFF))
        self._header.append(
            Label(
                terminalio.FONT,
                text=profile.name,
                color=0x000000,
                anchored_position=(width // 2, -2),
                anchor_point=(0.5, 0.0),
            )
        )
        self._group.append(self._header)

        # Init lookup table
        self._table = displayio.Group()
        for i in range(total_keys):
            x = i % keys_per_row
            y = i // keys_per_row
            anchored_position_x = (width - 1) * x / 2
            anchored_position_y = height - 1 - (keys_per_row - y) * total_keys
            label = Label(
                terminalio.FONT,
                text=profile.macros[i].name,
                color=0xFFFFFF,
                anchored_position=(anchored_position_x, anchored_position_y),
                anchor_point=(x / 2, 1.0),
            )
            self._table.append(label)
        self._group.append(self._table)

    # Group cheatsheet is renedered to
    @property
    def group(self):
        return self._group

    # Profile
    @property
    def profile(self):
        return self._profile
