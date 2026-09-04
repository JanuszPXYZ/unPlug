# unPlug

A small macOS status bar app that reminds you to unplug your MacBook once the
battery reaches a charge threshold you choose.

Keeping a laptop at 100% all day is harder on the battery than letting it sit
somewhere in the middle, so unPlug watches the charge level and tells you when
it is a good moment to pull the cable.

<img width="211" alt="unPlug in the status bar" src="https://user-images.githubusercontent.com/19962689/81486768-6efb6280-9257-11ea-8b65-596e8d7be8e8.png">

The status bar shows the current charge at a glance:

| Display | Meaning |
| --- | --- |
| `⚡ 85%` | plugged in and charging |
| `🔋 62%` | running on battery |
| `⚠️ 15%` | running on battery, below 20% |

All the battery details live in the menu — current charge, whether the machine
is plugged in, and the active threshold. The threshold starts at 85% and can be
changed at any time from **Change Threshold**.

<img width="420" alt="unPlug menu" src="https://user-images.githubusercontent.com/19962689/81486791-9baf7a00-9257-11ea-852a-c24e84592734.png">

<img width="344" alt="Setting the threshold" src="https://user-images.githubusercontent.com/19962689/81503160-6a2fc080-92e2-11ea-9436-14dae8f5cad8.png">

## Running from source

Requires Python 3.9 or newer on macOS.

```bash
git clone https://github.com/JanuszPXYZ/unPlug.git
cd unPlug
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python unPlug.py
```

The app runs in the status bar. Quit it from its own menu.

## Building a standalone .app

```bash
pip install -r requirements-dev.txt
python setup.py py2app
```

The bundle is written to `dist/unPlug.app`. It is marked `LSUIElement`, so it
appears only in the status bar and not in the Dock or app switcher.

## Version 0.2.0

The first update since 2020. The app now runs again on current macOS and
Python; previously it could not start at all.

- **Fixed a crash on launch.** The app loaded its icons from hardcoded absolute
  paths that pointed inside one specific machine's home folder. Those files were
  never part of the repository, so the app raised `FileNotFoundError` on startup
  for anyone who cloned it. The status bar now uses text glyphs and the app has
  no external asset files to lose.
- **Fixed the reminder never firing.** The notification triggered only when the
  battery percentage was *exactly* equal to the threshold. Charge levels skip
  values between polls, so a battery going from 84% to 86% jumped straight past
  an 85% threshold and no reminder was ever shown. The check now triggers on
  reaching *or passing* the threshold.
- **The reminder no longer repeats.** It fires once per charge cycle and re-arms
  when you unplug, instead of firing on every poll while the machine sits above
  the threshold.
- **Threshold input is validated.** Entering text, an empty value, or a number
  out of range used to raise an exception inside the timer callback every few
  seconds for as long as the app stayed open. Input is now checked, values such
  as `85%` and `85.0` are accepted, and anything invalid shows an explanation
  and leaves the old threshold in place.
- **Updated dependencies** to versions that support Python 3.12 and Apple
  Silicon: `rumps` 0.4.0, `psutil` 7.x, `pyobjc` 12.x, `py2app` 0.28.x.
- **Trimmed the dependency list.** `numpy`, `wxPython` and `Pillow` were listed
  but never imported — `Pillow` was the source of years of security alerts on a
  package the app never used. Transitively installed build packages are no
  longer pinned by hand.
- **Handles Macs without a battery** rather than crashing on them.
- The battery is now read once per refresh instead of six times, so every line
  of the menu describes the same moment.

## Version 0.1.1

- After the update, the app no longer resides in the bottom bar when active
  (initially it was visible both in the dock and the status bar). It is visible
  only in the status bar.
- Some errors that caused the app to crash were removed.

## A note on macOS's own battery management

Recent versions of macOS include Optimized Battery Charging, and some Macs can
cap charging at 80%. unPlug remains useful if you want a threshold of your own
choosing and an explicit reminder rather than silent background management.

## Credits for the icons

The screenshots above show the original icons by:

1) App logo in the dock created by monkik — https://www.flaticon.com/free-icon/charging_861088
2) Status bar icon — https://icons8.com/icon/64388/charging-station
3) Wrench (Maintenance) icon in settings — https://icons8.com/icon/11151/maintenance
