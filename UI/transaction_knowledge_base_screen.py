
import threading
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from UI.reusables import TopLeftBackButton, CustomLabel, KBItem # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<TransactionKBScreen>:
    name: "tx_kb_screen"
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
                    text: "[size=18dp]  Transactions Knowledge Base[/size]"
                    bold: True

        MDBoxLayout:
            md_bg_color: app._lightgray
            size_hint: (.98, None)
            height: dp(1.8)
            pos_hint: {"center_x": .5}

        MDBoxLayout:
            orientation: "vertical"

            MDFloatLayout: 
                MDBoxLayout:
                    id: no_kb_data
                    opacity: 0
                    size_hint: (.98, 1)
                    padding: dp(11.5)
                    pos_hint: {"center_x": .5, "center_y": .5}

                    CustomLabel:
                        text: "[b][color=00afff]There's no Knowledge base for your account... Please link a wallet by tapping on the  [size=23dp][color=eeeeee]'+'[/color][/size]  Button from the Wallet screen...[/color][/b]"
                        font_size: "15dp"
                        pos_hint: {"center_y": .9}

                MDBoxLayout:
                    id: kb_data
                    opacity: 1
                    orientation: "vertical"
                    spacing: dp(11.5)
                    size_hint_x: .98
                    padding: dp(3)
                    pos_hint: {"center_x": .5, "center_y": .5}

                    MDBoxLayout:
                        orientation: "horizontal"
                        md_bg_color: app._tinted
                        size_hint: (1, None)
                        height: "90dp"
                        pos_hint: {"center_x": .5, "center_y": .73}    
                        radius: dp(11.5)
                        padding: dp(11.5)

                        MDBoxLayout:
                            size_hint: (None, 1)
                            width: dp(23)

                            MDIcon:
                                icon: "information"
                                pos_hint: {"top": .97}
                                theme_text_color: "Custom"
                                text_color: app._white

                        MDBoxLayout:
                            orientation: "vertical"
                            size_hint: (1, 1)
                            spacing: dp(3)

                            MDLabel:
                                text: "From here, you can easily edit your transaction categories based on the Knowledge base name..."
                                padding: dp(12.5), dp(0), dp(0), dp(8)
                                pos_hint: {"center_y": .5}
                                font_size: "15dp"
                                bold: True
                                halign: "left"
                                theme_text_color: "Custom"
                                text_color: app._white

                    MDBoxLayout:
                        size_hint: (.95, None)
                        height: dp(30)
                        pos_hint: {"center_x": .5}
                        radius: dp(11.5)
                        padding: dp(6.3)
                        orientation: "horizontal"

                        MDBoxLayout:
                            pos_hint: {"center_y": .5}
                            CustomLabel:
                                text: "[b]Name[/b]"

                        MDBoxLayout:
                            pos_hint: {"center_y": .5}
                            size_hint: (None, 1)
                            width: dp(170)
                            CustomLabel:
                                text: "[b]  Transaction Category[/b]"

                    MDBoxLayout:
                        orientation: "vertical"
                        size_hint: (1, 1)

                        RecycleView:
                            id: rv_kb
                            viewclass: "KBItem"
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
                                spacing: dp(0)

"""

Builder.load_string(KV)


class TransactionKBScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._green = "#2fc46c"
        self.menu = None
        self.knowledge_base = {}

        self.firebase = None
        self.id_token = None
        self.u_id = None

    def on_pre_enter(self):
        try: self.load_knowledge_base()
        except Exception: pass

    def load_knowledge_base(self):
        data = []
        app = App.get_running_app()
        parser = app.data_handler.parser

        if parser:
            self.knowledge_base = parser.sync_knowledge_base(app.data_handler.all_transactions)
            for idx, (sr_name, t_category) in enumerate(self.knowledge_base.items()):
                color = "#99999926" if idx % 2 == 0 else (.2, .2, .6, .1)
                data.append({
                    "sr_name": sr_name, "t_category": t_category, "bg_color": color
                })
            self.ids.rv_kb.data = data

    def open_category_menu(self, textfield_widget, sr_name):
        menu_items = [
            {
                "viewclass": "OneLineListItem", "text": "Friends & Family",
                "on_release": lambda x="Friends & Family": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Housing",
                "on_release": lambda x="Housing": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Utilities",
                "on_release": lambda x="Utilities": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Groceries",
                "on_release": lambda x="Groceries": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Miscellaneous",
                "on_release": lambda x="Miscellaneous": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Salary",
                "on_release": lambda x="Salary": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Investments",
                "on_release": lambda x="Investments": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Side Gigs",
                "on_release": lambda x="Side Gigs": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Other Income",
                "on_release": lambda x="Other Income": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Savings",
                "on_release": lambda x="Savings": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Savings Withdrawal",
                "on_release": lambda x="Savings Withdrawal": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Cash Withdrawal",
                "on_release": lambda x="Cash Withdrawal": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Loan Repayment",
                "on_release": lambda x="Loan Repayment": self.set_new_category(textfield_widget, sr_name, x)
            },
            {
                "viewclass": "OneLineListItem", "text": "Airtime",
                "on_release": lambda x="Airtime": self.set_new_category(textfield_widget, sr_name, x)
            }
        ]

        self.menu = MDDropdownMenu(
            caller=textfield_widget, items=menu_items, width_mult=4, max_height=dp(300)
        )
        self.menu.open()

    def set_new_category(self, textfield_widget, sr_name, new_category):
        textfield_widget.text = new_category
        if sr_name in self.knowledge_base:
            self.knowledge_base[sr_name] = new_category
            parser = App.get_running_app().data_handler.parser
            parser.knowledge_base = self.knowledge_base.copy()
            self.update_knowledge_base_in_firebase()

        for i, item in enumerate(self.ids.rv_kb.data):
            if item['sr_name'] == sr_name:
                self.ids.rv_kb.data[i]["t_category"] = new_category
                self.ids.rv_kb.refresh_from_data()
                break

        if self.menu: self.menu.dismiss()

    def update_knowledge_base_in_firebase(self):
        app = App.get_running_app()
        parser = app.data_handler.parser
        self.firebase = parser.firebase
        self.id_token = parser.id_token
        self.u_id = parser.u_id

        def update():
            if not all([self.firebase, self.id_token, self.u_id]):
                print("Missing Firebase credentials.")
                return

            if self.firebase and self.id_token and self.u_id:
                try:
                    self.firebase.put_data(
                        id_token=self.id_token,
                        path=f"users/{self.u_id}/knowledge_base",
                        data={"Knowledge Base": self.knowledge_base}
                    )
                    parser.repopulate_firebase()

                    Clock.schedule_once(lambda dt: app.show_snackbar(text="Knowledge base updated successfully", background=self._green), 0)
                except Exception: Clock.schedule_once(lambda dt: app.show_snackbar(text="Failed to sync updates..."), 0)

        threading.Thread(target=update).start()
