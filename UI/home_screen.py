
import threading
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.screen import MDScreen
from UI.text_insight_screen import InsightScreen1
from UI.visual_insight_screen import InsightScreen2
from UI.reusables import CustomPieChart, CustomTwoLineListItem, KeyItem, CustomLabel, NavIconButton, WidgetContainer, LeftIconContainer, RightArrow, TopLeftBackButton # noqa
from BACKEND.data_handler import DataHandler
# The "# noqa" comment suppresses the 'UNUSED IMPORT' Warnings! 🙂🙂

KV = """
<MySwiper@MDSwiperItem>
    md_bg_color: app._lightgray
    radius: dp(11.5)

<HomeScreen>:
    name: "home_screen"
    md_bg_color: app._dark
    on_leave: bottom_nav.current = ""

    MDBottomNavigation:
        id: bottom_nav
        panel_color: app._tinted
        selected_color_background: app._tinted
        text_color_active: app._white

        MDBottomNavigationItem:
            name: "home_tab"
            text: "Home"
            icon: "assets/images/home_icon.png"
            on_tab_release: bottom_nav.current = f"{self.name}"

            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(1.63)

                # Custom Top App Bar
                MDCard:
                    size_hint: (1, None)
                    height: dp(59)
                    radius: dp(0)
                    elevation: 2
                    shadow_radius: 11.5
                    shadow_softness: 11.5
                    shadow_color: app._blue
                    pos_hint: {"top": 1}
                    md_bg_color: app._dark
                    padding: dp(17.5)

                    MDBoxLayout:
                        size_hint: (None, None)
                        size: ("38dp", "38dp")
                        radius: self.height / 2
                        pos_hint: {"center_y": .5}
                        line_color: app._blue

                        MDCard:
                            size_hint: (1, 1)
                            radius: self.height / 2
                            on_release: app.switch_screen("personal_info_screen")

                            FitImage:
                                id: home_dp
                                source: app.profile_photo
                                radius: root.height / 2

                    MDBoxLayout:
                        size_hint: (1, 1)
                        padding: dp(8), dp(0), dp(0), dp(0)

                        CustomLabel:
                            id: greetings
                            text: f"[color=a6a6a6]{app.greeting_text()}[/color] [size=18dp]{app.full_name}[/size]"
                            bold: True

                    MDBoxLayout:
                        size_hint: (None, None)
                        size: ("38dp", "38dp")
                        pos_hint: {"center_y": .5}

                        MDIconButton:
                            _no_ripple_effect: True
                            icon: "assets/images/settings_icon.png"
                            pos_hint: {"center_y": .5}
                            on_release: app.switch_screen("settings_screen")

                # Content
                MDBoxLayout:
                    md_bg_color: app._dark
                    orientation: "vertical"
                    padding: dp(0), dp(10), dp(0), dp(8)
                    spacing: dp(12.5)

                    MDBoxLayout:
                        md_bg_color: app._lightgray
                        size_hint: (.95, None)
                        height: dp(75)
                        pos_hint: {"center_x": .5}
                        radius: dp(11.5)
                        padding: dp(6.3)

                        MDBoxLayout:
                            orientation: "vertical"

                            CustomLabel:
                                text: "[b]Balance[/b]"
                                text_color: "#ffffff"

                            CustomLabel:
                                id: overview_balance
                                text: f"[size=14dp]Ksh.[/size] {root.kes_user_balance:,.2f}"
                                font_size: "20dp"
                                text_color: "#ffffff"

                        MDBoxLayout:
                            size_hint: (None, 1)
                            width: dp(145)

                            MDRoundFlatIconButton:
                                icon: "eye-off"
                                text: "Hide Balance"
                                size_hint_x: 1
                                line_color: app._blue
                                theme_text_color: "Custom"
                                text_color: app._white
                                icon_color: app._white
                                on_release:
                                    self.icon = "eye" if self.icon == "eye-off" else "eye-off"
                                    self.text = "Show Balance" if self.text == "Hide Balance" else "Hide Balance"
                                    overview_balance.text = f"[size=14dp]Ksh.[/size] *.**" if overview_balance.text == f"[size=14dp]Ksh.[/size] {root.kes_user_balance:,.2f}" else f"[size=14dp]Ksh.[/size] {root.kes_user_balance:,.2f}"

                    MDBoxLayout:
                        size_hint: (1, None)
                        height: dp(230)
                        pos_hint: {"center_x": .5}
                        radius: dp(0)

                        MDSwiper:
                            size_hint: (1, 1)
                            items_spacing: dp(11.5)

                            MySwiper:
                                MDBoxLayout:
                                    orientation: "horizontal"
                                    padding: dp(6)
                                    spacing: dp(8)

                                    MDFloatLayout:
                                        size_hint: (None, None)
                                        size: ("160dp", "160dp")
                                        pos_hint: {"center_y": .5}

                                        MDBoxLayout:
                                            id: spending_pie_chart
                                            opacity: 1
                                            size_hint: (1, 1)
                                            pos_hint: {"center_x": .5, "center_y": .5}

                                        MDBoxLayout:
                                            id: no_spending_data_txt
                                            opacity: 0
                                            size_hint: (1, 1)
                                            padding: dp(6)
                                            pos_hint: {"center_x": .5, "center_y": .5}

                                            CustomLabel:
                                                text: "[b][color=00afff]There's nothing to display. Please add an account...[/color][/b]"
                                                font_size: "12dp"

                                    MDBoxLayout:
                                        orientation: "vertical"
                                        size_hint: (1, .88)
                                        pos_hint: {"center_y": .5}

                                        MDBoxLayout:
                                            md_bg_color: app._red
                                            size_hint: (1, .4)
                                            radius: dp(11.5), dp(11.5), dp(0), dp(0)
                                            padding: dp(6)

                                            CustomLabel:
                                                text: f"[size=12dp]Total Expenditure[/size]\\n[size=11dp]Ksh.[/size] [b]{root.total_expenditure:,.2f}[/b]"
                                                text_color: "#ffffff"

                                        MDBoxLayout:
                                            orientation: "vertical"
                                            spacing: dp(6)
                                            padding: dp(1), dp(11.5), dp(0), dp(0)

                                            KeyItem:
                                                key_color: "#f28500"
                                                key_text: "Friends & Family"

                                            KeyItem:
                                                key_color: "#8887f1"
                                                key_text: "Housing"

                                            KeyItem:
                                                key_color: "#ffd046"
                                                key_text: "Utilities"

                                            KeyItem:
                                                key_color: "#e78777"
                                                key_text: "Groceries"

                                            KeyItem:
                                                key_color: "#bed09c"
                                                key_text: "Miscellaneous"

                                            MDBoxLayout:

                            MySwiper:
                                MDBoxLayout:
                                    orientation: "horizontal"
                                    padding: dp(6)
                                    spacing: dp(8)

                                    MDFloatLayout:
                                        size_hint: (None, None)
                                        size: ("160dp", "160dp")
                                        pos_hint: {"center_y": .5}

                                        MDBoxLayout:
                                            id: income_pie_chart
                                            opacity: 1
                                            size_hint: (1, 1)
                                            pos_hint: {"center_x": .5, "center_y": .5}

                                        MDBoxLayout:
                                            id: no_income_data_txt
                                            opacity: 0
                                            size_hint: (1, 1)
                                            padding: dp(6)
                                            pos_hint: {"center_x": .5, "center_y": .5}

                                            CustomLabel:
                                                text: "[b][color=00afff]There's nothing to display. Please add an account...[/color][/b]"
                                                font_size: "12dp"

                                    MDBoxLayout:
                                        orientation: "vertical"
                                        size_hint: (1, .88)
                                        pos_hint: {"center_y": .5}

                                        MDBoxLayout:
                                            md_bg_color: app._green
                                            size_hint: (1, .4)
                                            radius: dp(11.5), dp(11.5), dp(0), dp(0)
                                            padding: dp(6)

                                            CustomLabel:
                                                text: f"[size=12dp]Total Income[/size]\\n[size=11dp]Ksh.[/size] [b]{root.total_income:,.2f}[/b]"
                                                text_color: app._dark

                                        MDBoxLayout:
                                            orientation: "vertical"
                                            spacing: dp(6)
                                            padding: dp(1), dp(11.5), dp(0), dp(0)

                                            KeyItem:
                                                key_color: "#f28500"
                                                key_text: "Friends & Family"

                                            KeyItem:
                                                key_color: "#66dd66"
                                                key_text: "Salary"

                                            KeyItem:
                                                key_color: "#90d3c2"
                                                key_text: "Investments"

                                            KeyItem:
                                                key_color: "#66ac85"
                                                key_text: "Side Gigs"

                                            KeyItem:
                                                key_color: "#37c3ea"
                                                key_text: "Other Income"

                                            MDBoxLayout:

                    MDCard:
                        orientation: "vertical"
                        md_bg_color: app._green
                        background: "assets/images/bg5.jpg"
                        size_hint: (.95, None)
                        height: dp(175)
                        pos_hint: {"center_x": .5}
                        radius: dp(23)
                        padding: dp(11.5)
                        spacing: dp(8)

                        MDBoxLayout:
                            size_hint: (1, None)
                            height: dp(48)
                            pos_hint: {"center_x": .5}
                            padding: dp(3)

                            CustomLabel:
                                text: "Recent Transaction"
                                bold: True

                            MDBoxLayout:
                                md_bg_color: app._invisible
                                size_hint: (None, 1)
                                width: "123dp"

                                MDCard:
                                    md_bg_color: app._invisible
                                    size: (1, 1)
                                    on_release: app.switch_screen("transactions_screen")

                                    CustomLabel:
                                        padding: dp(6)
                                        text: "[b]View all[/b]"
                                        halign: "right"
                                        text_color: app._gray

                                    MDIcon:
                                        icon: "chevron-right"
                                        halign: "right"
                                        pos_hint: {"center_y": .5}
                                        theme_text_color: "Custom"
                                        text_color: app._gray

                        MDFloatLayout: 
                            MDBoxLayout:
                                id: no_recent_tx_data_txt
                                opacity: 0
                                size_hint: (1, 1)
                                padding: dp(6)
                                pos_hint: {"center_x": .5, "center_y": .5}

                                CustomLabel:
                                    text: "[b][color=00afff]There's nothing to display. Please add an account...[/color][/b]"
                                    font_size: "14dp"

                            RecentTransaction:
                                id: recent_tx_data
                                opacity: 1

                    WidgetContainer:
                        md_bg_color: "#aaaaaa26"
                        size_hint_x: .95
                        size_hint_max_y: dp(70)
                        pos_hint: {"center_x": .5}
                        on_release: app.switch_screen("reports_screen")
                        padding: dp(6), dp(6), dp(16), dp(6)

                        LeftIconContainer:
                            Image:
                                source:  "assets/images/reports_icon.png"
                                pos_hint: {"center_x": .5, "center_y": .5}
                                size_hint: (.53, .63)

                        MDBoxLayout:
                            CustomLabel:
                                text: " [b]Financial Reports[/b]"

                        RightArrow:

        MDBottomNavigationItem:
            name: "wallet_tab"
            text: "Wallet"
            icon: "assets/images/wallet_icon.png"
            on_tab_release: bottom_nav.current = f"{self.name}"

            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(1.63)

                # Custom Top App Bar
                MDCard:
                    size_hint: (1, None)
                    height: dp(59)
                    radius: dp(0)
                    elevation: 2
                    shadow_radius: 11.5
                    shadow_softness: 11.5
                    shadow_color: app._blue
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
                            text: "[size=18dp]Wallet[/size]"
                            bold: True
                            halign: "center"

                    MDBoxLayout:
                        size_hint: (None, None)
                        size: ("38dp", "38dp")
                        pos_hint: {"center_y": .5}

                        MDIconButton:
                            _no_ripple_effect: True
                            icon: "assets/images/settings_icon.png"
                            pos_hint: {"center_y": .5}
                            on_release: app.switch_screen("settings_screen")

                # Content
                MDBoxLayout:
                    md_bg_color: app._dark
                    orientation: "vertical"
                    padding: dp(0), dp(10), dp(0), dp(11.5)
                    spacing: dp(12.5)

                    MDBoxLayout:
                        md_bg_color: app._lightgray
                        size_hint: (.95, None)
                        height: dp(136)
                        pos_hint: {"center_x": .5}
                        radius: dp(11.5)
                        padding: dp(6.3)

                        MDBoxLayout:
                            orientation: "vertical"
                            padding: dp(0), dp(10), dp(0), dp(0)

                            CustomLabel:
                                text: "[b]Total Assets[/b]"

                            Spacer:

                            CustomLabel:
                                id: kes_assets_value
                                text: f"[size=15dp]Ksh.[/size] {root.kes_user_balance:,.2f}"
                                font_size: "21dp"
                                bold: True
                                text_color: "#ffffff"

                            CustomLabel:
                                id: usd_assets_value
                                text: f"[color=00afff]≈ [size=18dp]$ [/size] {root.usd_user_balance:,.2f}[/color]"
                                font_size: "15dp"
                                bold: True

                        MDBoxLayout:
                            size_hint: (None, 1)
                            width: dp(145)

                            MDRoundFlatIconButton:
                                icon: "eye-off"
                                text: "Hide Balance"
                                size_hint_x: 1
                                line_color: app._blue
                                theme_text_color: "Custom"
                                text_color: app._white
                                icon_color: app._white
                                on_release:
                                    self.icon = "eye" if self.icon == "eye-off" else "eye-off"
                                    self.text = "Show Balance" if self.text == "Hide Balance" else "Hide Balance"
                                    kes_assets_value.text = f"[size=15dp]Ksh.[/size] *.**" if kes_assets_value.text == f"[size=15dp]Ksh.[/size] {root.kes_user_balance:,.2f}" else f"[size=15dp]Ksh.[/size] {root.kes_user_balance:,.2f}"
                                    usd_assets_value.text = f"≈ [size=18dp]$ [/size] -.--" if usd_assets_value.text == f"[color=00afff]≈ [size=18dp]$ [/size] {root.usd_user_balance:,.2f}[/color]" else f"[color=00afff]≈ [size=18dp]$ [/size] {root.usd_user_balance:,.2f}[/color]"

                    MDBoxLayout:
                        md_bg_color: app._tinted
                        size_hint: (.98, None)
                        height: dp(.8)
                        pos_hint: {"center_x": .5}

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
                                text: "[b]My Wallets[/b]"

                    MDFloatLayout: 
                        MDBoxLayout:
                            id: no_wallet_data_txt
                            opacity: 0
                            size_hint: (.98, 1)
                            padding: dp(11.5)
                            pos_hint: {"center_x": .5, "center_y": .5}

                            CustomLabel:
                                text: "[b][color=00afff]There's nothing to display. Please link a wallet by tapping on the  [size=23dp][color=eeeeee]'+'[/color][/size]  Button...[/color][/b]"
                                font_size: "15dp"
                                pos_hint: {"center_y": .9}

                        MDBoxLayout:
                            id: wallet_data
                            opacity: 1
                            size_hint_x: .98
                            padding: dp(3)
                            pos_hint: {"center_x": .5, "center_y": .5}

                            MDScrollView:
                                effect_cls: "ScrollEffect"
                                MDList:
                                    id: all_wallets

                    MDBoxLayout:
                        orientation: "horizontal"
                        size_hint: (.95, None)
                        height: dp(50)
                        padding: dp(0), dp(-32), dp(0), dp(0)

                        MDBoxLayout:
                            size_hint: (1, 1)

                        MDCard:
                            ripple_behavior: True
                            md_bg_color: app._blue
                            size_hint: (None, None)
                            size: ("56dp", "56dp")
                            radius: dp(17.5)
                            pos_hint: {"center_y": .5}
                            padding: dp(16)
                            on_release: app.switch_screen("wallet_setup_screen")

                            MDIcon:
                                icon: "plus"
                                pos_hint: {"center_y": .5}   

        MDBottomNavigationItem:
            name: "insights_tab"
            text: "Insights"
            icon: "assets/images/insight.png"
            on_tab_release: bottom_nav.current = f"{self.name}"

            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(1.63)

                # Custom Top App Bar
                MDCard:
                    size_hint: (1, None)
                    height: dp(59)
                    radius: dp(0)
                    elevation: 2
                    shadow_radius: 11.5
                    shadow_softness: 11.5
                    shadow_color: app._blue
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
                            text: "[size=18dp]Insights[/size]"
                            bold: True
                            halign: "center"

                    MDBoxLayout:
                        size_hint: (None, None)
                        size: ("38dp", "38dp")
                        pos_hint: {"center_y": .5}

                        MDIconButton:
                            _no_ripple_effect: True
                            icon: "assets/images/settings_icon.png"
                            pos_hint: {"center_y": .5}
                            on_release: app.switch_screen("settings_screen")

                # Content
                MDBoxLayout:
                    md_bg_color: app._dark
                    orientation: "vertical"
                    padding: dp(0), dp(10), dp(0), dp(8)
                    spacing: dp(12.5)

                    MDBoxLayout:
                        md_bg_color: app._lightgray
                        size_hint: (.95, None)
                        height: dp(50)
                        pos_hint: {"center_x": .5}
                        orientation: "horizontal"
                        spacing: dp(8)
                        padding: dp(8)
                        radius: dp(11.5)

                        MDCard:
                            id: text_insights_tab
                            md_bg_color: app._blue
                            size_hint: (1, 1)
                            radius: dp(12)
                            on_release: 
                                self.md_bg_color = app._blue if visual_insights_tab.md_bg_color == app._blue else  app._blue
                                visual_insights_tab.md_bg_color = app._invisible
                                root.switch_insight_category("insight_screen1")

                            CustomLabel:
                                text: "[b]Text-Based Insights[/b]"
                                halign: "center"
                                text_color: "#ffffff"

                        MDCard:
                            id: visual_insights_tab
                            md_bg_color: app._invisible
                            size_hint: (1, 1)
                            radius: dp(12)
                            on_release: 
                                self.md_bg_color = app._blue if text_insights_tab.md_bg_color == app._blue else  app._blue
                                text_insights_tab.md_bg_color = app._invisible
                                root.switch_insight_category("insight_screen2")

                            CustomLabel:
                                text: "[b]Visual Insights[/b]"
                                halign: "center"
                                text_color: "#ffffff"

                    MDScreenManager:
                        id: insight_section_screen_manager

"""

