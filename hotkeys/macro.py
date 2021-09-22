# macro.py
# Macro class
# Each macro consists of an automated input sequence

from hotkeys.macro_action import MacroAction


class Macro(object):
    def __init__(self, name="", sequence=[], led=0, led_pressed=0, tone=None):
        self._name = name
        self._sequence = sequence
        self._led = led
        self._led_pressed = led_pressed
        self._tone = tone

    # Name
    @property
    def name(self):
        return self._name

    # Sequence of macros
    @property
    def sequence(self):
        return self._sequence

    # Key LED
    @property
    def led(self):
        return self._led

    # Key LED when pressed
    @property
    def led_pressed(self):
        return self._led_pressed

    # Tone when pressed
    @property
    def tone(self):
        return self._tone

    # Executes sequence
    def execute(self, hotkeys, pressed, released):
        if not self._sequence:
            return
        if pressed:
            for item in self._sequence:
                if isinstance(item, MacroAction):
                    item.handle_press(hotkeys)
        if released:
            for item in self._sequence:
                if isinstance(item, MacroAction):
                    item.handle_release(hotkeys)

    # Executes encoder sequence
    def execute_encoder(self, hotkeys, delta):
        if not self._sequence or delta is 0:
            return
        for item in self._sequence:
            item.handle_encoder(hotkeys, delta)
