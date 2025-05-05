
import threading
from datetime import datetime
from calendar import monthrange
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen
from kivymd_extensions.akivymd.uix.charts import AKBarChart, AKLineChart
from UI.reusables import InsightScreenTopBar, InsightCard, CustomCard, CustomCardLayout, CustomCardIdentifier, CustomCardTitleBar, CustomCardGraph, IncomeCategoryCard, ExpenseCategoryCard, Spacer, CustomTabs, Tab # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """
<InsightScreen2>:
    name: "insight_screen2"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: app._invisible
        size_hint: (.95, 1)
        pos_hint: {"center_x": .5}    
        radius: dp(11.5)

        CustomTabs:
            Tab:
                title: "Today's Insight"

                InsightCard:
                    padding: dp(2), dp(11.5), dp(2), dp(6)

                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        effect_cls: "ScrollEffect" 

                        MDBoxLayout:
                            orientation: "vertical"
                            padding: dp(0)
                            spacing: dp(11.5)
                            adaptive_height: True

                            CustomCardIdentifier:
                                text: "[b][size=20dp]Spending[/b]"

                            CustomCard:
                                CustomCardLayout:
                                    CustomCardTitleBar:
                                        id: daily_insights_title
                                        title: f"[color=ffffff][size=14dp]Today You've Spent:[/size]  [b][size=13dp]Ksh.[/size] [size=20dp]{root.ds_total:,.2f}[/b][/color]"

                                    CustomCardGraph:
                                        id: daily_spending_graph
                                        orientation: "vertical"

                            ExpenseCategoryCard:
                                e_cat_val1: f"Ksh. {root.ds_cat_val1:,.2f}"
                                e_cat_val2: f"Ksh. {root.ds_cat_val2:,.2f}"
                                e_cat_val3: f"Ksh. {root.ds_cat_val3:,.2f}"
                                e_cat_val4: f"Ksh. {root.ds_cat_val4:,.2f}"
                                e_cat_val5: f"Ksh. {root.ds_cat_val5:,.2f}"

                            Spacer:
                            CustomCardIdentifier:
                                text: "[b][size=20dp]Income[/b]"

                            CustomCard:
                                CustomCardLayout:
                                    CustomCardTitleBar:
                                        id: daily_insights_title
                                        md_bg_color: app._green
                                        title: f"[color=00001f][size=14dp]Today's Income is:[/size]  [b][size=13dp]Ksh.[/size] [size=20dp]{root.di_total:,.2f}[/b][/color]"

                                    CustomCardGraph:
                                        id: daily_income_graph

                            IncomeCategoryCard:
                                i_cat_val1: f"Ksh. {root.di_cat_val1:,.2f}"
                                i_cat_val2: f"Ksh. {root.di_cat_val2:,.2f}"
                                i_cat_val3: f"Ksh. {root.di_cat_val3:,.2f}"
                                i_cat_val4: f"Ksh. {root.di_cat_val4:,.2f}"
                                i_cat_val5: f"Ksh. {root.di_cat_val5:,.2f}"                        

            Tab:
                title: "Weekly Insight"

                InsightCard:
                    padding: dp(2), dp(11.5), dp(2), dp(6)

                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        effect_cls: "ScrollEffect" 

                        MDBoxLayout:
                            orientation: "vertical"
                            padding: dp(0)
                            spacing: dp(11.5)
                            adaptive_height: True

                            CustomCardIdentifier:
                                text: "[b][size=20dp]Spending[/b]"

                            CustomCard:
                                CustomCardLayout:
                                    CustomCardTitleBar:
                                        id: weekly_insights_title
                                        title: f"[color=ffffff][size=14dp]Week {app.current_week_number}'s Expenditure:[/size]  [b][size=13dp]Ksh.[/size] [size=20dp]{root.ws_total:,.2f}[/b][/color]"

                                    CustomCardGraph:
                                        id: weekly_spending_graph

                            ExpenseCategoryCard:
                                e_cat_val1: f"Ksh. {root.ws_cat_val1:,.2f}"
                                e_cat_val2: f"Ksh. {root.ws_cat_val2:,.2f}"
                                e_cat_val3: f"Ksh. {root.ws_cat_val3:,.2f}"
                                e_cat_val4: f"Ksh. {root.ws_cat_val4:,.2f}"
                                e_cat_val5: f"Ksh. {root.ws_cat_val5:,.2f}"

                            Spacer:
                            CustomCardIdentifier:
                                text: "[b][size=20dp]Income[/b]"

                            CustomCard:
                                CustomCardLayout:
                                    CustomCardTitleBar:
                                        id: weekly_insights_title
                                        md_bg_color: app._green
                                        title: f"[color=00001f][size=15dp]Week {app.current_week_number}'s Income: [/size] [b][size=13dp]Ksh.[/size] [size=20dp]{root.wi_total:,.2f}[/b][/color]"

                                    CustomCardGraph:
                                        id: weekly_income_graph

                            IncomeCategoryCard:
                                i_cat_val1: f"Ksh. {root.wi_cat_val1:,.2f}"
                                i_cat_val2: f"Ksh. {root.wi_cat_val2:,.2f}"
                                i_cat_val3: f"Ksh. {root.wi_cat_val3:,.2f}"
                                i_cat_val4: f"Ksh. {root.wi_cat_val4:,.2f}"
                                i_cat_val5: f"Ksh. {root.wi_cat_val5:,.2f}"

            Tab:
                title: "Monthly Insight"

                InsightCard:
                    padding: dp(2), dp(11.5), dp(2), dp(6)

                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        effect_cls: "ScrollEffect" 

                        MDBoxLayout:
                            orientation: "vertical"
                            padding: dp(0)
                            spacing: dp(11.5)
                            adaptive_height: True

                            CustomCardIdentifier:
                                text: "[b][size=20dp]Spending[/b]"

                            CustomCard:
                                CustomCardLayout:
                                    CustomCardTitleBar:
                                        id: monthly_insights_title
                                        title: f"[color=ffffff][size=15dp]{app.month}'s Expenditure:[/size]  [b][size=13dp]Ksh.[/size] [size=20dp]{root.ms_total:,.2f}[/b][/color]"

                                    CustomCardGraph:
                                        id: monthly_spending_graph

                            ExpenseCategoryCard:
                                e_cat_val1: f"Ksh. {root.ms_cat_val1:,.2f}"
                                e_cat_val2: f"Ksh. {root.ms_cat_val2:,.2f}"
                                e_cat_val3: f"Ksh. {root.ms_cat_val3:,.2f}"
                                e_cat_val4: f"Ksh. {root.ms_cat_val4:,.2f}"
                                e_cat_val5: f"Ksh. {root.ms_cat_val5:,.2f}"

                            Spacer:
                            CustomCardIdentifier:
                                text: "[b][size=20dp]Income[/b]"

                            CustomCard:
                                CustomCardLayout:
                                    CustomCardTitleBar:
                                        id: monthly_insights_title
                                        md_bg_color: app._green
                                        title: f"[color=00001f][size=15dp]{app.month}'s Income: [/size] [b][size=13dp]Ksh.[/size] [size=20dp]{root.mi_total:,.2f}[/b][/color]"

                                    CustomCardGraph:
                                        id: monthly_income_graph

                            IncomeCategoryCard:
                                i_cat_val1: f"Ksh. {root.mi_cat_val1:,.2f}"
                                i_cat_val2: f"Ksh. {root.mi_cat_val2:,.2f}"
                                i_cat_val3: f"Ksh. {root.mi_cat_val3:,.2f}"
                                i_cat_val4: f"Ksh. {root.mi_cat_val4:,.2f}"
                                i_cat_val5: f"Ksh. {root.mi_cat_val5:,.2f}"

            Tab:
                title: "Yearly Insight"

                InsightCard:
                    padding: dp(2), dp(11.5), dp(2), dp(6)

                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        effect_cls: "ScrollEffect" 

                        MDBoxLayout:
                            orientation: "vertical"
                            padding: dp(0)
                            spacing: dp(11.5)
                            adaptive_height: True

                            CustomCardIdentifier:
                                text: "[b][size=20dp]Spending[/b]"

                            CustomCard:
                                CustomCardLayout:
                                    CustomCardTitleBar:
                                        id: yearly_insights_title
                                        title: f"[color=ffffff][size=15dp]{app.year}'s Expenditure:[/size]  [b][size=13dp]Ksh.[/size] [size=20dp]{root.ys_total:,.2f}[/b][/color]"

                                    CustomCardGraph:
                                        id: yearly_spending_graph

                            ExpenseCategoryCard:
                                e_cat_val1: f"Ksh. {root.ys_cat_val1:,.2f}"
                                e_cat_val2: f"Ksh. {root.ys_cat_val2:,.2f}"
                                e_cat_val3: f"Ksh. {root.ys_cat_val3:,.2f}"
                                e_cat_val4: f"Ksh. {root.ys_cat_val4:,.2f}"
                                e_cat_val5: f"Ksh. {root.ys_cat_val5:,.2f}"

                            Spacer:
                            CustomCardIdentifier:
                                text: "[b][size=20dp]Income[/b]"

                            CustomCard:
                                CustomCardLayout:
                                    CustomCardTitleBar:
                                        id: yearly_insights_title
                                        md_bg_color: app._green
                                        title: f"[color=00001f][size=15dp]{app.year}'s Income: [/size] [b][size=13dp]Ksh.[/size] [size=20dp]{root.yi_total:,.2f}[/b][/color]"

                                    CustomCardGraph:
                                        id: yearly_income_graph

                            IncomeCategoryCard:
                                i_cat_val1: f"Ksh. {root.yi_cat_val1:,.2f}"
                                i_cat_val2: f"Ksh. {root.yi_cat_val2:,.2f}"
                                i_cat_val3: f"Ksh. {root.yi_cat_val3:,.2f}"
                                i_cat_val4: f"Ksh. {root.yi_cat_val4:,.2f}"
                                i_cat_val5: f"Ksh. {root.yi_cat_val5:,.2f}"