Builder.load_string(KV)


class HomeScreen(MDScreen):
    kes_user_balance, usd_user_balance = NumericProperty(0.00), NumericProperty(0.00)
    total_expenditure, total_income = NumericProperty(0.00), NumericProperty(0.00)

    def __init__(self, user_data_store=None, text_insights_store=None, **kwargs):
        super().__init__(**kwargs)
        self._dark = "#00001fff"
        self.user_data_store = user_data_store
        self.text_insights_store = text_insights_store
        self.firebase = None
        self.id_token = None
        self.u_id = None

    def on_enter(self, *args):
        try:
            Clock.schedule_once(lambda dt: self.load_recent_transaction(), 0)
            Clock.schedule_once(lambda dt: self.load_wallets(), 0)
            Clock.schedule_once(lambda dt: self.load_spending_income_totals(), 0)
            Clock.schedule_once(lambda dt: self.refresh_piecharts(), 0)
            if not hasattr(self, 'insight_screens_loaded'):
                self.ids.insight_section_screen_manager.add_widget(InsightScreen1(data_handler=DataHandler(), user_data_store=self.user_data_store, text_insights_store=self.text_insights_store))
                self.ids.insight_section_screen_manager.add_widget(InsightScreen2())
                self.insight_screens_loaded = True

        except Exception: pass

    def refresh_piecharts(self):
        def fetch_data():
            app = App.get_running_app()
            parser = app.data_handler.parser
            self.firebase = parser.firebase
            self.id_token = parser.id_token
            self.u_id = parser.u_id

            if not all([self.firebase, self.id_token, self.u_id]):
                print("Missing Firebase credentials.")
                return

            try:
                parsed_data = self.firebase.get_data(
                    id_token=self.id_token,
                    path=f"users/{self.u_id}/parsed_data/mpesa_account"
                )
                if parsed_data and "Piechart Data" in parsed_data:
                    pie_data = parsed_data["Piechart Data"]
                    spending_data = pie_data.get("Spending", {" ": 100, "  ": 0, "   ": 0, "    ": 0, "     ": 0})
                    income_data = pie_data.get("Income", {" ": 100, "  ": 0, "   ": 0, "    ": 0, "     ": 0})

                    # the "p" means percentages, "s" means spending, "i" means income
                    spending_p_values_rounded = self.get_piechart_round_data(spending_data, target_type="expense")
                    spending_p_values = self.format_piechart_data(spending_p_values_rounded, target_type="expense")
                    income_p_values_rounded = self.get_piechart_round_data(income_data, target_type="income")
                    income_p_values = self.format_piechart_data(income_p_values_rounded, target_type="income")

                    def update_ui(dt):
                        segment_s_colors = ["#f28500", "#8887f1", "#ffd046", "#e78777", "#bed09c"]
                        segment_i_colors = ["#f28500", "#66dd66", "#90d3c2", "#66ac85", "#37c3ea"]
                        self.load_pie_chart(spending_p_values, "spending", segment_s_colors)
                        self.load_pie_chart(income_p_values, "income", segment_i_colors)

                    Clock.schedule_once(update_ui)

            except Exception: pass

        threading.Thread(target=fetch_data).start()

    def format_piechart_data(self, data_dict, target_type="expense"):
        if target_type == "expense":
            preferred_order = ["Friends & Family", "Housing", "Utilities", "Groceries", "Miscellaneous"]
            custom_keys = [" ", "  ", "   ", "    ", "     "]
        else:
            preferred_order = ["Friends & Family", "Salary", "Investments", "Side Gigs", "Other Income"]
            custom_keys = [" ", "  ", "   ", "    ", "     "]

        result = {}
        for label, custom_key in zip(preferred_order, custom_keys):
            result[custom_key] = data_dict.get(label, 0)

        return [result]

    def get_piechart_round_data(self, data_dict, target_type="expense"):
        """Always make pie chart values to sum up to 100"""
        if target_type == "expense":
            preferred_order = ["Friends & Family", "Housing", "Utilities", "Groceries", "Miscellaneous"]
        else:
            preferred_order = ["Friends & Family", "Salary", "Investments", "Side Gigs", "Other Income"]

        clean_data = {key: data_dict.get(key, 0) for key in preferred_order}
        total = sum(clean_data.values())

        if total == 0:
            return {key: 100 // len(preferred_order) for key in preferred_order}

        rounded_data = {}
        running_total = 0
        for i, key in enumerate(preferred_order):
            value = clean_data[key]
            percent = round((value / total) * 100)
            if i == len(preferred_order) - 1:
                percent = 100 - running_total
            rounded_data[key] = percent
            running_total += percent

        return rounded_data

    def load_recent_transaction(self):
        all_tx = App.get_running_app().data_handler.transactions().get("all", [])
        if all_tx:
            recent_transaction = all_tx[0]
            self.ids.recent_tx_data.left_text = recent_transaction["sr_name"]
            self.ids.recent_tx_data.right_text = recent_transaction["amount"]
            self.ids.recent_tx_data.t_time = recent_transaction["t_time"]
            self.ids.recent_tx_data.icon_path = recent_transaction["acc_type"]

        else: pass

    def load_spending_income_totals(self):
        app = App.get_running_app()
        parser = app.data_handler.parser
        self.firebase = parser.firebase
        self.id_token = parser.id_token
        self.u_id = parser.u_id
        try:
            parsed_data = self.firebase.get_data(
                id_token=self.id_token,
                path=f"users/{self.u_id}/parsed_data/mpesa_account"
            )

            if parsed_data:
                income_totals = parsed_data.get("General Insight", {}).get("Income", {})
                expense_totals = parsed_data.get("General Insight", {}).get("Expense", {})

                self.total_income = sum(income_totals.values())
                self.total_expenditure = sum(expense_totals.values())

        except Exception: pass

    def load_pie_chart(self, pie_chart_data, pie_chart_type, pie_chart_colors):
        """
        pie_chart_data is a list of percentages for either spending or income categories...,
        pie_chart_type is either "spending" or "income",
        pie_chart_color is a list of pie chart's segment colors,
        """

        chart_container = None
        if pie_chart_type == "spending": chart_container = self.ids.spending_pie_chart
        elif pie_chart_type == "income": chart_container = self.ids.income_pie_chart

        pie_chart = CustomPieChart(
            items=pie_chart_data, pos_hint={"center_x": .5, "center_y": .5}, size_hint=(1, 1)
        )

        pie_chart.order = False
        pie_chart.custom_colors = pie_chart_colors
        chart_container.clear_widgets()
        chart_container.add_widget(pie_chart)

    def load_wallets(self):
        parser = App.get_running_app().data_handler.parser
        if parser:
            wallet_data = parser.get_mpesa_wallet_details()
            wallet_widget = CustomTwoLineListItem(
                icon_path=wallet_data["wallet_details"]["mpesa"]["icon_path"],
                left_text=wallet_data["wallet_details"]["mpesa"]["left_text"],
                right_text=wallet_data["wallet_details"]["mpesa"]["right_text"]
            )

            self.ids.all_wallets.clear_widgets()
            self.ids.all_wallets.add_widget(wallet_widget)
            self.kes_user_balance, self.usd_user_balance = wallet_data["kes_bal"], wallet_data["usd_bal"]

    def switch_insight_category(self, screen_name):
        self.ids.insight_section_screen_manager.transition = FadeTransition(duration=.2, clearcolor=self._dark)
        self.ids.insight_section_screen_manager.current = screen_name
