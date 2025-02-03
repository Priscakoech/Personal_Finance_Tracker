from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton, CustomTabs, Tab, InsightCard # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<TransactionsScreen>:
    name: "transactions_screen"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .95}    
        radius: dp(11.5)

        TopLeftBackButton:
            pos_hint: {"center_y": .5}

        MDLabel:
            padding: (23, 0)
            text: "Transactions"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: app._white
            pos_hint: {"center_y": .5}
            halign: "center"

        MDIconButton:
            _no_ripple_effect: True
            icon: "assets/images/settings_icon.png"
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("settings_screen", "left")

    MDCard:
        md_bg_color: app._invisible
        size_hint: (.9, .85)
        pos_hint: {"center_x": .5, "top": .83}    
        radius: dp(11.5)

        CustomTabs:
            Tab:
                title: "All"
    
                MDScrollView:
                    do_scroll_x: False
                    do_scroll_y: True
    
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(20)
                        adaptive_height: True
    
                        # Example for Today's Date
                        MDLabel:
                            text: "Tuesday, 4th February, 2025"
                            font_style: "H6"
                            halign: "left"
                            size_hint_y: None
                            height: dp(46)
    
                        MDCard:
                            md_bg_color: app._green
                            size_hint: (1, None)
                            height: dp(120)
                            radius: dp(11.5)
                            padding: dp(10)
                            BoxLayout:
                                orientation: "vertical"
                                MDLabel:
                                    text: "Transaction ID: 12345"
                                    font_style: "Body1"
                                MDLabel:
                                    text: "+ 100.00"
                                    font_style: "H5"
                                MDLabel:
                                    text: "From: Prisca Koech"
                                    font_style: "Body2"
                                MDLabel:
                                    text: "AT: 09:45 AM"
                                    font_style: "Caption"
    
                        # Another Transaction for Today
                        MDCard:
                            md_bg_color: app._blue
                            size_hint: (1, None)
                            height: dp(120)
                            radius: dp(11.5)
                            line_color: app._white
                            padding: dp(10)
                            BoxLayout:
                                orientation: "vertical"
                                MDLabel:
                                    text: "Transaction ID: 54321"
                                    font_style: "Body1"
                                    theme_text_color: "Primary"
                                MDLabel:
                                    text: "Amount: ksh. 75.00"
                                    font_style: "Body2"
                                    theme_text_color: "Secondary"
                                MDLabel:
                                    text: "Time: 12:30 PM"
                                    font_style: "Caption"
                                    theme_text_color: "Hint"
    
                        # Example for Yesterday's Date
                        MDLabel:
                            text: "3rd February, Monday, 2025"
                            font_style: "H6"
                            halign: "center"
                            size_hint_y: None
                            height: dp(40)
    
                        MDCard:
                            md_bg_color: app._red
                            size_hint: (1, None)
                            height: dp(120)
                            radius: dp(11.5)
                            line_color: app._white
                            padding: dp(10)
                            BoxLayout:
                                orientation: "vertical"
                                MDLabel:
                                    text: "Transaction ID: 67890"
                                    font_style: "Body1"
                                MDLabel:
                                    text: "Amount: $100.00"
                                    font_style: "Body2"
                                MDLabel:
                                    text: "Time: 03:00 PM"
                                    font_style: "Caption"
                                    
                        Widget:  # Spacer to prevent disappearing content
                            size_hint_y: None
                            height: dp(50)


            Tab:
                title: "M-PESA"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            id: mpesa_transactions
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "PayPal"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            id: paypal_transactions
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "Card"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            id: card_transactions
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "Crypto"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            id: crypto_transactions
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

"""

Builder.load_string(KV)


class TransactionsScreen(MDScreen):
    pass
