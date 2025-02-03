from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton # noqa
from UI.reusables import TextFieldNormal # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<AddCryptoWalletScreen>:
    name: "add_crypto_wallet_screen"
    md_bg_color: app._dark

    TopLeftBackButton:

    MDLabel:
        padding: dp(25)
        text: "Link Your Crypto Wallet"
        font_size: "26dp"
        bold: True
        pos_hint: {"center_y": .87}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._white

    MDCard:
        md_bg_color: app._tinted
        size_hint: (.87, .13)
        pos_hint: {"center_x": .5, "center_y": .75}    
        radius: dp(11.5)
        padding: dp(11.5)

        MDBoxLayout:
            MDIcon:
                icon: "information"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app._gray

            MDLabel:
                text: "Supported wallets are:-"
                markup: True
                padding: dp(11.5)
                size_hint_y: None
                pos_hint: {"center_y": .5}
                font_style: "Subtitle2"
                halign: "left"
                theme_text_color: "Custom"
                text_color: app._gray

    TextFieldNormal:
        id: wallet
        hint_text: "Wallet"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .62}

    TextFieldNormal:
        id: wallet_api
        hint_text: "Wallet API"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .5}

    TextFieldNormal:
        id: wallet_chain
        hint_text: "Blockchain Network"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .38}

    TextFieldNormal:
        id: wallet_address
        hint_text: "Wallet Address"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .26}

    # add crypto wallet btn
    MDCard:
        md_bg_color: app._blue
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .15}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: True

        MDRectangleFlatIconButton:
            text: "Link Wallet"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._dark
            font_size: "20dp"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.change_screen_wt("home_screen", "left")

"""

Builder.load_string(KV)


class AddCryptoWalletScreen(MDScreen):
    pass