"""

Builder.load_string(KV)


class InsightScreen2(MDScreen):
    ds_total = NumericProperty(0.00)        # "ds" means daily spending
    di_total = NumericProperty(0.00)        # "di" means daily income
    ds_cat_val1 = NumericProperty(0.00)    # "ds_cat_val" means daily spending category value
    ds_cat_val2 = NumericProperty(0.00)
    ds_cat_val3 = NumericProperty(0.00)
    ds_cat_val4 = NumericProperty(0.00)
    ds_cat_val5 = NumericProperty(0.00)
    di_cat_val1 = NumericProperty(0.00)    # "di_cat_val" means daily income category value
    di_cat_val2 = NumericProperty(0.00)
    di_cat_val3 = NumericProperty(0.00)
    di_cat_val4 = NumericProperty(0.00)
    di_cat_val5 = NumericProperty(0.00)

    ws_total = NumericProperty(0.00)        # "ws" means weekly spending
    wi_total = NumericProperty(0.00)        # "wi" means weekly income
    ws_cat_val1 = NumericProperty(0.00)    # "ws_cat_val" means weekly spending category value
    ws_cat_val2 = NumericProperty(0.00)
    ws_cat_val3 = NumericProperty(0.00)
    ws_cat_val4 = NumericProperty(0.00)
    ws_cat_val5 = NumericProperty(0.00)
    wi_cat_val1 = NumericProperty(0.00)    # "wi_cat_val" means weekly income category value
    wi_cat_val2 = NumericProperty(0.00)
    wi_cat_val3 = NumericProperty(0.00)
    wi_cat_val4 = NumericProperty(0.00)
    wi_cat_val5 = NumericProperty(0.00)

    ms_total = NumericProperty(0.00)        # "ms" means monthly spending
    mi_total = NumericProperty(0.00)        # "mi" means monthly income
    ms_cat_val1 = NumericProperty(0.00)    # "ms_cat_val" means monthly spending category value
    ms_cat_val2 = NumericProperty(0.00)
    ms_cat_val3 = NumericProperty(0.00)
    ms_cat_val4 = NumericProperty(0.00)
    ms_cat_val5 = NumericProperty(0.00)
    mi_cat_val1 = NumericProperty(0.00)    # "mi_cat_val" means monthly income category value
    mi_cat_val2 = NumericProperty(0.00)
    mi_cat_val3 = NumericProperty(0.00)
    mi_cat_val4 = NumericProperty(0.00)
    mi_cat_val5 = NumericProperty(0.00)

    ys_total = NumericProperty(0.00)        # "ys" means yearly spending
    yi_total = NumericProperty(0.00)        # "yi" means yearly income
    ys_cat_val1 = NumericProperty(0.00)    # "ys_cat_val" means yearly spending category value
    ys_cat_val2 = NumericProperty(0.00)
    ys_cat_val3 = NumericProperty(0.00)
    ys_cat_val4 = NumericProperty(0.00)
    ys_cat_val5 = NumericProperty(0.00)
    yi_cat_val1 = NumericProperty(0.00)    # "yi_cat_val" means yearly income category value
    yi_cat_val2 = NumericProperty(0.00)
    yi_cat_val3 = NumericProperty(0.00)
    yi_cat_val4 = NumericProperty(0.00)
    yi_cat_val5 = NumericProperty(0.00)


    def __init__(self, user_data_store=None, firebase=None, **kwargs):
        super().__init__(**kwargs)
        self._red, self._green, self._light, self._invisible = "#ff2f3f", "#2fc46c", "#c800f0", (1, 1, 1, 0)
        self.current_month_num_of_days = monthrange(datetime.today().year, datetime.today().month)[1]
        self.user_data_store = user_data_store
        self.firebase = firebase
        self.id_token = None
        self.u_id = None

    def on_enter(self):
        self.id_token = self.user_data_store.get("credentials")["id_token"] if self.user_data_store.exists("credentials") else None
        self.u_id = self.user_data_store.get("credentials")["uid"] if self.user_data_store.exists("credentials") else None
        threading.Thread(target=self.load_visual_insights, daemon=True).start()

    def load_visual_insights(self):
        self.id_token = self.user_data_store.get("credentials")["id_token"] if self.user_data_store.exists("credentials") else None
        self.u_id = self.user_data_store.get("credentials")["uid"] if self.user_data_store.exists("credentials") else None
        if not all([self.firebase, self.id_token, self.u_id]): return
        try:
            data = self.firebase.get_data(
                id_token=self.id_token,
                path=f"users/{self.u_id}/parsed_data/mpesa_account/All Insights"
            )

            if not data:
                print("No visual insights available.")
                return

            daily = data.get("Daily", {}).get("Graph Data", {})
            weekly = data.get("Weekly", {}).get("Graph Data", {})
            monthly = data.get("Monthly", {}).get("Graph Data", {})
            yearly = data.get("Yearly", {}).get("Graph Data", {})

            self.ds_total = data.get("Daily", {}).get("Total Expenditure", 0.00)
            self.di_total = data.get("Daily", {}).get("Total Income", 0.00)
            self.ds_cat_val1 = data.get("Daily", {}).get("Expense Category", {}).get("Friends & Family", 0.00)
            self.ds_cat_val2 = data.get("Daily", {}).get("Expense Category", {}).get("Housing", 0.00)
            self.ds_cat_val3 = data.get("Daily", {}).get("Expense Category", {}).get("Utilities", 0.00)
            self.ds_cat_val4 = data.get("Daily", {}).get("Expense Category", {}).get("Groceries", 0.00)
            self.ds_cat_val5 = data.get("Daily", {}).get("Expense Category", {}).get("Miscellaneous", 0.00)
            self.di_cat_val1 = data.get("Daily", {}).get("Income Category", {}).get("Friends & Family", 0.00)
            self.di_cat_val2 = data.get("Daily", {}).get("Income Category", {}).get("Salary", 0.00)
            self.di_cat_val3 = data.get("Daily", {}).get("Income Category", {}).get("Investments", 0.00)
            self.di_cat_val4 = data.get("Daily", {}).get("Income Category", {}).get("Side Gigs", 0.00)
            self.di_cat_val5 = data.get("Daily", {}).get("Income Category", {}).get("Other Income", 0.00)

            self.ws_total = data.get("Weekly", {}).get("Total Expenditure", 0.00)
            self.wi_total = data.get("Weekly", {}).get("Total Income", 0.00)
            self.ws_cat_val1 = data.get("Weekly", {}).get("Expense Category", {}).get("Friends & Family", 0.00)
            self.ws_cat_val2 = data.get("Weekly", {}).get("Expense Category", {}).get("Housing", 0.00)
            self.ws_cat_val3 = data.get("Weekly", {}).get("Expense Category", {}).get("Utilities", 0.00)
            self.ws_cat_val4 = data.get("Weekly", {}).get("Expense Category", {}).get("Groceries", 0.00)
            self.ws_cat_val5 = data.get("Weekly", {}).get("Expense Category", {}).get("Miscellaneous", 0.00)
            self.wi_cat_val1 = data.get("Weekly", {}).get("Income Category", {}).get("Friends & Family", 0.00)
            self.wi_cat_val2 = data.get("Weekly", {}).get("Income Category", {}).get("Salary", 0.00)
            self.wi_cat_val3 = data.get("Weekly", {}).get("Income Category", {}).get("Investments", 0.00)
            self.wi_cat_val4 = data.get("Weekly", {}).get("Income Category", {}).get("Side Gigs", 0.00)
            self.wi_cat_val5 = data.get("Weekly", {}).get("Income Category", {}).get("Other Income", 0.00)

            self.ms_total = data.get("Monthly", {}).get("Total Expenditure", 0.00)
            self.mi_total = data.get("Monthly", {}).get("Total Income", 0.00)
            self.ms_cat_val1 = data.get("Monthly", {}).get("Expense Category", {}).get("Friends & Family", 0.00)
            self.ms_cat_val2 = data.get("Monthly", {}).get("Expense Category", {}).get("Housing", 0.00)
            self.ms_cat_val3 = data.get("Monthly", {}).get("Expense Category", {}).get("Utilities", 0.00)
            self.ms_cat_val4 = data.get("Monthly", {}).get("Expense Category", {}).get("Groceries", 0.00)
            self.ms_cat_val5 = data.get("Monthly", {}).get("Expense Category", {}).get("Miscellaneous", 0.00)
            self.mi_cat_val1 = data.get("Monthly", {}).get("Income Category", {}).get("Friends & Family", 0.00)
            self.mi_cat_val2 = data.get("Monthly", {}).get("Income Category", {}).get("Salary", 0.00)
            self.mi_cat_val3 = data.get("Monthly", {}).get("Income Category", {}).get("Investments", 0.00)
            self.mi_cat_val4 = data.get("Monthly", {}).get("Income Category", {}).get("Side Gigs", 0.00)
            self.mi_cat_val5 = data.get("Monthly", {}).get("Income Category", {}).get("Other Income", 0.00)

            self.ys_total = data.get("Yearly", {}).get("Total Expenditure", 0.00)
            self.yi_total = data.get("Yearly", {}).get("Total Income", 0.00)
            self.ys_cat_val1 = data.get("Yearly", {}).get("Expense Category", {}).get("Friends & Family", 0.00)
            self.ys_cat_val2 = data.get("Yearly", {}).get("Expense Category", {}).get("Housing", 0.00)
            self.ys_cat_val3 = data.get("Yearly", {}).get("Expense Category", {}).get("Utilities", 0.00)
            self.ys_cat_val4 = data.get("Yearly", {}).get("Expense Category", {}).get("Groceries", 0.00)
            self.ys_cat_val5 = data.get("Yearly", {}).get("Expense Category", {}).get("Miscellaneous", 0.00)
            self.yi_cat_val1 = data.get("Yearly", {}).get("Income Category", {}).get("Friends & Family", 0.00)
            self.yi_cat_val2 = data.get("Yearly", {}).get("Income Category", {}).get("Salary", 0.00)
            self.yi_cat_val3 = data.get("Yearly", {}).get("Income Category", {}).get("Investments", 0.00)
            self.yi_cat_val4 = data.get("Yearly", {}).get("Income Category", {}).get("Side Gigs", 0.00)
            self.yi_cat_val5 = data.get("Yearly", {}).get("Income Category", {}).get("Other Income", 0.00)

            def safe_render(graph_data, graph_type, color, render_func):
                normalized = self.normalize_graph_data(graph_data)
                if normalized:
                    Clock.schedule_once(lambda dt: render_func(normalized, graph_type, color), 0)

            # Daily Graph
            safe_render(daily.get("Expenditure", [0]*24), "spending", self._red, self.load_daily_graph)
            safe_render(daily.get("Income", [0]*24), "income", self._green, self.load_daily_graph)

            # Weekly Graph
            safe_render(weekly.get("Expenditure", [0]*7), "spending", self._red, self.load_weekly_graph)
            safe_render(weekly.get("Income", [0]*7), "income", self._green, self.load_weekly_graph)

            # Monthly Graph
            safe_render(monthly.get("Expenditure", [0]*self.current_month_num_of_days), "spending", self._red, self.load_monthly_graph)
            safe_render(monthly.get("Income", [0]*self.current_month_num_of_days), "income", self._green, self.load_monthly_graph)

            # Yearly Graph
            safe_render(yearly.get("Expenditure", [0]*12), "spending", self._red, self.load_yearly_graph)
            safe_render(yearly.get("Income", [0]*12), "income", self._green, self.load_yearly_graph)

        except Exception: pass

    @staticmethod
    def normalize_graph_data(data):
        """For preventing division by zero error"""
        if not data or all(val == data[0] for val in data): return None
        return data

    def load_daily_graph(self, graph_data, graph_type, graph_color):
        """
        graph_data is a list of 24 hourly summations,
        graph_type is either "spending" or "income",
        graph_color is the color of the graph,
        """

        graph_container = None
        if graph_type == "spending": graph_container = self.ids.daily_spending_graph
        elif graph_type == "income": graph_container = self.ids.daily_income_graph

        graph = AKLineChart(
            bg_color=self._invisible, lines_color=graph_color, line_width=1.2, circles_color=self._light, circles_radius=4
        )

        graph.x_values = list(range(24))
        graph.y_values = graph_data
        graph.x_labels = ['12AM', ' ', ' ', ' ', ' ', ' ', ' 06AM', ' ', ' ', ' ', ' ', ' ', '12PM', ' ', ' ', ' ', ' ', ' ', ' 06PM', ' ', ' ', ' ', ' ', '11PM']
        graph.y_labels = [" " for _ in range(24)]
        graph_container.clear_widgets()
        graph_container.add_widget(graph)

    def load_weekly_graph(self, graph_data, graph_type, graph_color):
        """
        graph_data is a list of 7 daily summations,
        graph_type is either "spending" or "income",
        graph_color is the color of the graph,
        """

        graph_container = None
        if graph_type == "spending": graph_container = self.ids.weekly_spending_graph
        elif graph_type == "income": graph_container = self.ids.weekly_income_graph

        graph = AKBarChart(
            bg_color=self._invisible, line_width=1, lines_color=graph_color, bars_color=graph_color, bars_spacing=dp(20), max_bar_width=dp(20)
        )

        graph.x_values, graph.y_values = [0, 1, 2, 3, 4, 5, 6], graph_data
        graph.x_labels = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        graph.y_labels = ['', '', '', '', '', '', '']
        graph_container.clear_widgets()
        graph_container.add_widget(graph)

    def load_monthly_graph(self, graph_data, graph_type, graph_color):
        """
        graph_data is a list of monthly daily summations,
        graph_type is either "spending" or "income",
        graph_color is the color of the graph,
        """

        graph_container = None
        if graph_type == "spending": graph_container = self.ids.monthly_spending_graph
        elif graph_type == "income": graph_container = self.ids.monthly_income_graph

        graph = AKLineChart(
            bg_color=self._invisible, lines_color=graph_color, line_width=1.2, circles_color=self._light, circles_radius=4
        )

        x_labels = []
        for day in range(1, self.current_month_num_of_days + 1):
            if day in [1, 7, 13, 19, 24, self.current_month_num_of_days]:
                suffix = "th"
                if day in [1, 21, 31]: suffix = "st"
                elif day in [2, 22]: suffix = "nd"
                elif day in [3, 23]: suffix = "rd"
                label = f"{day}{suffix}"
            else: label = " "
            x_labels.append(label)

        graph.x_values = list(range(self.current_month_num_of_days))
        graph.x_labels = x_labels
        graph.y_values = graph_data
        graph.y_labels = [" " for _ in range(self.current_month_num_of_days)]
        graph_container.clear_widgets()
        graph_container.add_widget(graph)

    def load_yearly_graph(self, graph_data, graph_type, graph_color):
        """
        graph_data is a list of 12 monthly summations,
        graph_type is either "spending" or "income",
        graph_color is the color of the graph,
        """

        graph_container = None
        if graph_type == "spending": graph_container = self.ids.yearly_spending_graph
        elif graph_type == "income": graph_container = self.ids.yearly_income_graph

        graph = AKLineChart(
            bg_color=self._invisible, lines_color=graph_color, line_width=1.2, circles_color=self._light, circles_radius=4
        )

        graph.x_values, graph.y_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], graph_data
        graph.x_labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
        graph.y_labels = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        graph_container.clear_widgets()
        graph_container.add_widget(graph)
