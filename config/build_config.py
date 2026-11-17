"""Builds phonebox-config.json: the pages, buttons and rules of this desk panel.

Run:  python config/build_config.py
Then paste the output into PhoneBox › Settings › Advanced (raw JSON) › Apply JSON › Save.
The tracker scripts are read from ../scripts so they stay readable as normal .ps1 files.
"""
import json
from pathlib import Path

PC_USER = "user"  # your Windows user name (C:\Users\<this>)
ROOT = Path(__file__).resolve().parent.parent
ps1 = lambda name: (ROOT / "scripts" / name).read_text(encoding="utf-8").strip()


def W(id, type, x, y, w, h, **options):
    widget = {"id": id, "type": type, "x": x, "y": y, "w": w, "h": h}
    if options:
        widget["options"] = options
    return widget


def page(id, title, icon, *widgets, enabled=True):
    return {"id": id, "title": title, "icon": icon, "enabled": enabled, "widgets": list(widgets)}


# ---------------------------------------------------------------- buttons
def key(id, label, icon, keys, color):
    return {"id": id, "label": label, "icon": icon, "color": color, "cmd": "builtin:keys", "args": keys, "toggle": False}


def macro(id, label, icon, steps, color):
    return {"id": id, "label": label, "icon": icon, "color": color, "cmd": "builtin:macro", "steps": steps, "toggle": False}


def app(id, label, icon, cmd, color, args=None):
    s = {"id": id, "label": label, "icon": icon, "color": color, "cmd": cmd, "toggle": False}
    if args:
        s["args"] = args
    return s


LOCAL = rf"C:\Users\{PC_USER}\AppData\Local"
launchers = [
    app("discord", "Discord", "💬", rf"{LOCAL}\Discord\Update.exe", "#5865f2", "--processStart Discord.exe"),
    app("operagx", "Opera GX", "🦊", rf"{LOCAL}\Programs\Opera GX\launcher.exe", "#fa1e4e"),
    app("claudeai", "Claude", "✳️", "https://claude.ai", "#d97757"),
    app("terminal", "Terminal", "⌨️", "wt.exe", "#4b5563"),
    app("explorer", "Files", "📁", "explorer.exe", "#e5b84b"),
    app("vscode", "VS Code", "📝", r"shell:AppsFolder\Microsoft.VisualStudioCode", "#2f80ed"),
    app("browser", "Browser", "🌐", "https://github.com", "#0ea5e9"),
    app("spotify", "Spotify", "🎧", r"shell:AppsFolder\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify", "#1db954"),
    app("calc", "Calculator", "🧮", "calc.exe", "#64748b"),
    app("settings", "Settings", "⚙️", "ms-settings:", "#94a3b8"),
    app("snip", "Snip", "✂️", "ms-screenclip:", "#14b8a6"),
    app("taskmgr", "Task Manager", "📊", "taskmgr.exe", "#22c55e"),
    app("mute", "Mute", "🔇", "builtin:mute", "#f59e0b"),
    app("monitoroff", "Screen Off", "🌙", "builtin:monitor-off", "#6366f1"),
    key("clip30", "Clip last 30s", "🎬", "win+alt+g", "#ef4444"),
    key("gamebar", "Game Bar", "🎮", "win+g", "#22c55e"),
    app("claudecode", "Start Claude Code", "⌨️", "powershell.exe", "#d97757", "-NoExit -Command claude"),
    app("claudeusage", "Claude usage", "📊", "https://claude.ai/settings/usage", "#b45f3c"),
    key("yt-cap", "Captions", "💬", "c", "#64748b"),
    key("br-reload", "Reload", "🔄", "ctrl+r", "#0369a1"),
    key("br-close", "Close tab", "✖️", "ctrl+w", "#0369a1"),
]

