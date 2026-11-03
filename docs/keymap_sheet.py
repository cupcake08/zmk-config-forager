"""Render the Forager keymap as a one-page A4 landscape colour cheat sheet.

python3 docs/keymap_sheet.py  ->  docs/forager_keymap_a4.html (print it, or
let Chrome headless turn it into the PDF next to it).
"""
import math
from html import escape
from pathlib import Path

U = 0.095  # mm per physical-layout unit (100 units = one key)

# Physical layout from boards/shields/forager/forager.dtsi: x, y, rot, rx, ry
COL_X = [0, 100, 200, 300, 400, 750, 850, 950, 1050, 1150]
COL_Y = [61, 28, 0, 17, 28, 28, 17, 0, 28, 61]
THUMBS = [(400, 350, 25, 450, 400), (500, 370, 25, 450, 400),
          (650, 370, -25, 800, 400), (750, 350, -25, 800, 400)]

# kind: ag agent, br browser, md modifier, dn power/firmware, hd held, ly layer key
LAYERS = [
    ("Base", "plain Colemak", "base", [
        ["Q", "W", "F", "P", "G", "J", "L", "U", "Y", ("*", "test key")],
        ["A", ("R", "⌃ hold", "md"), ("S", "⌥ hold", "md"), ("T", "⌘ hold", "md"), "D",
         "H", ("N", "⌘ hold", "md"), ("E", "⌥ hold", "md"), ("I", "⌃ hold", "md"), "O"],
        [("Z", "⇧ hold", "md"), "X", "C", "V", "B", "K", "M", (",", "<"), (".", ">"), ("/", "⇧ hold", "md")],
        [("*", "test key"), ("⇧", "hold AI", "ly-ai"), ("Space", "hold Nav", "ly-nav"), ("⏎", "hold Sym", "ly-sym")],
    ]),
    ("AI", "hold ⇧ thumb", "ai", [
        [("⌘W", "close tab", "br"), ("⌘⇧[", "prev tab", "br"), ("⌘⇧]", "next tab", "br"), ("⌘T", "new tab", "br"), ("⌘⇧T", "reopen", "br"),
         ("⌘[", "back", "br"), ("⌘]", "forward", "br"), ("↑", "last prompt", "ag"), ("⌘⇧Z", "redo"), None],
        [("⌘A", "select all"), ("Esc", "stop agent", "ag"), ("⇧Tab", "mode / app ←", "ag"), ("⌘Tab", "app →", "ag"), ("⌘`", "window"),
         ("⌃C", "cancel", "ag"), ("⌘⏎", "send", "ag"), ("↓", "next prompt", "ag"), ("⌃V", "paste image", "ag"), ("⌘K", "palette")],
        [("⌘Z", "undo"), ("⌘X", "cut"), ("⌘C", "copy"), ("⌘V", "paste"), ("⌘⌃⇧4", "snip", "ag"),
         ("Esc Esc", "rewind", "ag"), ("⌃R", "history", "ag"), ("⇧⏎", "newline", "ag"), ("⌘Space", "launcher"), ("Dictate", "voice", "ag")],
        [None, ("", "held", "hd"), ("Space", "hold: Fn", "ly-fn"), ("⌘⌫", "delete line")],
    ]),
    ("Nav", "hold Space thumb", "nav", [
        [("Esc",), ("⌘[", "back", "br"), ("Scroll", "up", "br"), ("⌘]", "forward", "br"), ("⌘R", "reload", "br"),
         ("PgUp",), ("⌘←", "line start"), ("↑",), ("⌘→", "line end"), None],
        [("⇧", "", "md"), ("⌃", "", "md"), ("⌥", "", "md"), ("⌘", "", "md"), None,
         ("PgDn",), ("←",), ("↓",), ("→",), ("⏎",)],
        [None, ("Click", "left"), ("Scroll", "down", "br"), ("Click", "right"), None,
         ("⌘↑", "top"), ("⌥←", "word"), ("⌘↓", "bottom"), ("⌥→", "word"), ("Del",)],
        [None, ("⇧", "hold: Fn", "ly-fn"), ("", "held", "hd"), None],
    ]),
    ("Sym", "hold ⏎ thumb", "sym", [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", None],
        ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"],
        ["`", ("```", "code block"), "_", "|", "~", "-", "=", "[", "]", "\\"],
        [None, ("0", ""), None, ("", "held", "hd")],
    ]),
    ("Fn", "hold ⇧ + Space", "fn", [
        [("BT 1",), ("BT 2",), ("BT 3",), ("BT 4",), ("BT 5",), ("⏮",), ("⏯",), ("⏭",), ("Mute",), None],
        [("BT clear", "1 s", "dn"), ("USB/BT", "1 s", "dn"), ("Battery", "LED"), ("Link", "LED"), ("Studio", "unlock"),
         ("Bright −",), ("Vol −",), ("Vol +",), ("Bright +",), ("Mission", "Control")],
        [("Boot", "left · 1 s", "dn"), ("Reset", "left · 1 s", "dn"), None, ("Lock", "⌃⌘Q"), ("Power off", "both · 1 s", "dn"),
         ("⌘⇧5", "screenshot"), ("⌃←", "space"), ("⌃→", "space"), ("Reset", "right · 1 s", "dn"), ("Boot", "right · 1 s", "dn")],
        [None, ("", "held", "hd"), ("", "held", "hd"), None],
    ]),
]


