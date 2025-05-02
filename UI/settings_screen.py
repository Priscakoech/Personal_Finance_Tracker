
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from UI.reusables import TopLeftBackButton, RightArrow, CustomLabel, LeftIconContainer, WidgetContainer # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """
<SettingsScreen>:
    name: "settings_screen"
    md_bg_color: app._dark

    # Custom Top App Bar
    MDCard:
        size_hint: (1, None)
        height: dp(61)
        radius: dp(0)
        pos_hint: {"top": 1}
        md_bg_color: app._dark
        orientation: "vertical"

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(60)
            padding: dp(17.5)
            MDBoxLayout:
                md_bg_color: app._lightgray
                size_hint: (None, None)
                size: ("34dp", "34dp")
                pos_hint: {"center_y": .5}
                radius: self.height / 2
                line_color: app._blue
    
                TopLeftBackButton:
    
            MDBoxLayout:
                size_hint: (1, 1)
                padding: dp(8), dp(0), dp(0), dp(0)
    
                CustomLabel:
                    text: "[size=18dp]Settings[/size]"
                    bold: True
                    halign: "center"
    
            MDBoxLayout:
                size_hint: (None, None)
                size: ("38dp", "38dp")
                pos_hint: {"center_y": .5}

                MDCard:
                    ripple_behavior: True
                    md_bg_color: app._red
                    size_hint: (None, None)
                    size: ("38dp", "38dp")
                    pos_hint: {"center_y": .5}
                    radius: self.height / 2
                    on_release: root.show_logout_dialog()

                    MDIcon:
                        icon: "logout"
                        padding: dp(9.5)
                        theme_text_color: "Custom"
                        text_color: app._white
                        pos_hint: {"center_y": .5}
                        font_size: "23dp"

        MDBoxLayout:
            md_bg_color: app._lightgray
            size_hint: (.98, None)
            height: dp(1.8)
            pos_hint: {"center_x": .5}
    
    MDCard:
        id: profile_photo_background
        md_bg_color: app._invisible
        line_color: app._blue
        size_hint: (None, None)
        size: ("136dp", "136dp")
        radius: self.height / 2
        pos_hint: {"center_x": .5, "center_y": .75}

        FitImage:
            id: settings_dp
            source: app.profile_photo
            radius: profile_photo_background.height / 2

    MDLabel:
        id: settings_name
        text: app.full_name
        halign: "center"
        pos_hint: {"center_y": .63}
        font_size: "22dp"
        bold: True
        theme_text_color: "Custom"
        text_color: app._white

    MDLabel:
        id: settings_mail
        text: app.email_address
        halign: "center"
        pos_hint: {"center_y": .59}
        font_size: "16dp"
        bold: True
        theme_text_color: "Custom"
        text_color: app._gray

    WidgetContainer:
        pos_hint: {"center_x": .5, "top": .52}
        on_release: app.switch_screen("personal_info_screen")

        LeftIconContainer:
            Image:
                source: "assets/images/personal_info_icon.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.43, .6)

        MDBoxLayout:
            CustomLabel:
                text: "  Personal Information"

        RightArrow:

    WidgetContainer:
        pos_hint: {"center_x": .5, "top": .41}
        on_release: app.switch_screen("reports_screen")

        LeftIconContainer:
            Image:
                source:  "assets/images/reports_icon.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.53, .63)

        MDBoxLayout:
            CustomLabel:
                text: "  Financial Reports"

        RightArrow:

    WidgetContainer:
        pos_hint: {"center_x": .5, "top": .3}
        on_release: app.switch_screen("privacy_policy_screen")

        LeftIconContainer:
            Image:
                source:  "assets/images/privacy_policy_icon.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.66, .66)

        MDBoxLayout:
            CustomLabel:
                text: "  Privacy Policy"

        RightArrow:

    WidgetContainer:
        pos_hint: {"center_x": .5, "top": .19}    
        on_release: app.switch_screen("terms_of_use_screen")

        LeftIconContainer:
            Image:
                source:  "assets/images/terms_of_use_icon.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.66, .66)

        MDBoxLayout:
            CustomLabel:
                text: "  Terms of Use"

        RightArrow:

    MDLabel:
        text: "Personal Finance Tracker" +\"\\nv1.0"
        halign: "center"
        pos_hint: {"center_y": .04}
        font_size: "14dp"
        bold: True
        theme_text_color: "Custom"
        text_color: app._gray

"""

Builder.load_string(KV)


class SettingsScreen(MDScreen):
    dialog = None
    def __init__(self, store=None, snackbar=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_data_store = store
        self.show_snackbar = snackbar
        self._white, self._red, self._green, self._blue = "#dddddd", "#ff2f3f", "#2fc46c", "#005eff"

    def show_logout_dialog(self):
        self.dialog = MDDialog(
            title="Log out Request.",
            text="You are about to log out...\nAre you sure about this?",
            buttons=[
                MDRectangleFlatButton(text="YES", line_color=self._red, theme_text_color="Custom", text_color=self._white, on_release=self.app_logout),
                MDRectangleFlatButton(text="NO", line_color=self._green, theme_text_color="Custom", text_color=self._white, on_release=lambda x: self.dialog.dismiss())
            ],
        )

        self.dialog.open()

    def app_logout(self, *args):
        self.dialog.dismiss()
        self.manager.current = "onboarding_screen"
        self.user_data_store.put("credentials", uid="", id_token="", refresh_token="")
        Clock.schedule_once(lambda dt: self.show_snackbar(text="You are now logged out...", background=self._blue), .3)