# Button sets used by the Live page's smart buttons (scripts/smart-buttons.html picks the set for the app in front).
# Each set = (set id, title, icon, process names, buttons). Only the buttons are needed in the config.
RED, GREEN, BLURPLE, CLAY, AMBER, SLATE = "#ef4444", "#1db954", "#5865f2", "#d97757", "#f59e0b", "#64748b"
live_sets = [
    ("live-opera", "Live · Opera", "📺", "opera|chrome|msedge|brave|firefox", [
        key("yt-play", "Play / pause", "⏯️", "k", RED), key("yt-back", "Back 10s", "⏪", "j", RED),
        key("yt-fwd", "Forward 10s", "⏩", "l", RED), key("yt-full", "Fullscreen", "⛶", "f", RED),
        key("yt-next", "Next video", "⏭️", "shift+n", RED), key("br-back", "Back", "⬅️", "alt+left", RED),
        key("br-newtab", "New tab", "➕", "ctrl+t", RED), key("tab-next", "Next tab", "➡️", "ctrl+tab", RED)]),
    ("live-spotify", "Live · Spotify", "🎧", "Spotify", [
        key("sp-play", "Play / pause", "⏯️", "space", GREEN), key("sp-prev", "Previous", "⏮️", "ctrl+left", GREEN),
        key("sp-next", "Next", "⏭️", "ctrl+right", GREEN), key("sp-like", "Like", "💚", "alt+shift+b", GREEN),
        key("sp-shuffle", "Shuffle", "🔀", "ctrl+s", GREEN), key("sp-repeat", "Repeat", "🔁", "ctrl+r", GREEN),
        key("sp-volup", "Volume up", "🔊", "ctrl+up", GREEN), key("sp-voldown", "Volume down", "🔉", "ctrl+down", GREEN)]),
    ("live-discord", "Live · Discord", "💬", "Discord", [
        key("dc-mute", "Mute mic", "🎙️", "ctrl+shift+m", BLURPLE), key("dc-deafen", "Deafen", "🎧", "ctrl+shift+d", BLURPLE),
        key("dc-switch", "Quick switch", "🔎", "ctrl+k", BLURPLE), key("dc-read", "Mark read", "✔️", "esc", BLURPLE),
        key("dc-answer", "Answer call", "📞", "ctrl+enter", BLURPLE), key("dc-unread", "Next unread", "📩", "alt+shift+down", BLURPLE),
        key("dc-up", "Scroll up", "⬆️", "pageup", BLURPLE), key("dc-down", "Scroll down", "⬇️", "pagedown", BLURPLE)]),
    ("live-code", "Live · Claude & code", "💻", "claude|Code|WindowsTerminal|powershell|pwsh", [
        key("cd-enter", "Enter", "↩️", "enter", CLAY), key("cd-esc", "Esc / stop", "⏹️", "esc", CLAY),
        key("cd-ctrlc", "Ctrl+C", "✋", "ctrl+c", CLAY), key("cd-up", "Previous", "⬆️", "up", CLAY),
        macro("cd-usage", "/usage", "📊", ["text:/usage", "keys:enter"], CLAY),
        macro("cd-clear", "/clear", "🧹", ["text:/clear", "keys:enter"], CLAY),
        key("cd-save", "Save", "💾", "ctrl+s", CLAY), key("cd-undo", "Undo", "↩", "ctrl+z", CLAY)]),
    ("live-docs", "Live · Study apps", "📚", "WINWORD|EXCEL|POWERPNT|Acrobat|AcroRd32|Notion|Obsidian", [
        key("dk-prev", "Previous", "◀️", "pageup", AMBER), key("dk-next", "Next", "▶️", "pagedown", AMBER),
        key("dk-zin", "Zoom in", "➕", "ctrl+equals", AMBER), key("dk-zout", "Zoom out", "➖", "ctrl+minus", AMBER),
        key("dk-save", "Save", "💾", "ctrl+s", AMBER), key("dk-undo", "Undo", "↩", "ctrl+z", AMBER),
        key("dk-find", "Find", "🔎", "ctrl+f", AMBER), key("dk-show", "Slideshow", "📽️", "f5", AMBER)]),
    ("live", "Live", "🖥️", None, [
        key("alt-tab", "Switch app", "🔀", "alt+tab", SLATE), key("os-desktop", "Show desktop", "🏠", "win+d", SLATE),
        key("os-files", "Files", "📁", "win+e", SLATE), key("shot", "Screenshot", "📸", "win+alt+printscreen", SLATE),
        key("os-tasks", "Task view", "🗂️", "win+tab", SLATE), key("os-snip", "Snip", "✂️", "win+shift+s", SLATE),
        key("os-mute", "Mute", "🔇", "mute", SLATE), key("lock", "Lock", "🔒", "win+l", SLATE)]),
]

