from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton # noqa
from UI.reusables import TextFieldNormal # noqa
from UI.reusables import PasswordTextField # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<AddCardScreen>:
    name: "add_card_screen"
    md_bg_color: app._dark

    TopLeftBackButton:

    MDLabel:
        padding: dp(25)
        text: "Link Your Card"
        font_size: "26dp"
        bold: True
        pos_hint: {"center_y": .87}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._white

    MDCard:
        md_bg_color: app._tinted
        size_hint: (.87, None)
        height: "60dp"
        pos_hint: {"center_x": .5, "center_y": .79}    
        radius: dp(11.5)
        padding: dp(11.5)

        MDBoxLayout:
            MDIcon:
                icon: "information"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app._gray

            MDLabel:
                text: "Supported cards are [color=0000ff]VISA[/color] and [color=ffaa23]MASTERCARD[/color]"
                markup: True
                padding: dp(11.5)
                pos_hint: {"center_y": .5}
                font_size: "15dp"
                bold: True
                halign: "left"
                theme_text_color: "Custom"
                text_color: app._gray

    TextFieldNormal:
        id: card_holder_name
        hint_text: "  Card holder name "
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .69}

    TextFieldNormal:
        id: card_number
        hint_text: "  Card number "
        input_type: "number"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .58}

    MDBoxLayout:
        size_hint: (.85, None)
        height: "60dp"
        orientation: "horizontal"
        spacing: dp(23)
        pos_hint: {"center_x": .5, "center_y": .47}

        TextFieldNormal:
            id: card_expiry_date
            hint_text: "  Expiry "
            helper_text: "  Format: 01/25"
            multiline: False
            pos_hint: {"center_x": .5, "center_y": .5}

        PasswordTextField:
            id: cvv_number
            hint_text: " CVV"
            input_type: "number"
            multiline: False
            pos_hint: {"center_x": .5, "center_y": .42}

    # add card btn
    MDCard:
        md_bg_color: app._blue
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .34}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: True

        MDRectangleFlatIconButton:
            text: "Link Card"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._white
            font_size: "20dp"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.change_screen_wt("home_screen", "left")

"""

Builder.load_string(KV)


class AddCardScreen(MDScreen):
    pass
