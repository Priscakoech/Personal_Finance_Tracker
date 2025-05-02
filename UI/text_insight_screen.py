
import random
import threading
from datetime import datetime, timedelta
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from UI.reusables import InsightScreenTopBar, InsightCard, CustomTabs, Tab # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """
<InsightScreen1>:
    name: "insight_screen1"
    md_bg_color: app._dark

    MDBoxLayout:
        md_bg_color: app._invisible
        size_hint: (.95, 1)
        pos_hint: {"center_x": .5}
        orientation: "vertical"
        spacing: dp(3)

        CustomTabs:
            Tab:
                title: "Today's Insight"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        scroll_cls: "ScrollEffect"

                        MDBoxLayout:
                            id: daily_insight
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "Weekly Insight"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        scroll_cls: "ScrollEffect"

                        MDBoxLayout:
                            id: weekly_insight
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "Monthly Insight"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        scroll_cls: "ScrollEffect"

                        MDBoxLayout:
                            id: monthly_insight
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "Yearly Insight"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        scroll_cls: "ScrollEffect"

                        MDBoxLayout:
                            id: yearly_insight
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "General Insight"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        scroll_cls: "ScrollEffect"

                        MDBoxLayout:
                            id: general_insight
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(65)
            orientation: "vertical"
            spacing: dp(6)

            # insight generator btn
            MDCard:
                id: btn_bg
                md_bg_color: app._white
                size_hint: (.95, None)
                height: dp(48)
                pos_hint: {"center_x": .5}
                radius: dp(11.5)

                MDRectangleFlatIconButton:
                    id: generate_button
                    disabled: False
                    text: "Generate Insight"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app._dark
                    font_size: "20dp"
                    size_hint: (1, 1)
                    line_color: app._invisible
                    _no_ripple_effect: True
                    on_release: root.on_generate_button_pressed()

                    MDSpinner:
                        id: insight_gen_spinner
                        size_hint: (None, None) 
                        size: ("23dp", "23dp")
                        pos_hint: {"center_y": .5}
                        active: False


            CustomLabel:
                text: "[b][size=14dp]Powered by ChatGPT-4o mini[/size][/b]"
                halign: "center"
                text_color: app._gray

