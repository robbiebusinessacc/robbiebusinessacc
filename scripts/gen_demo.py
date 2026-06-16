#!/usr/bin/env python3
"""Generate the profile terminal demo — no screen recording involved.

Writes assets/terminal.cast (asciicast v2) with a warm robbiew.dev theme baked into
the header, then render it to a GIF with agg (https://github.com/asciinema/agg):

    python3 scripts/gen_demo.py
    agg assets/terminal.cast assets/terminal.gif     # uses the theme in the cast header

Edit this script and re-render to change pacing or content — nothing here is
hand-recorded.

Pacing knobs: CHAR_DT (typing speed), PAUSE (wait after each command), END_HOLD
(final freeze). HEIGHT equals the visible line count so there's no empty space.
"""
import json
import os

WIDTH, HEIGHT = 80, 12
CHAR_DT = 0.035  # per-character typing delay
PAUSE = 0.30     # wait after a command's newline
END_HOLD = 4.0   # final freeze before the GIF loops

ESC = "\x1b"
AMBER = ESC + "[32m"   # $ shell prompt (warm)
CLAY = ESC + "[34m"    # >>> REPL prompt (warm)
GOLD = ESC + "[33m"    # output
GREY = ESC + "[90m"    # comments
RESET = ESC + "[0m"
SH = f"{AMBER}${RESET} "
PY = f"{CLAY}>>>{RESET} "

events = []
t = 0.0


def emit(text, dt=0.25):
    global t
    t += dt
    events.append([round(t, 3), "o", text])


def type_cmd(prompt, text):
    global t
    emit(prompt, 0.18)
    for ch in text:
        t += CHAR_DT
        events.append([round(t, 3), "o", ch])
    t += 0.1
    events.append([round(t, 3), "o", "\r\n"])
    t += PAUSE


def show(text):
    emit(text + "\r\n", 0.30)


emit(f"{GREY}# robbie walmsley · ai engineer{RESET}\r\n", 0.4)
type_cmd(SH, "python")
type_cmd(PY, "import robbie")
type_cmd(PY, "robbie.focus")
show(f"{GOLD}'making language models reliable enough to ship'{RESET}")
type_cmd(PY, "robbie.open_source")
show(f"{GOLD}['justllm', 'MAIF Backtester', 'AutoRecycle']{RESET}")
type_cmd(PY, "robbie.contributes_to")
show(f"{GOLD}['TransformerLens', 'Auto-GPT-Plugins', 'DocsGPT', 'pypdf']{RESET}")
type_cmd(PY, "robbie.site")
show(f"{GOLD}'https://robbiew.dev'{RESET}")
t += END_HOLD
events.append([round(t, 3), "o", ""])

# Warm robbiew.dev palette: cream fg on near-black bg; amber/clay/gold accents.
PALETTE = ":".join([
    "#15110b", "#c0563a", "#d6a35c", "#ead08a", "#c98a64", "#b58db0", "#86b3a8", "#f3ecdd",
    "#8a8173", "#d06a4a", "#e2b878", "#f0dca0", "#d8a07e", "#cda6c6", "#a3cfc2", "#f3ecdd",
])
header = {
    "version": 2,
    "width": WIDTH,
    "height": HEIGHT,
    "theme": {"fg": "#f3ecdd", "bg": "#15110b", "palette": PALETTE},
    "env": {"TERM": "xterm-256color", "SHELL": "/bin/zsh"},
}

os.makedirs("assets", exist_ok=True)
with open("assets/terminal.cast", "w", encoding="utf-8") as fh:
    fh.write(json.dumps(header) + "\n")
    for event in events:
        fh.write(json.dumps(event) + "\n")

print(f"wrote assets/terminal.cast ({len(events)} events, {round(t, 1)}s)")
