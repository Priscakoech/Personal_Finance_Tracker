from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<TermsOfUseScreen>:
    name: "terms_of_use_screen"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: app._tinted
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .95}    
        radius: dp(11.5)

        TopLeftBackButton:
            pos_hint: {"center_y": .5}

        MDLabel:
            padding: (11.5, 0)
            text: "Terms of Use"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: app._white
            pos_hint: {"center_y": .5}
            halign: "left"

"""

Builder.load_string(KV)


class TermsOfUseScreen(MDScreen):
    pass
