"""
unPlug - a small macOS status bar app that reminds you to unplug your Mac
once the battery reaches a chosen charge threshold.

Project: https://github.com/JanuszPXYZ/unPlug
"""

import rumps
import psutil

# --- configuration ---------------------------------------------------------

DEFAULT_THRESHOLD = 85      # notify once the battery reaches this percentage
MIN_THRESHOLD = 10
MAX_THRESHOLD = 100
POLL_SECONDS = 5            # how often the battery is sampled
LOW_BATTERY = 20            # below this, the status bar shows a warning glyph

# Status bar glyphs. Using text instead of image files keeps the app
# self-contained: there are no asset paths that can go missing.
GLYPH_CHARGING = "⚡"       # high voltage
GLYPH_BATTERY = "\U0001f50b"    # battery
GLYPH_LOW = "⚠️"      # warning

# Stable menu keys. rumps keys a menu item by the title it was created with
# and does NOT re-key it when the title changes, so these stay valid even
# after the visible text is updated.
MENU_CHARGE = "Charge"
MENU_THRESHOLD = "Current Threshold"
MENU_PLUGGED = "Plugged in"
MENU_SETTINGS = "Change Threshold"
MENU_ABOUT = "About"


def parse_threshold(text):
    """
    Turn user input into a valid threshold percentage.

    Accepts values such as "85", " 85 ", "85%" and "85.0".
    Raises ValueError if the text is not a number or is out of range.
    """
    cleaned = text.strip().rstrip("%").strip()
    if not cleaned:
        raise ValueError("no value entered")
    value = int(round(float(cleaned)))
    if not MIN_THRESHOLD <= value <= MAX_THRESHOLD:
        raise ValueError(
            "threshold must be between {0} and {1}".format(
                MIN_THRESHOLD, MAX_THRESHOLD
            )
        )
    return value


class UnplugMe(rumps.App):
    def __init__(self):
        super(UnplugMe, self).__init__("unPlug")

        self.threshold = DEFAULT_THRESHOLD

        # True once the user has been told to unplug for the current charge
        # cycle. Prevents the notification repeating on every poll.
        self._notified = False

        self.menu.add(rumps.MenuItem(title=MENU_CHARGE))
        self.menu.add(rumps.MenuItem(title=MENU_THRESHOLD))
        self.menu.add(rumps.MenuItem(title=MENU_PLUGGED))
        self.menu.add(rumps.MenuItem(title=MENU_SETTINGS))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem(title=MENU_ABOUT))

        self.menu[MENU_THRESHOLD].title = "Current Threshold: {0}%".format(
            self.threshold
        )
        self.refresh()

    # --- core loop ---------------------------------------------------------

    def refresh(self):
        """
        Sample the battery once and update the status bar and menu.

        The battery is read a single time per call so that every line of the
        menu describes the same moment in time.
        """
        battery = psutil.sensors_battery()

        if battery is None:
            # Desktop Macs, or a machine where the battery cannot be read.
            self.title = GLYPH_BATTERY
            self.menu[MENU_CHARGE].title = "Charge: unavailable"
            self.menu[MENU_PLUGGED].title = "Plugged in: unavailable"
            return

        percent = int(round(battery.percent))
        plugged = bool(battery.power_plugged)

        if plugged:
            glyph = GLYPH_CHARGING
        elif percent <= LOW_BATTERY:
            glyph = GLYPH_LOW
        else:
            glyph = GLYPH_BATTERY

        self.title = "{0} {1}%".format(glyph, percent)
        self.menu[MENU_CHARGE].title = "Charge: {0}%".format(percent)
        self.menu[MENU_PLUGGED].title = "Plugged in: {0}".format(
            "Yes" if plugged else "No"
        )

        # Fire once when the threshold is reached or passed. Comparing with
        # >= rather than == matters: the battery percentage can skip values
        # between polls, and an equality test would miss the crossing
        # entirely and never notify.
        if plugged and percent >= self.threshold:
            if not self._notified:
                self._notified = True
                rumps.notification(
                    title="Your Mac has reached {0}%".format(self.threshold),
                    subtitle="You can unplug your machine",
                    message="Save your battery life!",
                )
        else:
            # Re-arm once unplugged, or if the charge drops back below the
            # threshold (including when the threshold is raised).
            self._notified = False

    @rumps.timer(POLL_SECONDS)
    def update_info(self, _):
        self.refresh()

    # --- menu actions ------------------------------------------------------

    @rumps.clicked(MENU_SETTINGS)
    def charge_threshold(self, _):
        """Prompt for a new charge threshold and validate what is entered."""
        window = rumps.Window(
            message="Set the charge threshold ({0}-{1}%):".format(
                MIN_THRESHOLD, MAX_THRESHOLD
            ),
            title="Preferences",
            default_text=str(self.threshold),
            ok="Apply",
            cancel="Cancel",
            dimensions=(100, 50),
        )

        response = window.run()
        if not response.clicked:
            return

        try:
            self.threshold = parse_threshold(response.text)
        except ValueError as error:
            # Without this the bad value reaches the timer callback and
            # raises on every poll, once every few seconds, forever.
            rumps.alert(
                title="Invalid threshold",
                message="{0}\n\nPlease enter a whole number between "
                "{1} and {2}.".format(error, MIN_THRESHOLD, MAX_THRESHOLD),
            )
            return

        self.menu[MENU_THRESHOLD].title = "Current Threshold: {0}%".format(
            self.threshold
        )
        self._notified = False
        self.refresh()

    @rumps.clicked(MENU_ABOUT)
    def about(self, _):
        rumps.Window(
            message="Additional Info",
            title="About unPlug",
            default_text=(
                "Contact me: januszpolowczyk19@gmail.com\n"
                "Project can be found @: https://github.com/JanuszPXYZ/unPlug"
            ),
            ok=None,
            dimensions=(300, 300),
        ).run()


if __name__ == "__main__":
    UnplugMe().run()
