from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<WalletSetupScreen>:
    name: "wallet_setup_screen"
    md_bg_color: app._dark

    TopLeftBackButton:

    Image:
        source: "assets/images/link_icon.png"
        size_hint: (None, None)
        width: "100dp"
        height: "100dp"
        pos_hint: {"center_x": .46, "center_y": .78}

    Image:
        source: "assets/images/wallet_icon.png"
        size_hint: (None, None)
        width: "28dp"
        height: "28dp"
        pos_hint: {"center_x": .54, "center_y": .745}

    MDLabel:
        text: "Link a Wallet"
        font_size: "36dp"
        bold: True
        pos_hint: {"center_y": .65}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._white

    # ------------------------- account options --------------------------
    # ----- mpesa ------
    MDCard:
        md_bg_color: app._tinted
        size_hint: (.4, .18)
        pos_hint: {"center_x": .275, "center_y": .423}    
        radius: dp(23)
        padding: dp(20)
        on_release: app.change_screen_wt("add_mpesa_acc_screen", "left")

        MDRelativeLayout:
            orientation: "vertical"
            Image:
                source: "assets/images/mpesa_icon.png"
                size_hint: (.6, .6)
                pos_hint: {"center_x": .5, "center_y": .7}

            MDLabel:
                text: "M-PESA"
                font_size: "16dp"
                pos_hint: {"center_y": .15}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._white

    # ----- paypal ------
    MDCard:
        md_bg_color: app._tinted
        size_hint: (.4, .18)
        pos_hint: {"center_x": .725, "center_y": .423}  
        radius: dp(23)
        padding: dp(20)
        on_release: app.change_screen_wt("add_paypal_acc_screen", "left")

        MDRelativeLayout:
            orientation: "vertical"
            Image:
                source: "assets/images/paypal_icon.png"
                size_hint: (.6, .6)
                pos_hint: {"center_x": .5, "center_y": .7}

            MDLabel:
                text: "PayPal"
                font_size: "16dp"
                pos_hint: {"center_y": .15}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._white

    # ----- crypto -----
    MDCard:
        md_bg_color: app._tinted
        size_hint: (.4, .18)
        pos_hint: {"center_x": .275, "center_y": .21} 
        radius: dp(23)
        padding: dp(20)
        on_release: app.change_screen_wt("add_crypto_wallet_screen", "left")

        MDRelativeLayout:
            orientation: "vertical"
            Image:
                source: "assets/images/crypto_icon.png"
                size_hint: (.7, .7)
                pos_hint: {"center_x": .5, "center_y": .7}

            MDLabel:
                text: "Crypto"
                font_size: "16dp"
                pos_hint: {"center_y": .15}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._white

    # ----- card ------
    # This feature is disabled...
    
    MDCard:
        md_bg_color: app._tinted
        size_hint: (.4, .18)
        pos_hint: {"center_x": .725, "center_y": .21}           
        radius: dp(23)
        padding: dp(20)
        # on_release: app.change_screen_wt("add_card_screen", "left")

        MDRelativeLayout:
            orientation: "vertical"
            MDCard:
                background: "assets/images/card_icon1.png"
                md_bg_color: app._tinted
                size_hint: (.7, .7)
                pos_hint: {"center_x": .5, "center_y": .7}

            MDLabel:
                text: "Card\\n[size=12dp][color=a6a6a6]COMING SOON![/size]"
                markup: True
                font_size: "16dp"
                pos_hint: {"center_y": .123}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._tinted

"""

Builder.load_string(KV)

class WalletSetupScreen(MDScreen):
    pass

