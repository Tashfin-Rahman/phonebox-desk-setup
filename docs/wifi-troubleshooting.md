# Wi-Fi troubleshooting

My panel connected over USB but not over Wi-Fi. These fixes solved it, in this order:

## 1. Same network?
On the phone: Settings → Wi-Fi → your network → **IP address**. It must start with the same numbers as the
address PhoneBox shows under *Settings › General › Wi-Fi & Tailscale* (for me: `192.168.100.x`).
If they differ, connect both to the same router, or install [Tailscale](https://tailscale.com) on both.

## 2. Let PhoneBox through Windows Firewall
Windows Security → *Allow an app through firewall* → **Change settings** → **Allow another app…** → Browse to:

```
C:\Users\<you>\AppData\Local\PhoneBox\app\PhoneBoxAgent.exe
```

(`AppData` is hidden: in File Explorer, turn on View → Show → Hidden items first.) Tick **Private** only.

## 3. Is your network set to Private? (this was my real problem)
Settings → Network & internet → your Ethernet / Wi-Fi → **Network profile type → Private**.
If it's **Public**, the firewall rule from step 2 doesn't apply.

## 4. Re-sync
Plug the phone in over USB for a minute, then unplug it. The status line on the phone should say **Wi-Fi**.

## Red "LOAD FAIL …/api/art" bar?
This is a PhoneBox bug, not a Wi-Fi problem. When the track changes while the panel is fetching the album cover, the
PC answers 404 for the old cover. The Now Playing widget handles that fine, but PhoneBox's boot-error watcher also
reports the failed `<img>` as a red bar that stays until the panel reloads.

- **My workaround:** use `media-remote` ("Now playing" without cover art) instead of `media`, so no cover is ever requested.
- **The real fix:** PhoneBox fixed it in **0.9.18** (#200): the box now ignores failed covers and photos. After
  updating (the phone app updates over USB, so plug the phone in once), you can swap `media` back in.
- **To clear it once:** reopen the app, or `POST http://127.0.0.1:8765/api/refresh?reload=true` from the PC.
