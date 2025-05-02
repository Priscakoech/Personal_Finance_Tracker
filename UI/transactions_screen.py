
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton, CustomTabs, Tab, Spacer, InsightCard, AllTransactionsCard, RV # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """
<TransactionsScreen>:
    name: "transactions_screen"
    md_bg_color: app._dark

    MDBoxLayout:
        orientation: "vertical"

        # Custom Top App Bar
        MDCard:
            size_hint: (1, None)
            height: dp(59)
            radius: dp(0)
            pos_hint: {"top": 1}
            md_bg_color: app._dark
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
                    text: "[size=18dp]Transactions[/size]"
                    bold: True
                    halign: "center"

            MDBoxLayout:
                size_hint: (None, None)
                size: ("39dp", "37dp")
                pos_hint: {"center_y": .5}
                radius: self.height / 2
                line_color: app._white

                MDIconButton:
                    size_hint: (1, 1)
                    _no_ripple_effect: True
                    icon: "assets/images/knowledge_base.png"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: app.switch_screen("tx_kb_screen")

        MDBoxLayout:
            md_bg_color: app._lightgray
            size_hint: (.98, None)
            height: dp(1.8)
            pos_hint: {"center_x": .5}

        MDCard:
            md_bg_color: app._invisible
            size_hint: (.9, .85)
            pos_hint: {"center_x": .5, "top": .85}    
            radius: dp(11.5)

            CustomTabs:
                Tab:
                    title: "All"

                    InsightCard:
                        orientation: "vertical"
                        MDBoxLayout:
                            id: empty_label_all
                            size_hint_y: None
                            height: self.minimum_height

                            CustomLabel:
                                padding: dp(0), dp(80), dp(0), dp(0)
                                text: "[size=19dp][b]There's Nothing to Display yet![/b][/size]"

                        RV:
                            id: rv_all
                            viewclass: 'AllTransactionsCard'
                            scroll_type: ['bars', 'content']
                            bar_width: dp(3)
                            do_scroll_x: False
                            do_scroll_y: True
                            effect_cls: "ScrollEffect"

                            RecycleBoxLayout:
                                default_size: None, None
                                default_size_hint: 1, None
                                size_hint_y: None
                                height: self.minimum_height
                                orientation: 'vertical'
                                spacing: dp(11.5)

                Tab:
                    title: "M-PESA"

                    InsightCard:
                        orientation: "vertical"
                        MDBoxLayout:
                            id: empty_label_mpesa
                            size_hint_y: None
                            height: self.minimum_height

                            CustomLabel:
                                padding: dp(0), dp(80), dp(0), dp(0)
                                text: "[size=19dp][b]There's Nothing to Display yet![/b][/size]"

                        RV:
                            id: rv_mpesa
                            viewclass: 'AllTransactionsCard'
                            scroll_type: ['bars', 'content']
                            bar_width: dp(2)
                            do_scroll_x: False
                            do_scroll_y: True
                            effect_cls: "ScrollEffect"

                            RecycleBoxLayout:
                                default_size: None, None
                                default_size_hint: 1, None
                                size_hint_y: None
                                height: self.minimum_height
                                orientation: 'vertical'
                                spacing: dp(11.5)

                Tab:
                    title: "Crypto"

                    InsightCard:
                        orientation: "vertical"
                        MDBoxLayout:
                            id: empty_label_crypto
                            size_hint_y: None
                            height: self.minimum_height

                            CustomLabel:
                                padding: dp(0), dp(80), dp(0), dp(0)
                                text: "[size=19dp][b]There's Nothing to Display yet![/b][/size]"

                        RV:
                            id: rv_crypto
                            viewclass: 'AllTransactionsCard'
                            scroll_type: ['bars', 'content']
                            bar_width: dp(2)
                            do_scroll_x: False
                            do_scroll_y: True
                            effect_cls: "ScrollEffect"

                            RecycleBoxLayout:
                                default_size: None, None
                                default_size_hint: 1, None
                                size_hint_y: None
                                height: self.minimum_height
                                orientation: 'vertical'
                                spacing: dp(11.5)

                Tab:
                    title: "PayPal"

                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        effect_cls: "ScrollEffect" 

                        MDBoxLayout:
                            id: paypal_transactions
                            size_hint_y: None
                            height: self.minimum_height

                            CustomLabel:
                                padding: dp(0), dp(80), dp(0), dp(0)
                                text: "[size=19dp][b]This option is not yet available, but it's on the way. Stay tuned for updates![/b][/size]"

                Tab:
                    title: "Card"

                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        effect_cls: "ScrollEffect" 

                        MDBoxLayout:
                            id: card_transactions
                            size_hint_y: None
                            height: self.minimum_height

                            CustomLabel:
                                padding: dp(0), dp(80), dp(0), dp(0)
                                text: "[size=19dp][b]This option is not yet available, but it's on the way. Stay tuned for updates![/b][/size]"

"""

Builder.load_string(KV)


class TransactionsScreen(MDScreen):
    def update_transaction_tab(self, rv_id, empty_label_id, data_list):
        rv, label = self.ids[rv_id], self.ids[empty_label_id]
        if not data_list:
            label.opacity = 1
            rv.data = []
        else:
            label.opacity = 0
            rv.data = [
                {
                    "sr_name": i["sr_name"],
                    "amount": i["amount"],
                    "t_time": i["t_time"],
                    "acc_type": i["acc_type"],
                    "t_id": i["t_id"],
                    "t_fee": i["t_fee"],
                    "sender_acc": i["sender_acc"],
                    "receiver_acc": i["receiver_acc"],
                    "t_category": i["t_category"]
                }
                for i in data_list
            ]

    def on_pre_enter(self):
        app = App.get_running_app()
        try:
            parser = app.data_handler.parser
            parser.knowledge_base = parser.sync_knowledge_base(parser.formatted_transactions)
            for tx in parser.formatted_transactions: parser.override_with_kb(tx)
            transactions = app.data_handler.transactions()

            Clock.schedule_once(lambda dt: self.update_transaction_tab("rv_all", "empty_label_all", transactions["all"]), 0)
            Clock.schedule_once(lambda dt: self.update_transaction_tab("rv_mpesa", "empty_label_mpesa", transactions["mpesa"]), 0)
            Clock.schedule_once(lambda dt: self.update_transaction_tab("rv_crypto", "empty_label_crypto", transactions["crypto"]), 0)

        except Exception: pass