shortcuts, seen = [], set()
for s in launchers + [b for *_, buttons in live_sets for b in buttons]:
    if s["id"] not in seen:
        seen.add(s["id"])
        shortcuts.append(s)

# ---------------------------------------------------------------- pages
RIGHT_NOW, TODAY, OPEN_WINDOWS = ps1("right-now.ps1"), ps1("today.ps1"), ps1("open-windows.ps1")


SMART_BUTTONS = (ROOT / "scripts" / "smart-buttons.html").read_text(encoding="utf-8").strip()

live = page("live", "Live", "🖥️",
            W("now", "command", 0, 0, 6, 2, title="Right now", command=RIGHT_NOW, interval=5),
            W("media", "media", 0, 2, 6, 2),
            W("today", "command", 6, 0, 6, 4, title="Today on the PC", command=TODAY, interval=60),
            W("buttons", "html", 0, 4, 8, 2, html=SMART_BUTTONS),
            W("windows", "command", 8, 4, 4, 2, title="Open on the PC", command=OPEN_WINDOWS, interval=5))

pages = [
    page("home", "Home", "🏠",
         W("clock", "clock", 0, 0, 6, 3, status=True, weather=True),
         W("media", "media", 6, 0, 6, 4),
         W("stat", "stat", 0, 4, 2, 2, metric="cpu"), W("stat-2", "stat", 2, 4, 2, 2, metric="gpu"),
         W("stat-3", "stat", 4, 4, 2, 2, metric="ram"), W("stat-4", "stat", 6, 4, 2, 2, metric="ping"),
         W("claude-5h", "quotaring", 8, 4, 2, 2, provider="claude", limit="0"),
         W("claude-week", "quotaring", 10, 4, 2, 2, provider="claude", limit="1"),
         W("now", "command", 0, 3, 6, 1, title="Right now", command=RIGHT_NOW, interval=10)),
    live,
    page("study", "Study", "📚",
         W("pomodoro", "pomodoro", 0, 0, 4, 6, focus=25, **{"break": 5}),
         W("checklist", "checklist", 4, 0, 4, 4, title="Today's tasks",
           items=["Revise class notes", "Work on assignment", "Read one chapter", "Check NSU email"], daily=True),
         W("note", "note", 4, 4, 4, 2, text="Exam focus:\n• ", color="#fbbf24"),
         W("clock", "clock", 8, 0, 4, 2, status=False, weather=False),
         W("progress", "progress", 8, 2, 4, 2),
         W("timer", "timer", 8, 4, 4, 2, label="Break", presets=["5", "10", "15"])),
    page("gaming", "Gaming", "🎮",
         W("gpu", "gpu", 0, 0, 4, 4),
         W("chart", "chart", 4, 0, 8, 3, metrics=["cpu", "gpu"]),
         W("shortcuts", "shortcuts", 4, 3, 8, 3, columns=4, ids=["discord", "operagx", "spotify", "mute"]),
         W("stat", "stat", 0, 4, 2, 2, metric="ping"), W("stat-2", "stat", 2, 4, 2, 2, metric="ram")),
    page("gamedeck", "Game deck", "🎧",
         W("ptt", "push-to-talk", 0, 0, 4, 3, title="Hold to talk"),
         W("panic", "panic-mute", 0, 3, 4, 3, title="Mute everything"),
         W("keys", "shortcuts", 4, 0, 8, 4, columns=3, ids=["dc-mute", "dc-deafen", "clip30", "gamebar", "shot", "discord"]),
         W("sounds", "soundboard", 4, 4, 8, 2, title="Soundboard")),
    page("ai", "AI work", "✳️",
         W("quotas", "quotas", 0, 0, 6, 6, providers=["claude"], rotate=False, pageSize=2, rotateInterval=8),
         W("sessions", "sessions", 6, 0, 6, 4),
         W("claude-keys", "shortcuts", 6, 4, 6, 2, columns=3, ids=["claudecode", "claudeusage", "claudeai"])),
    page("system", "System", "📊",
         W("chart", "chart", 0, 0, 6, 3, metrics=["cpu"]), W("chart-2", "chart", 6, 0, 6, 3, metrics=["gpu"]),
         W("meters", "meters", 0, 3, 6, 3), W("chart-3", "chart", 6, 3, 6, 3, metrics=["down", "up"])),
    page("procs", "Processes", "⚙️", W("processes", "processes", 0, 0, 12, 6)),
    page("deck", "Shortcuts", "🎛️", W("shortcuts", "shortcuts", 0, 0, 12, 6, columns=4)),
    page("music", "Music", "🎵",
         W("media", "media", 0, 0, 8, 6),
         W("clock", "clock", 8, 0, 4, 2, status=False, weather=False),
         W("forecast", "forecast", 8, 2, 4, 4, mode="daily")),
    page("world", "World", "🌍",
         W("worldclock", "worldclock", 0, 0, 12, 2),
         W("forecast", "forecast", 0, 2, 8, 4, mode="hourly"),
         W("calendar", "calendar", 8, 2, 4, 4), enabled=False),
    page("night", "Night", "🌙",
         W("analog", "analog", 0, 0, 5, 6, seconds=False, numbers=True, zone="", label=""),
         W("wordclock", "wordclock", 5, 0, 7, 3),
         W("moon", "moon", 5, 3, 7, 3)),
]

