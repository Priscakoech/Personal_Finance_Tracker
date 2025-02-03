from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import RightArrow, CustomLabel, LeftIconContainer, WidgetContainer # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<SettingsScreen>:
    name: "settings_screen"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: app._tinted
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .95}    
        radius: dp(11.5)

        TopLeftBackButton:
            pos_hint: {"center_y": .5}

        MDLabel:
            padding: (23, 0)
            text: "Settings"
            font_style: "H6"
            pos_hint: {"center_y": .5}
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._white

        MDIconButton:
            _no_ripple_effect: True
            padding: 17.5
            icon: "logout"
            theme_text_color: "Custom"
            text_color: app._red
            pos_hint: {"center_y": .5}
            halign: "right"

    MDCard:
        background: app.profile_photo
        md_bg_color: app._white
        line_color: app._dark
        size_hint: (None, None)
        size: ("136dp", "136dp")
        radius: self.height / 2
        pos_hint: {"center_x": .5, "center_y": .75}

    MDLabel:
        text: app.full_name
        halign: "center"
        pos_hint: {"center_y": .63}
        font_size: "22dp"
        bold: True
        theme_text_color: "Custom"
        text_color: app._white

    MDLabel:
        text: app.email_address
        halign: "center"
        pos_hint: {"center_y": .59}
        font_size: "16dp"
        bold: True
        theme_text_color: "Custom"
        text_color: app._gray

    WidgetContainer:
        pos_hint: {"center_x": .5, "top": .52}
        on_release: app.change_screen_wt("personal_info_screen", "left")

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
        on_release: app.change_screen_wt("reports_screen", "left")

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
        on_release: app.change_screen_wt("privacy_policy_screen", "left")

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
        on_release: app.change_screen_wt("terms_of_use_screen", "left")

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
    pass
