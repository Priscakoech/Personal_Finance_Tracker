from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """
<OnboardingScreen>:
    name: "onboarding_screen"
    md_bg_color: app._dark

    TopLeftBackButton:

    Image:
        source: "assets/images/onboarding.png"
        size_hint: (1, .5)
        pos_hint: {"center_x": .5, "center_y": .7}

    MDLabel:
        padding: dp(25)
        text: "Let's get you\\nonboard!"
        font_size: "36dp"
        bold: True
        pos_hint: {"center_y": .35}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._white

    # continue with google btn
    MDCard:
        md_bg_color: app._white
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .18}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: True

        MDRectangleFlatIconButton:
            icon: "assets/images/google_icon.png"
            text: "      Continue with Google"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._dark
            font_size: "20dp"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.change_screen_wt("full_name_input_screen", "left")

    MDLabel:
        text: "'Continue with Google' action will complete in\\nyour web browser."
        font_size: "15dp"
        bold: True
        pos_hint: {"center_y": .063}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._gray

"""

Builder.load_string(KV)


class OnboardingScreen(MDScreen):
    pass
