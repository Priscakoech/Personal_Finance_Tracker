from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import RightArrow, CustomLabel, LeftIconContainer, WidgetContainer # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<WalletScreen>:
    name: "wallet_screen"
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
            text: "Wallet"
            font_style: "H6"
            pos_hint: {"center_y": .5}
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._white

        MDIconButton:
            _no_ripple_effect: True
            icon: "assets/images/settings_icon.png"
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("settings_screen", "left")

    MDLabel:
        text: "Total Assets"
        font_size: "15dp"
        bold: True
        pos_hint: {"center_y": .78}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._gray

    MDLabel:
        text: f"[size=15dp]Ksh.[/size] {app.total_user_balance:,.2f}"
        markup: True
        font_size: "23dp"
        bold: True
        pos_hint: {"center_y": .73}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._white

    MDCard:
        md_bg_color: app._blue
        size_hint: (None, None)
        size: ("49dp", "49dp")
        pos_hint: {"center_x": .5, "center_y": .64}
        radius: self.height / 2
        ripple_behavior: True
        on_release: currency.text = "KES" if currency.text == "USD" else "USD"

        CustomLabel:
            id: currency
            text: "USD"
            font_size: "18dp"
            bold: True
            halign: "center"

    MDCard:
        md_bg_color: app._green
        background: "assets/images/bg5.jpg"
        size_hint: (1, .58)
        pos_hint: {"center_x": .5, "center_y": .29}
        radius: dp(46), dp(46), dp(0), dp(0)
        padding: dp(23)

        MDCard:
            md_bg_color: app._invisible
            size_hint: (1, .123)
            pos_hint: {"center_x": .5, "top": .98}
            padding: dp(0)
            radius: dp(0)

            MDLabel:
                text: "My wallets"
                halign: "left"
                pos_hint: {"center_y": .9}
                font_size: "16dp"
                bold: True
                theme_text_color: "Custom"
                text_color: app._white

    MDCard:
        md_bg_color: app._invisible
        size_hint: (.95, .4)
        pos_hint: {"center_x": .5, "top": .51}  
        radius: dp(0)
        padding: dp(0)

        MDScrollView:
            MDList:
                TwoLineListItem:
                    divider: None
                    _no_ripple_effect: True

                    MDCard:
                        md_bg_color: app._invisible
                        size_hint: (1, 1)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        padding: dp(6)

                        MDCard:
                            md_bg_color: app._tinted
                            padding: dp(0), dp(0), dp(10), dp(0)
                            radius: dp(11.5)
                            padding: dp(6)

                            MDBoxLayout:
                                size_hint: (None, None)
                                width: "50dp"
                                height: "50dp"
                                pos_hint: {"center_y": .5}

                                Image:
                                    source: "assets/images/mpesa_icon.png"
                                    size_hint: (1,.9)
                                    pos_hint: {"center_y": .5}

                            MDBoxLayout:
                                orientation: "vertical"
                                padding: dp(11.5)

                                MDLabel:
                                    text: "M-PESA\\n[color=a6a6a6][b][size=11sp]0795923160[/size][/b]"
                                    markup: True
                                    halign: "left"
                                    font_style: "Subtitle1"
                                    theme_text_color: "Custom"
                                    text_color: app._white

                            MDBoxLayout:
                                MDLabel:
                                    text: "[size=13sp]Ksh. 128.57\\n[color=a6a6a6]$ 1.00[/size]"
                                    markup: True
                                    pos_hint: {"center_x": .5, "center_y": .5}
                                    halign: "right"
                                    theme_text_color: "Custom"
                                    text_color: app._white

                TwoLineListItem:
                    divider: None
                    _no_ripple_effect: True

                    MDCard:
                        md_bg_color: app._invisible
                        size_hint: (1, 1)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        padding: dp(6)

                        MDCard:
                            md_bg_color: app._tinted
                            padding: dp(0), dp(0), dp(10), dp(0)
                            radius: dp(11.5)
                            padding: dp(6)

                            MDBoxLayout:
                                size_hint: (None, None)
                                size: ("50dp", "50dp")
                                pos_hint: {"center_y": .5}

                                Image:
                                    source: "assets/images/paypal_icon.png"
                                    size_hint: (1,.9)
                                    pos_hint: {"center_y": .5}

                            MDBoxLayout:
                                orientation: "vertical"
                                padding: dp(11.5)

                                MDLabel:
                                    text: "PayPal\\n[color=a6a6a6][b][size=11sp]dav***@gmail.com[/size][/b]"
                                    markup: True
                                    halign: "left"
                                    font_style: "Subtitle1"
                                    theme_text_color: "Custom"
                                    text_color: app._white

                            MDBoxLayout:
                                MDLabel:
                                    text: "[size=13sp]Ksh. 128.57\\n[color=a6a6a6]$ 1.00[/size]"
                                    markup: True
                                    pos_hint: {"center_x": .5, "center_y": .5}
                                    halign: "right"
                                    theme_text_color: "Custom"
                                    text_color: app._white

    # add wallet btn
    MDCard:
        md_bg_color: app._white
        size_hint: (.9, .07)
        pos_hint: {"center_x": .5, "center_y": .08}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: True

        MDRectangleFlatIconButton:
            icon: "plus"
            icon_text_color: "Custom"
            icon_color: app._dark
            text: "  Add Wallet"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._dark
            font_size: "22dp"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.change_screen_wt("wallet_setup_screen", "left")

"""

Builder.load_string(KV)


class WalletScreen(MDScreen):
    pass