def norm(k):
    if k is None:
        return None
    if isinstance(k, str):
        k = (k,)
    return (k + ("", ""))[:3]


def key_html(k, cx, cy, rot=0):
    s = 100 * U - 0.9
    style = (f"left:{cx * U - s / 2:.2f}mm;top:{cy * U - s / 2:.2f}mm;"
             f"width:{s:.2f}mm;height:{s:.2f}mm;transform:rotate({rot}deg)")
    if k is None:
        return f'<div class="k empty" style="{style}"></div>'
    main, sub, kind = norm(k)
    small = " small" if len(main) > 4 or sum(ch in "⌘⌃⌥⇧" for ch in main) >= 3 else ""
    return (f'<div class="k {kind}" style="{style}"><span class="m{small}">{escape(main)}</span>'
            + (f'<span class="s">{escape(sub)}</span>' if sub else "") + "</div>")


def board(rows):
    out = []
    for r, row in enumerate(rows[:3]):
        for c, k in enumerate(row):
            out.append(key_html(k, COL_X[c] + 50, COL_Y[c] + r * 100 + 50))
    for k, (x, y, rot, rx, ry) in zip(rows[3], THUMBS):
        a = math.radians(rot)
        dx, dy = x + 50 - rx, y + 50 - ry
        cx = rx + dx * math.cos(a) - dy * math.sin(a)
        cy = ry + dx * math.sin(a) + dy * math.cos(a)
        out.append(key_html(k, cx, cy, rot))
    return "".join(out)


def card(name, how, cls, rows):
    return (f'<section class="card {cls}"><div class="title"><b>{name}</b><span>{escape(how)}</span></div>'
            f'<div class="board">{board(rows)}</div></section>')


INFO = """
<section class="card info">
  <h3>Combos <span>press together, on Base</span></h3>
  <div class="combos">
    <div><b>W + F</b> Esc</div><div><b>F + P</b> Tab</div><div><b>Z + X</b> ⌘X cut</div>
    <div><b>X + C</b> ⌘C copy</div><div><b>C + V</b> ⌘V paste</div><div><b>, + .</b> ; semicolon</div>
    <div><b>. + /</b> : colon</div><div><b>U + Y</b> ' (hold Z: ")</div><div><b>L + U</b> ⌫ (hold Z: word)</div><div><b>⇧ ⇧</b> caps word</div>
  </div>
  <h3>Power <span>no switch: sleep is automatic, off is a key</span></h3>
  <table>
    <tr><td><span class="pill">15 min idle</span></td><td>Each half sleeps by itself. Any key wakes it.</td></tr>
    <tr><td><span class="pill dn">Fn + B</span></td><td>Hold 1 s, let go: both off 2 s later (bag, travel).</td></tr>
    <tr><td><span class="pill">⇧ / Space</span></td><td>After off: ⇧ turns the left half on, Space the right.</td></tr>
  </table>
  <h3>Flashing <span>Fn = hold ⇧, then hold Space; hold the key 1 s</span></h3>
  <table>
    <tr><td><span class="pill dn">Fn + Z</span></td><td>Bootloader, left</td><td><span class="pill dn">Fn + /</span></td><td>Bootloader, right</td></tr>
    <tr><td><span class="pill dn">Fn + X</span></td><td>Reset, left</td><td><span class="pill dn">Fn + .</span></td><td>Reset, right</td></tr>
  </table>
  <p>Bootloader mounts <b>XIAO-SENSE</b>: copy that half's <b>.uf2</b> onto it.
  App switcher: hold <b>⇧</b>, tap <b>T</b> (<b>S</b> back), release.
  Mac: keep the <b>Colemak</b> input source; dictation shortcut <b>Right ⌘ twice</b>.</p>
</section>"""

