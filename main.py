from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivy.uix.screenmanager import SlideTransition, NoTransition, CardTransition
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem
from kivymd.utils.set_bars_colors import set_bars_colors
from datetime import datetime, timedelta
import calendar

from UI.welcome_screen import WelcomeScreen
from UI.onboarding_screen import OnboardingScreen
from UI.privacy_policy_screen import PrivacyPolicyScreen
from UI.terms_of_use_screen import TermsOfUseScreen
from UI.full_name_screen import FullNameScreen
from UI.wallet_setup_screen import WalletSetupScreen
from UI.m_pesa import AddMpesaAccScreen
from UI.paypal import AddPaypalAccScreen
from UI.crypto import AddCryptoWalletScreen
# from UI.cards import AddCardScreen
from UI.home_screen import HomeScreen
from UI.transactions_screen import TransactionsScreen
from UI.wallet_screen import WalletScreen
from UI.text_insight_screen import InsightScreen1
from UI.visual_insight_screen import InsightScreen2
from UI.settings_screen import SettingsScreen
from UI.personal_info_screen import PersonalInfoScreen
from UI.reports_screen import ReportsScreen


# this window size is for development purposes only...
Window.size = (386, 723)

class PersonalFinanceTrackerApp(MDApp):
    def __init__(self):
        super().__init__()
        self.title = "Personal Finance Tracker"
        self.theme_cls.theme_style = "Dark"

        # colors
        self._dark, self._tinted, self._light, self._white, self._gray, self._blue, self._green, self._invisible, self._red = (
            "#00001fff", (.6, .6, 1, .1), "#c800f0", "#dddddd", "#a6a6a6", "#005eff", "#2fc46c", (1, 1, 1, 0), "#ff2f3f"
        )

        self.full_name = "Prisca Koech"
        self.email_address = "priscakoech448@gmail.com"
        self.profile_photo = "assets/images/default_avatar.jpg"
        self.total_user_balance = 567477.967

        # variables for determining date and time
        self.current_hour = datetime.now().hour
        self.today = calendar.day_name[datetime.now().weekday()]
        self.today_date = datetime.now().day
        self.month = datetime.now().strftime("%B")
        self.year = datetime.now().year
        self.previous_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B")
        self.current_week_number = datetime.now().isocalendar().week
        self.week_number_year = datetime.now().isocalendar().year
        self.week_number_start_date = datetime.now() - timedelta(days=datetime.now().weekday())
        self.week_number_end_date = self.week_number_start_date + timedelta(days=6)
        self.week_number_start_date = self.week_number_start_date.strftime("%B %d")
        self.week_number_end_date = self.week_number_end_date.strftime("%B %d")

        # ------------------------- insight_screen content -----------------------------------

        # self.client = OpenAI(api_key=OPENAI_API_KEY)

        self.all_insights, self.tab_insights, self.all_insights_index = [], {}, 0

        self.tab_categories = [
            "daily_insight", "weekly_insight", "monthly_insight", "yearly_insight", "general_insight"
        ]
        self.insight_categories = ["daily", "weekly", "monthly", "yearly", "general"]

        for category in self.insight_categories:
            # self.insight = self.client.chat.completions.create(
            #     model="gpt-4o-mini",
            #     messages=[
            #         {"role": "system",
            #          "content": "You are my personal finance tracker app assistant.... "
            #                     "I want you to generate insights based on the flow of my "
            #                     "finances.... use an arbitrary account...currency(Ksh.)...also the output "
            #                     "should only contain 4 text styles... in markdown.... "
            #                     "#title, **subtitle**, *italics*, and - lists.... nothing else...."
            #                     "and also normal text for comments/overview..."
            #          },
            #
            #         {"role": "user", "content": f"generate a {category} insight"}
            #     ]
            # )
            #
            # self.all_insights.append(
            #     MarkdownFormatter().format_text(text=self.insight.choices[0].message.content)
            # )

            # self.no_internet_fallback_txt = "[b]\nOops!\nYou are offline...[/b]"
            self.insight = "[b]\nFor development purposes, \nInsight generation has been paused....[/b]"
            self.all_insights.append(self.insight)

        for tab_category in self.tab_categories:
            self.insight_dict = {
                f"{tab_category}": {
                    "text": f"{self.all_insights[self.all_insights_index]}",
                    "label": MDLabel(
                        text=f"\n\n\n\nClick on 'Generate insights' to view "
                             f"{self.insight_categories[self.all_insights_index]} insights...",
                        halign="left",
                        theme_text_color="Custom",
                        text_color=self._white,
                        markup=True,
                    ),
                }
            }
            self.tab_insights.update(self.insight_dict)
            self.all_insights_index += 1

    def build(self):
        self.set_bars_colors()

        screen_manager = MDScreenManager()
        screen_manager.add_widget(WelcomeScreen())
        screen_manager.add_widget(OnboardingScreen())
        screen_manager.add_widget(PrivacyPolicyScreen())
        screen_manager.add_widget(TermsOfUseScreen())
        screen_manager.add_widget(FullNameScreen())
        screen_manager.add_widget(WalletSetupScreen())
        screen_manager.add_widget(AddMpesaAccScreen())
        screen_manager.add_widget(AddPaypalAccScreen())
        screen_manager.add_widget(AddCryptoWalletScreen())
        # screen_manager.add_widget(AddCardScreen())
        screen_manager.add_widget(HomeScreen())
        screen_manager.add_widget(TransactionsScreen())
        screen_manager.add_widget(WalletScreen())
        screen_manager.add_widget(InsightScreen1())
        screen_manager.add_widget(InsightScreen2())
        screen_manager.add_widget(SettingsScreen())
        screen_manager.add_widget(PersonalInfoScreen())
        screen_manager.add_widget(ReportsScreen())

        return screen_manager

    def on_start(self):
        # Binding the Android back button to the go_back() method
        Window.bind(on_keyboard=self.on_keyboard)

        self.minimalistic_transactions_view()

        # Add the labels to their respective cards
        for tab_id, tab_data in self.tab_insights.items():
            self.root.get_screen("insight_screen1").ids[tab_id].add_widget(tab_data["label"])

    def set_bars_colors(self):
        set_bars_colors(get_color_from_hex(self._dark), get_color_from_hex(self._dark), "Light")

    def go_back(self):
        self.root.current = self.root.previous()

    def on_keyboard(self, window, key, *args):
        # Android back button (keycode 27)
        if key == 27:
            self.go_back()
            return True
        return False

    def change_screen_wt(self, screen_name, direction, mode="push"):
        """change screen with transition"""
        pop_screen_list = [
            "home_screen", "transactions_screen", "wallet_screen", "insight_screen1", "insight_screen2",
            "settings_screen", "personal_info_screen", "reports_screen"
        ]

        if self.root.current in pop_screen_list:
            self.root.transition = CardTransition(direction=direction, mode=mode)

        else:
            self.root.transition = SlideTransition(direction=direction)
        self.root.current = screen_name

    def change_screen_wnt(self, screen_name):
        """change screen with no transition"""
        self.root.transition = NoTransition()
        self.root.current = screen_name

    def goto_hyperlink(self, ref):
        """Handles the 'ref' text in the welcome screen..."""
        if ref == "privacy": self.change_screen_wt("privacy_policy_screen", "left")
        elif ref == "terms": self.change_screen_wt("terms_of_use_screen", "left")

    def enable_submit_btn(self):
        """
        Enables the submit button if the lengths of first_name, and last_name are greater than 0...
        Disables it if either has a length of 0...
        """
        current_screen = self.root.get_screen("full_name_input_screen")

        if len(current_screen.ids.first_name.text) > 0 and len(current_screen.ids.last_name.text) > 0:
            current_screen.ids.submit_btn_bg.md_bg_color = self._white
            current_screen.ids.submit_btn_bg.ripple_behavior = True
            current_screen.ids.submit_btn.disabled = False

        else:
            current_screen.ids.submit_btn_bg.md_bg_color = self._tinted
            current_screen.ids.submit_btn_bg.ripple_behavior = False
            current_screen.ids.submit_btn.disabled = True

    def get_name(self):
        first_name = self.root.get_screen("full_name_input_screen").ids.first_name.text.capitalize()
        last_name = self.root.get_screen("full_name_input_screen").ids.last_name.text.capitalize()
        full_name = f"{first_name} {last_name}"
        return full_name

    def greeting_text(self):
        if 0 <= self.current_hour <= 11: return "Good Morning,"
        if 12 <= self.current_hour <= 15: return "Good Afternoon,"
        if 16 <= self.current_hour <= 23: return "Good Evening,"

    def change_indicator_color(self, current_slide_index):
        # Resetting all indicator colors to gray...
        self.root.get_screen("home_screen").ids.slide1_indicator_color.md_bg_color = "#a6a6a6"
        self.root.get_screen("home_screen").ids.slide2_indicator_color.md_bg_color = "#a6a6a6"

        # Changing indicator colors to blue based on the current slide index
        if current_slide_index == 0:
            self.root.get_screen("home_screen").ids.slide1_indicator_color.md_bg_color = "#005eff"
        if current_slide_index == 1:
            self.root.get_screen("home_screen").ids.slide2_indicator_color.md_bg_color = "#005eff"

    def change_chart(self):
        self.root.get_screen("home_screen").ids.chart.source = "assets/images/income_expenditure_bar.png" \
            if self.root.get_screen("home_screen").ids.chart.source == "assets/images/income_expenditure_graph.png" \
            else "assets/images/income_expenditure_graph.png"

    def minimalistic_transactions_view(self):
        for i in range(6):
            list_item = TwoLineListItem(divider=None, _no_ripple_effect=True)

            list_item_container = MDCard(
                md_bg_color=(0, 0, 0, 0),
                size_hint=(1, 1),
                pos_hint={"center_x": .5, "center_y": .5},
                padding=dp(6)
            )

            list_item_bg = MDCard(
                md_bg_color=self._tinted,
                padding=(dp(0), dp(0), dp(10), dp(0)),
                radius=dp(11.5),
            )

            logo_bg = MDBoxLayout(
                size_hint=(None, None),
                width="50dp",
                height="50dp",
                pos_hint={"center_y": .5}
            )

            logo = Image(
                source="assets/images/mpesa_icon.png",
                size_hint=(1, .9),
                pos_hint={"center_y": .5}
            )

            logo_bg.add_widget(logo)
            list_item_bg.add_widget(logo_bg)

            left_text_bg = MDBoxLayout(padding=dp(11.5))

            left_text = MDLabel(
                text=f"M-PESA\n[color=a6a6a6][b][size=13dp]1/1/25 at 4:07 PM[/size][/b]",
                markup=True,
                halign="left",
                font_size="15dp",
                theme_text_color="Custom",
                text_color=self._white
            )

            left_text_bg.add_widget(left_text)
            list_item_bg.add_widget(left_text_bg)

            right_text_bg = MDBoxLayout()

            right_text = MDLabel(
                text="+ 100.00",
                bold=True,
                halign="right",
                pos_hint={"center_x": .5, "center_y": .5},
                theme_text_color="Custom",
                text_color=self._green
            )

            right_text_bg.add_widget(right_text)
            list_item_bg.add_widget(right_text_bg)

            list_item_container.add_widget(list_item_bg)
            list_item.add_widget(list_item_container)

            self.root.get_screen("home_screen").ids.minimalistic_transactions.add_widget(list_item)

    def card_to_show_or_hide(self, card_id):
        card = None
        if card_id == "daily_report_card":
            card = self.root.get_screen("reports_screen").ids.daily_report_card

        if card_id == "weekly_report_card":
            card = self.root.get_screen("reports_screen").ids.weekly_report_card

        if card_id == "monthly_report_card":
            card = self.root.get_screen("reports_screen").ids.monthly_report_card

        if card_id == "yearly_report_card":
            card = self.root.get_screen("reports_screen").ids.yearly_report_card

        if card_id == "change_avatar":
            card = self.root.get_screen("personal_info_screen").ids.change_avatar

        return card

    @staticmethod
    def show_card(card):
        show_card_animation = Animation(y=0, d=.5, t="out_quad")
        show_card_animation.start(card)

    @staticmethod
    def hide_card(card):
        hide_card_animation = Animation(y=-card.height, d=.5, t="out_quad")
        hide_card_animation.start(card)

    @staticmethod
    def change_profile_pic():
        pass

    def start_text_animation(self):
        # Disable the button and tweak its appearance
        self.root.get_screen("insight_screen1").ids.generate_button.disabled = True
        self.root.get_screen("insight_screen1").ids.generate_button.text = "Next insight in 24hrs..."
        self.root.get_screen("insight_screen1").ids.btn_bg.md_bg_color = (.6, .6, 1, .1)
        self.root.get_screen("insight_screen1").ids.btn_bg.radius = dp(0)

        # Loop through all tabs and start animations
        for tab_id, tab_data in self.tab_insights.items():
            tab_data["label"].text = ""
            tab_data["label"].bind(texture_size=lambda instance, value: self.update_label_height(instance))
            Clock.schedule_once(lambda dt, t_id=tab_id: self.animate_text(t_id), 0.023)

        # Schedule re-enabling the button after every 24hrs
        Clock.schedule_once(lambda dt: self.enable_button(), 24 * 60 * 60)

    def animate_text(self, tab_id, step=0):
        """Animates text chat-gpt style"""
        insight_text = self.tab_insights[tab_id]["text"]
        label = self.tab_insights[tab_id]["label"]

        if step < len(insight_text):
            label.text += insight_text[step]
            Clock.schedule_once(lambda dt: self.animate_text(tab_id, step + 1), 0.023)

    def enable_button(self):
        """Re-enables the generate_insight button after a cooldown of 24hrs"""
        self.root.get_screen("insight_screen1").ids.generate_button.disabled = False
        self.root.get_screen("insight_screen1").ids.generate_button.text = "Generate Insights"
        self.root.get_screen("insight_screen1").ids.btn_bg.md_bg_color = self._white
        self.root.get_screen("insight_screen1").ids.btn_bg.radius = dp(11.5)

    @staticmethod
    def update_label_height(label):
        """Adjusts the height of the label dynamically based on its content."""
        label.height = label.texture_size[1]
        label.size_hint_y = None


if __name__ == "__main__":
    PersonalFinanceTrackerApp().run()
