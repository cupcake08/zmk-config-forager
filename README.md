# Forager ZMK config

ZMK firmware for my [Forager](https://github.com/carrefinho/forager), forked from
[carrefinho/forager-zmk-module](https://github.com/carrefinho/forager-zmk-module).

- ZMK `main` from October 2026 (Zephyr 4.1), pinned by commit in `config/west.yml`
  and `.github/workflows/build.yml`. The board is now `xiao_ble//zmk`.
- Plain Colemak through the macOS Colemak input source: the keyboard sends QWERTY
  codes and macOS maps them, so keep the Mac on Colemak. `config/mac_colemak.h`
  maps each letter to the code that types it.
- Keymap tuned for AI agents in the terminal and the browser: `config/forager.keymap`.

## Layers

| Layer | How | What |
| --- | --- | --- |
| Base | — | Colemak, `'` top right, home-row ⌃ ⌥ ⌘ on R S T / N E I |
| Caps | tap left inner thumb twice | caps word; Space, Enter or the shift thumb ends it |
| Nav | hold Space | arrows, line/word jumps, page, scroll, clicks, held mods |
| Sym | hold Enter | digits, shifted digits, ``` ` ``` ``` `` ` `` ``` code fence, `: ; ~ - = [ ] \` |
| AI | hold Backspace | tabs, clipboard, ⌘Tab switcher, agent keys (Esc, ⇧Tab, ⌃C, ⌃V image, Esc Esc, ⌃R, ⇧⏎, ⌘⏎), dictation |
| Fn | hold Backspace + Space | Bluetooth, media, brightness, Mission Control, power, reset, bootloader |

Combos: W+F Esc, F+P Tab, Z+X cut, X+C copy, C+V paste, `,`+`.` `;`, `.`+`/` `:`.

App switcher: hold the AI thumb, tap T to step forward (S steps back), release
the thumb to switch.

Dictation key: set System Settings › Keyboard › Dictation › Shortcut to
"Press Right Command Key Twice".

## Power

There is no power switch or reachable reset button, so:

- **Off:** hold Backspace + Space thumbs and hold B for 1 s. Both halves switch off.
- **On:** press the inner thumb key on each half.
- **Sleep:** each half sleeps after 30 min idle; any key wakes it.
- **Reset / bootloader:** Fn layer, hold 1 s. Left half: Z bootloader, X reset.
  Right half: `/` bootloader, `.` reset.

## Flashing

GitHub Actions builds `forager_left`, `forager_right` and `settings_reset` on every
push. Put a half in bootloader mode (Fn key above, or double-tap reset) and copy the
matching `.uf2` onto the `XIAO-SENSE` / `XIAO-BLE` drive.

ZMK Studio works over USB on the left half; it shows QWERTY key labels because of
the Colemak mapping above.
