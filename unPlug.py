import rumps
import psutil

## Icons for the app downloaded from:
# App logo in the dock created by: monkik "https://www.flaticon.com/free-icon/charging_861088"
# Status Bar icon: "https://icons8.com/icon/64388/charging-station"
# Wrench (Maintenance) Icon in Settings: "https://icons8.com/icon/11151/maintenance"


UNPLUG_AT = 85


class UnplugMe(rumps.App):

    unplugAt = UNPLUG_AT

    def __init__(self):
        super(UnplugMe, self).__init__("UnplugMe")
        self.icon = '/Users/januszpolowczyk/Documents/StatusBarApp/icons/charging_station.png'
        self.menu.add(rumps.MenuItem(title = "Charge: "))
        self.menu.add(rumps.MenuItem(title = "Current Threshold: 85%"))
        self.menu.add(rumps.MenuItem(title = "Plugged in: "))
        self.menu.add(rumps.MenuItem(title = "Change Threshold"))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem(title = "About"))
        self.battery = psutil.sensors_battery()
    

    @rumps.clicked("Change Threshold")
    def charge_threshold(self, sender):
        '''
        Prompts the user to enter the value of the charging threshold. 
        Input values should be no greater than 100 (<= 100)
        '''
        settings = rumps.Window(message = "Set the charge threshold: ",
        title = "Preferences",
        default_text = self.unplugAt,
        ok = "Apply",
        cancel = "Cancel",
        dimensions = (100,50))
        settings.icon = '/Users/januszpolowczyk/Documents/StatusBarApp/icons/wrench2.png'

        window_menu = settings.run()
        if window_menu.clicked:
            self.unplugAt = window_menu.text
            self.menu["Current Threshold: 85%"].title = "Current Threshold: " + str(self.unplugAt) + "%"

    def refresh_bar(self):
        '''
        Refreshing the information displayed in the apps status bar menu
        '''
        if (psutil.sensors_battery().power_plugged == True and str(int(self.unplugAt)) == str(int(psutil.sensors_battery().percent))):
            rumps.notification("Your Mac is charged at a set threshold", "You can unplug your machine",
            "Save your battery life!")
        self.menu["Plugged in: "].title = "Plugged in: " + str(psutil.sensors_battery().power_plugged)

    @rumps.timer(5)
    def update_info(self, sender):
        def counter(t):
            self.refresh_bar()
            if (psutil.sensors_battery().power_plugged == False and str(int(self.unplugAt)) == str(int(psutil.sensors_battery().percent))):
                self.menu["Charge: "] = "Charge: " + str(psutil.sensors_battery().percent) + "%"
        self.menu["Plugged in: "].title = "Plugged in: " + str(psutil.sensors_battery().power_plugged)
        self.menu['Charge: '].title = "Charge: " + str(psutil.sensors_battery().percent) + "%"
            

        counter(None)

    @rumps.clicked("About")
    def about(self, _):
        about_window = rumps.Window(message = "Additional Info",
        title = "About", default_text = "Contact me: januszpolowczyk19@gmail.com \nProject can be found @: https://github.com/JanuszPXYZ/unPlug",
        ok = None,
        dimensions = (300,300))

        about_window.run()


if __name__ == "__main__":
    UnplugMe().run()

