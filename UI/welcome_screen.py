
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen


KV = """
<WelcomeScreen>:
    name: "welcome_screen"
    md_bg_color: app._dark

    Image:
        source: "assets/images/pft_logo.png"
        size_hint: (None, None)
        size: ("250dp", "250dp")
        pos_hint: {"center_x": .48, "center_y": .75}

    MDLabel:
        padding: dp(25)
        text: "Track, Get Insights, and Visualize the flow of your finances easily."
        font_size: "36dp"
        bold: True
        pos_hint: {"center_y": .4}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._white

    # get started btn
    MDCard:
        md_bg_color: app._white
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .18}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        on_release: app.switch_screen("onboarding_screen")

        MDBoxLayout:
            padding: (63, 0)
            MDLabel:
                text: "Get started"
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._dark
                font_size: "20dp"

            MDIcon:
                icon: "arrow-right"
                halign: "right"
                font_size: "23dp"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app._dark

    MDLabel:
        text: "By tapping on 'Get started', you are accepting our\\n" +\
            "[ref=privacy][u][color=00afff]Privacy Policy[/color][/u][/ref] and " +\
            "[ref=terms][u][color=00afff]Terms of Use[/color][/u][/ref]"
        markup: True
        font_size: "15dp"
        bold: True
        pos_hint: {"center_y": .063}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._gray
        on_ref_press: root.goto_hyperlink(args[1])

"""

Builder.load_string(KV)


class WelcomeScreen(MDScreen):
    def __init__(self, switch_screen=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.switch_screen = switch_screen

    def goto_hyperlink(self, ref):
        """Handles the reference texts..."""
        if ref == "privacy": self.switch_screen("privacy_policy_screen")
        elif ref == "terms": self.switch_screen("terms_of_use_screen")
