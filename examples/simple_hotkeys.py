import displayio
from adafruit_macropad import MacroPad
from hotkeys.hotkeys import Hotkeys


macropad = MacroPad()
hotkeys = Hotkeys(macropad)

group = displayio.Group()
group.append(hotkeys.group)
macropad.display.show(group)

# Main loop
while True:
    key_event = macropad.keys.events.get()
    macropad.encoder_switch_debounced.update()
    hotkeys.update(key_event, macropad.encoder,
                   macropad.encoder_switch_debounced)