# ---------------------------------------------------------------- rules
def rule(id, name, when, then="goto", priority=5, **extra):
    return {"id": id, "name": name, "enabled": True, "when": when, "then": then,
            "whileActive": True, "priority": priority, **extra}


rules = [
    rule("r-ai", "AI needs me → AI work", "session-waiting", page="ai", priority=8),
    {**rule("r-game", "Game running → Gaming", "process-running", match="cs2|FC25|FC26", page="gaming", priority=6, forSec=10),
     "enabled": False},  # off: pages don't follow apps any more
    rule("r-study", "Study hours → Study", "time", match="19:00-22:00", days="sun,mon,tue,wed,thu", page="study", priority=4),
    rule("r-cpu", "CPU working hard", "cpu-above", then="notify", value=90, text="PC is working hard: {detail}",
         level="warn", forSec=30, cooldownMin=15, priority=3),
    rule("r-ping", "Internet slow", "ping-high", then="notify", text="Internet is slow: {detail}",
         level="warn", cooldownMin=10, priority=3),
    rule("r-afk", "Away 10 min → Night", "idle", value=10, page="night", priority=2),
    rule("r-late", "Late night → Night", "time", match="23:30-07:00", page="night", priority=2),
]

config = {
    "display": {"orientation": "landscape", "showSeconds": True, "hour12": False, "keepAwake": True,
                "accent": "#2dd4bf", "switchCountdownSec": 3, "touchGraceSec": 20, "minDwellSec": 15, "holdMaxMin": 30},
    "night": {"enabled": True, "start": "00:30", "end": "07:30", "brightness": 0.02},
    "weather": {"city": "Dhaka", "lat": 23.8103, "lon": 90.4125},
    "claude": {"phoneApprovals": True, "timeoutSec": 90, "onlyWhenAway": False},
    "pages": pages,
    "shortcuts": shortcuts,
    "rules": rules,
}

out = ROOT / "config" / "phonebox-config.json"
out.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {out.relative_to(ROOT)}: {len(pages)} pages, {len(shortcuts)} buttons, {len(rules)} rules")