CSS = """
@page { size: A4 landscape; margin: 7mm; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; color: #1d1d1b; }
header { display: flex; align-items: baseline; justify-content: space-between; height: 9mm; }
header h1 { font-size: 15pt; font-weight: 600; margin: 0; letter-spacing: -0.2pt; }
header h1 span { font-weight: 400; color: #6b6a65; font-size: 10pt; margin-left: 3mm; }
.legend { display: flex; gap: 4mm; font-size: 7pt; color: #4a4945; }
.legend i { display: inline-block; width: 3mm; height: 3mm; border-radius: 0.7mm; margin-right: 1mm; vertical-align: -0.4mm; border: 0.25mm solid; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm 4mm; }
.card { position: relative; height: 59mm; border: 0.3mm solid #d9d7cf; border-radius: 3mm; padding: 2.5mm; overflow: hidden; }
.card .title { position: absolute; left: 50%; top: 3mm; transform: translateX(-50%); width: 22mm; text-align: center; z-index: 2; }
.card .title b { display: block; font-size: 12pt; font-weight: 650; }
.card .title span { display: block; font-size: 6.5pt; color: #5c5b56; line-height: 1.2; margin-top: 0.6mm; }
.board { position: relative; width: calc(1250 * 0.095mm); height: 52mm; margin: 0 auto; }
.k { position: absolute; border-radius: 1.4mm; border: 0.25mm solid #c9c7be; background: #fff; display: flex; flex-direction: column;
     align-items: center; justify-content: center; text-align: center; line-height: 1.05; padding: 0.3mm; }
.k .m { font-size: 8pt; font-weight: 600; }
.k .m.small { font-size: 6.3pt; }
.k .s { font-size: 4.9pt; color: #5c5b56; margin-top: 0.4mm; }
.k.empty { background: none; border: 0.25mm dashed #dddbd3; }
.k.md { background: #efeee9; }
.k.ag { background: #e4eefb; border-color: #8fb4e6; } .k.ag .m, .k.ag .s { color: #0c447c; }
.k.br { background: #e8f3dc; border-color: #9cc672; } .k.br .m, .k.br .s { color: #2c5410; }
.k.dn { background: #fbe5e3; border-color: #e59a92; } .k.dn .m, .k.dn .s { color: #8f2424; }
.k.hd { background: #3d3c39; border-color: #3d3c39; } .k.hd .s { color: #fff; font-size: 5.5pt; }
.k.ly-ai { background: #ece9fb; border: 0.5mm solid #6d5bd0; } .k.ly-ai .s { color: #4b3ca8; font-weight: 600; }
.k.ly-nav { background: #e2f3ee; border: 0.5mm solid #0f8a6f; } .k.ly-nav .s { color: #0a5e4b; font-weight: 600; }
.k.ly-sym { background: #fcefd9; border: 0.5mm solid #c27a00; } .k.ly-sym .s { color: #7a4c00; font-weight: 600; }
.k.ly-fn { background: #fbe7e3; border: 0.5mm solid #c2412d; } .k.ly-fn .s { color: #8f2a1a; font-weight: 600; }
.card.ai { border: 0.6mm solid #6d5bd0; } .card.ai .title b { color: #4b3ca8; }
.card.nav { border: 0.6mm solid #0f8a6f; } .card.nav .title b { color: #0a5e4b; }
.card.sym { border: 0.6mm solid #c27a00; } .card.sym .title b { color: #7a4c00; }
.card.fn { border: 0.6mm solid #c2412d; } .card.fn .title b { color: #8f2a1a; }
.info { padding: 2.5mm 4mm; font-size: 6.9pt; line-height: 1.3; }
.info h3 { font-size: 8.2pt; margin: 0 0 0.8mm; font-weight: 650; }
.info h3 span { font-weight: 400; color: #6b6a65; font-size: 6.8pt; margin-left: 1.5mm; }
.info p { margin: 0 0 2mm; }
.combos { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6mm 2mm; margin-bottom: 1.6mm; }
.combos b, .info table td:nth-child(odd) { white-space: nowrap; }
.combos b { display: inline-block; min-width: 9mm; background: #efeee9; border-radius: 1mm; padding: 0 1mm; margin-right: 1mm; text-align: center; }
table { border-collapse: collapse; width: 100%; margin-bottom: 1.2mm; }
td { padding: 0.35mm 2mm 0.35mm 0; vertical-align: middle; }
td:nth-child(odd) { width: 1%; }
.pill { display: inline-block; min-width: 6mm; text-align: center; border-radius: 1mm; padding: 0 1.2mm; background: #efeee9; font-weight: 600; }
.pill.dn { background: #fbe5e3; color: #8f2424; }
"""

LEGEND = """<div class="legend">
<span><i style="background:#e4eefb;border-color:#8fb4e6"></i>AI agent and terminal</span>
<span><i style="background:#e8f3dc;border-color:#9cc672"></i>Browser</span>
<span><i style="background:#efeee9;border-color:#c9c7be"></i>Modifier</span>
<span><i style="background:#fbe5e3;border-color:#e59a92"></i>Power and firmware</span>
<span><i style="background:#3d3c39;border-color:#3d3c39"></i>Held thumb</span></div>"""


def main():
    cards = "".join(card(*layer) for layer in LAYERS) + INFO
    html = (f'<!doctype html><html><head><meta charset="utf-8"><title>Forager keymap</title><style>{CSS}</style></head>'
            f'<body><header><h1>Forager keymap<span>Colemak on macOS · AI workflow · ZMK</span></h1>{LEGEND}</header>'
            f'<div class="grid">{cards}</div></body></html>')
    out = Path(__file__).with_name("forager_keymap_a4.html")
    out.write_text(html)
    print(out)


if __name__ == "__main__":
    main()
