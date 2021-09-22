# hotkeys.py
# A hotkey manager for your device

import os
import displayio
import terminalio
import usb_hid
from adafruit_display_text.label import Label
from adafruit_hid.consumer_control import ConsumerControl
from hotkeys.cheatsheet import Cheatsheet


class Hotkeys(object):
    PROFILES_DIR = "/profiles"

    def __init__(
        self,
        macropad=None,
        keyboard=None,
        keyboard_layout=None,
        mouse=None,
        pixels=None,
        consumer_control=None,
        device_total_keys=12,
        device_keys_per_row=3,
    ):
        self._macropad = macropad
        self._keyboard = keyboard or macropad.keyboard
        self._keyboard_layout = keyboard_layout or macropad.keyboard_layout
        self._mouse = mouse or macropad.mouse
        self._pixels = pixels or macropad.pixels
        self._consumer_control = consumer_control or ConsumerControl(usb_hid.devices)
        self._device_total_keys = device_total_keys
        self._device_keys_per_row = device_keys_per_row
        self._group = displayio.Group()
        self._profiles = []
        self._index = 0
        self._cheatsheets = []
        self._cheatsheet_index = 0
        self._profile_select_mode = False
        self._last_encoder = 0

        # Init label
        self._label = Label(
            terminalio.FONT,
            text="no_profiles_found",
            color=0x000000,
            background_color=0xFFFFFF,
            background_tight=False,
            padding_top=-2,
            padding_bottom=1,
            padding_left=4,
            padding_right=4,
            anchor_point=(0, 0),
            anchored_position=(4, -2),
        )
        self._group.append(self._label)

        # Load profiles
        self._load_profiles()

    # Group hotkeys is rendered to
    @property
    def group(self):
        return self._group

    # Current profile label x position
    @property
    def x(self):
        return self._label.anchored_position[0]

    @x.setter
    def x(self, value):
        self._label.anchored_position = (value, self._label.anchored_position[1])

    # Current profile label y position
    @property
    def y(self):
        return self._label.anchored_position[1]

    @y.setter
    def y(self, value):
        self._label.anchored_position = (self._label.anchored_position[0], value)

    # Active profile
    @property
    def _profile(self):
        if self._profiles:
            return self._profiles[self._index]

    # Active cheatsheet
    @property
    def _cheatsheet(self):
        if self._cheatsheets:
            return self._cheatsheets[self._cheatsheet_index]

    # Update
    # Should be called in main loop
    def update(self, key_event, encoder, encoder_switch_debounced):
        if not self._profile:
            return
        self._handle_keys(key_event)
        self._handle_encoder(encoder, encoder_switch_debounced)

    # Loads all available profiles
    def _load_profiles(self):
        # Load profiles from disk and build cheatsheets
        os.stat(self.PROFILES_DIR)
        files = os.listdir(self.PROFILES_DIR)
        files.sort()
        for filename in files:
            if filename.endswith(".py"):
                try:
                    module = __import__(self.PROFILES_DIR + "/" + filename[:-3])
                    self._profiles.append(module.profile)
                    self._cheatsheets.append(
                        Cheatsheet(
                            profile=module.profile,
                            total_keys=self._device_total_keys,
                            keys_per_row=self._device_keys_per_row,
                        )
                    )
                except:
                    pass
        # Order profiles and cheatsheets
        self._profiles.sort(key=lambda x: x.order)
        self._cheatsheets.sort(key=lambda x: x.profile.order)

        # Init profile if any loaded
        if self._profile:
            self._init_profile()

    # Initializes the current profile
    # Should be called everytime the current profile is changed
    def _init_profile(self):
        self._label.text = self._profile.name
        for i, macro in enumerate(self._profile.macros):
            self._pixels[i] = macro.led

    # Handles key events
    def _handle_keys(self, key_event):
        if not key_event or self._profile_select_mode:
            return

        pressed = key_event.pressed
        released = key_event.released
        key_number = key_event.key_number
        macro = self._profile.macros[key_number]

        # Update pixel if it has changed
        if pressed and not self._pixels[key_number] == macro.led_pressed:
            self._pixels[key_number] = macro.led_pressed
        elif not self._pixels[key_number] == macro.led:
            self._pixels[key_number] = macro.led
        # Start/stop tone
        if pressed and macro.tone:
            self._macropad.start_tone(macro.tone)
        elif released and macro.tone:
            self._macropad.stop_tone()
        # Execute macro
        macro.execute(hotkeys=self, pressed=pressed, released=released)

    # Handles encoder events
    def _handle_encoder(self, encoder, encoder_switch_debounced):
        # Handle encoder turn
        delta = encoder - self._last_encoder
        if delta:
            self._last_encoder = encoder
            # Switch between profiles in profile select mode
            if self._profile_select_mode:
                if delta < 0 and self._cheatsheet_index > 0:
                    self._group.remove(self._cheatsheets[self._cheatsheet_index].group)
                    self._cheatsheet_index -= 1
                    self._group.append(self._cheatsheets[self._cheatsheet_index].group)
                elif delta > 0 and self._cheatsheet_index < len(self._profiles) - 1:
                    self._group.remove(self._cheatsheets[self._cheatsheet_index].group)
                    self._cheatsheet_index += 1
                    self._group.append(self._cheatsheets[self._cheatsheet_index].group)
            # Encoder turn sequence
            else:
                self._profile.encoder_turn.execute_encoder(hotkeys=self, delta=delta)

        # Handle encoder press
        self._profile.encoder_press.execute(
            hotkeys=self,
            pressed=encoder_switch_debounced.pressed,
            released=encoder_switch_debounced.released,
        )
