
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
import requests
from requests.exceptions import ConnectionError, Timeout
from UI.reusables import CustomLabel # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """
<NoInternetScreen>:
    name: "no_internet_screen"
    md_bg_color: app._dark

    Image:
        source: "assets/images/pft_logo.png"
        size_hint: (None, None)
        size: ("250dp", "250dp")
        pos_hint: {"center_x": .48, "center_y": .75}

    MDBoxLayout:
        id: spinning_widget
        opacity: 0
        orientation: "vertical"
        size_hint: (1, None)
        height: "236dp"
        pos_hint: {"center_x": .5, "center_y": .18}

        MDSpinner:
            size_hint: (None, None)
            size: ("43dp", "43dp")
            pos_hint: {"center_x": .5}

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(96.5)

    MDBoxLayout:
        id: no_internet_content
        opacity: 1
        orientation: "vertical"
        size_hint: (1, None)
        height: "236dp"
        pos_hint: {"center_x": .5, "center_y": .18}
        padding: dp(23)
        spacing: dp(23)

        MDIcon:
            icon: "wifi-off"
            font_size: "33dp"
            pos_hint: {"center_x": .5}

        CustomLabel:
            text: "[size=26dp][b]App offline[/b][/size]\\n[color=a6a6a6]There was a problem loading your data, please check your internet connection.[/color]"
            halign: "center"

        MDRoundFlatButton:
            text: "Reload"
            font_size: dp(16)
            theme_text_color: "Custom"
            text_color: "#ffffff"
            md_bg_color: "#aaaaaa26"
            line_color: "#005eff"
            size_hint_x: None
            width: dp(123)
            pos_hint: {"center_x": .5}
            on_release: root.retry_check()

"""

Builder.load_string(KV)


class NoInternetScreen(MDScreen):
    enter_app_callback = None

    def check_internet(self, dt=None):
        try:
            response = requests.get("https://www.google.com", timeout=6)
            if response.status_code == 200:
                if self.enter_app_callback:
                    self.enter_app_callback(self.manager)
            else: self.show_no_internet()
        except (ConnectionError, Timeout): self.show_no_internet()
        except Exception as e: self.show_no_internet()

    def show_no_internet(self):
        self.ids.spinning_widget.opacity = 0
        self.ids.no_internet_content.opacity = 1

    def retry_check(self):
        self.ids.spinning_widget.opacity = 1
        self.ids.no_internet_content.opacity = 0
        Clock.schedule_once(self.check_internet, 6)