"""

Builder.load_string(KV)


class InsightScreen1(MDScreen):
    def __init__(self, data_handler=None, user_data_store=None, text_insights_store=None, **kwargs):
        super().__init__(**kwargs)
        self._white = "#dddddd"
        self.data_handler = data_handler
        self.firebase = None
        self.id_token = None
        self.u_id = None
        self.user_data_store = user_data_store
        self.text_insights_store = text_insights_store
        self.tab_insights = {}
        self.insight_categories = ["daily", "weekly", "monthly", "yearly", "general"]
        self.tab_categories = [
            "daily_insight", "weekly_insight", "monthly_insight", "yearly_insight", "general_insight"
        ]

    def on_enter(self, *args):
        Clock.schedule_once(lambda dt: self.check_insight_cooldown(), 6)
        self.load_saved_insights()
        if not hasattr(self, 'insights_initialized'):
            self.prepare_insight_tabs()
            self.insights_initialized = True

    def prepare_insight_tabs(self, text=""):
        for tab_category in self.tab_categories:
            label = MDLabel(
                text=f"\n\n\nClick on 'Generate insights' to view {tab_category.replace('_', ' ')}..." if text == "" else text,
                halign="left",
                theme_text_color="Custom",
                text_color=(1,1,1,1),
                markup=True,
            )
            self.tab_insights[tab_category] = {"text": "", "label": label}
            self.ids[tab_category].add_widget(label)

    def start_text_animation(self):
        # Disable button
        self.ids.generate_button.disabled = True
        self.ids.generate_button.text = "Next insight in 24hrs..."
        self.ids.btn_bg.md_bg_color = (.6, .6, 1, .1)
        self.ids.btn_bg.radius = dp(0)

        # Clear labels and start animation
        for tab_id, tab_data in self.tab_insights.items():
            tab_data["label"].text = ""
            tab_data["label"].bind(texture_size=lambda instance, value: self.update_label_height(instance))
            Clock.schedule_once(lambda dt, t_id=tab_id: self.animate_text(t_id), 0.000023)

        # Re-enable button after 24hrs
        Clock.schedule_once(lambda dt: self.enable_button(), 24 * 60 * 60)

    def animate_text(self, tab_id, step=0):
        insight_text = self.tab_insights[tab_id]["text"]
        label = self.tab_insights[tab_id]["label"]

        if step < len(insight_text):
            label.text += insight_text[step]
            Clock.schedule_once(lambda dt: self.animate_text(tab_id, step + 1), 0.000023)

    def enable_button(self):
        self.ids.generate_button.disabled = False
        self.ids.generate_button.text = "Generate Insights"
        self.ids.generate_button.font_size = "20dp"
        self.ids.btn_bg.md_bg_color = self._white
        self.ids.btn_bg.radius = dp(11.5)

    @staticmethod
    def update_label_height(label):
        label.height = label.texture_size[1]
        label.size_hint_y = None

    def generate_insights(self):
        self.current_insight_idx = 0
        self.categories_to_generate = self.insight_categories.copy()
        self.tab_ids = self.tab_categories.copy()
        self.try_generate_next_insight()

    def reset_generate_button(self):
        self.ids.generate_button.text = "Next insight in 24hrs..."
        self.ids.generate_button.disabled = True
        self.ids.insight_gen_spinner.active = False

    def try_generate_next_insight(self, *args):
        app = App.get_running_app()
        parser = app.data_handler.parser
        self.firebase = parser.firebase
        self.id_token = parser.id_token
        self.u_id = parser.u_id

        if not all([self.firebase, self.id_token, self.u_id]):
                print("Missing Firebase credentials.")
                return

        try:
            all_insights = self.firebase.get_data(
                id_token=self.id_token,
                path=f"users/{self.u_id}/parsed_data/mpesa_account/All Insights"
            )

            general_insight = self.firebase.get_data(
                id_token=self.id_token,
                path=f"users/{self.u_id}/parsed_data/mpesa_account/General Insight"
            )

            merged_insights = [
                all_insights.get("Daily", {}),
                all_insights.get("Weekly", {}),
                all_insights.get("Monthly", {}),
                all_insights.get("Yearly", {}),
                general_insight
            ]

            if self.current_insight_idx > len(self.categories_to_generate) - 1:
                insight_gen_time = datetime.now().isoformat()
                self.user_data_store.put("insight_gen_time", timestamp=insight_gen_time)
                self.reset_generate_button()

            if self.current_insight_idx < len(self.categories_to_generate):
                category = self.categories_to_generate[self.current_insight_idx]
                insight_data = merged_insights[self.current_insight_idx]
                tab_id = self.tab_ids[self.current_insight_idx]

                threading.Thread(
                    target=self.get_insight_in_background,
                    args=(category, insight_data, tab_id)
                ).start()

            else:
                self.reset_generate_button()
            
        except Exception: pass

    def get_insight_in_background(self, category, insight_data, tab_id):
        try:
            user_name = self.firebase.get_data(id_token=self.id_token, path=f"users/{self.u_id}/user_profile")["Full name"]
            raw_text = self.data_handler.generate_insight(category, insight_data, user_name)
            Clock.schedule_once(lambda dt: self.update_insight_success(tab_id, category, raw_text))

        except Exception as e:
            print(str(e))
            Clock.schedule_once(lambda dt: self.handle_generation_error())

    def update_insight_success(self, tab_id, category, raw_text):
        self.tab_insights[tab_id]["text"] = raw_text
        self.save_generated_insight(category, raw_text)
        self.animate_single_tab(tab_id)

        self.current_insight_idx += 1
        Clock.schedule_once(self.try_generate_next_insight, random.uniform(16, 23))

    def save_generated_insight(self, category, content):
        self.text_insights_store.put(category, content=content)

    def load_saved_insights(self):
        for tab_category in self.tab_categories:
            category = tab_category.split("_")[0]
            if self.text_insights_store.exists(category):
                saved_text = self.text_insights_store.get(category)["content"]
                label = MDLabel(
                    text=f"{saved_text}",
                    halign="left",
                    theme_text_color="Custom",
                    text_color=(1,1,1,1),
                    markup=True,
                )
                label.bind(texture_size=lambda instance, value: self.update_label_height(instance))
                self.tab_insights[tab_category] = {"text": "", "label": label}
                self.ids[tab_category].clear_widgets()
                self.ids[tab_category].add_widget(label)

    def handle_generation_error(self):
        self.ids.generate_button.text = f"Error generating insights.\nTry again later..."
        self.ids.generate_button.font_size = "15dp"
        self.ids.generate_button.disabled = True
        self.ids.insight_gen_spinner.active = False

        # Every time an error occurs, Re-enable the button after a minute
        Clock.schedule_once(lambda dt: self.enable_button(), 59)

    def animate_single_tab(self, tab_id, step=0):
        """Animate text for a single tab immediately."""
        insight_text = self.tab_insights[tab_id]["text"]
        label = self.tab_insights[tab_id]["label"]

        if step == 0:
            label.text = ""
            label.bind(texture_size=lambda instance, value: self.update_label_height(instance))

        if step < len(insight_text):
            label.text += insight_text[step]
            Clock.schedule_once(lambda dt: self.animate_single_tab(tab_id, step + 1), 0.000023)

    def on_generate_button_pressed(self):
        if self.ids.generate_button.disabled:
            return  # protect double clicks

        for tab_id, tab_data in self.tab_insights.items():
            tab_data["label"].text = ""
            tab_data["label"].bind(texture_size=lambda instance, value: self.update_label_height(instance))

        for tab_category in self.tab_categories:
            label = MDLabel(
                text="[size=56dp]•[/size]",
                halign="left",
                theme_text_color="Custom",
                text_color=(1,1,1,1),
                markup=True,
            )
            label.bind(texture_size=lambda instance, value: self.update_label_height(instance))
            self.tab_insights[tab_category] = {"text": "", "label": label}
            self.ids[tab_category].add_widget(label)

        self.ids.generate_button.disabled = True
        self.ids.btn_bg.md_bg_color = (.6, .6, 1, .1)
        self.ids.btn_bg.radius = dp(0)
        self.ids.generate_button.text = "Generating Insights..."
        self.ids.insight_gen_spinner.active = True

        self.generate_insights()

    def check_insight_cooldown(self):
        if self.user_data_store.exists("insight_gen_time"):
            last_gen_str = self.user_data_store.get("insight_gen_time")["timestamp"]
            last_gen_time = datetime.fromisoformat(last_gen_str)
            now = datetime.now()

            delta = now - last_gen_time

            if delta < timedelta(hours=24):
                remaining = 24 - delta.seconds // 3600
                self.ids.generate_button.disabled = True
                self.ids.btn_bg.md_bg_color = (.6, .6, 1, .1)
                self.ids.btn_bg.radius = dp(0)
                self.ids.generate_button.text = f"Next insight in {remaining} hrs..."
            else:
                self.enable_generate_button()
                self.clear_stale_insights()
                self.load_saved_insights()

        else:
            self.enable_generate_button()
            self.clear_stale_insights()
            self.load_saved_insights()

    def enable_generate_button(self):
        self.ids.generate_button.disabled = False
        self.ids.btn_bg.radius = dp(11.5)
        self.ids.btn_bg.md_bg_color = self._white
        self.ids.generate_button.text = "Generate Insights"

    def clear_stale_insights(self):
        for tab_category in self.tab_categories:
            category = tab_category.split("_")[0]
            default_text = f"Click on 'Generate insights' to view {tab_category.replace('_', ' ')}..."
            self.text_insights_store.put(category, content=default_text)
