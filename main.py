
import os
import calendar
from datetime import datetime, timedelta
from kivy.app import App
from kivy.properties import StringProperty
from kivy.utils import platform, get_color_from_hex
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import FadeTransition
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.snackbar import Snackbar
from kivymd.utils.set_bars_colors import set_bars_colors

from UI.welcome_screen import WelcomeScreen
from UI.home_screen import HomeScreen
from UI.onboarding_screen import OnboardingScreen
from UI.privacy_policy_screen import PrivacyPolicyScreen
from UI.terms_of_use_screen import TermsOfUseScreen
from UI.wallet_setup_screen import WalletSetupScreen
from UI.transactions_screen import TransactionsScreen
from UI.transaction_knowledge_base_screen import TransactionKBScreen
from UI.settings_screen import SettingsScreen
from UI.personal_info_screen import PersonalInfoScreen
from UI.reports_screen import ReportsScreen
from UI.no_internet_screen import NoInternetScreen

from BACKEND.firebase_rest import FirebaseREST
from BACKEND.data_handler import DataHandler
from BACKEND.message_parser import MpesaMessageParser


# this window size is for development purposes only...
# Window.size = (386, 723)


if platform == 'android':
    from android.storage import app_storage_path # type: ignore
    path = app_storage_path()

else: path = os.getcwd()

user_data_store = JsonStore(os.path.join(path, "lightweight_user_data.json"))
text_insights_store = JsonStore(os.path.join(path, "text_insights_data.json"))


class PersonalFinanceTrackerApp(MDApp):
    screen_manager, screen_stack = None, []
    firebase, uid, id_token, refresh_token = None, None, None, None
    full_name, email_address, profile_photo = StringProperty(""), StringProperty(""), StringProperty("")

    def __init__(self):
        super().__init__()
        self.title = "Personal Finance Tracker"
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        self.data_handler = DataHandler()

        # colors
        self._dark, self._tinted, self._light, self._white, self._gray, self._blue, self._green, self._invisible, self._red, self._lightgray = (
            "#00001fff", (.6, .6, 1, .1), "#c800f0", "#dddddd", "#a6a6a6", "#005eff", "#2fc46c", (1, 1, 1, 0), "#ff2f3f", "#aaaaaa26"
        )

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


    def build(self):
        set_bars_colors(get_color_from_hex(self._dark), get_color_from_hex(self._dark), "Light")
        self.firebase = FirebaseREST()

        self.screen_manager = MDScreenManager(transition=FadeTransition(duration=.2, clearcolor=self._dark))
        self.screen_manager.add_widget(HomeScreen(user_data_store=user_data_store, firebase=self.firebase, text_insights_store=text_insights_store))
        self.screen_manager.add_widget(OnboardingScreen(store=user_data_store, firebase=self.firebase, show_snackbar=self.show_snackbar, update_ui=self.update_ui))
        self.screen_manager.add_widget(PrivacyPolicyScreen())
        self.screen_manager.add_widget(TermsOfUseScreen())
        self.screen_manager.add_widget(WalletSetupScreen(store=user_data_store, firebase=self.firebase, show_snackbar=self.show_snackbar, hide_card=self.hide_card, card_to_show_or_hide=self.card_to_show_or_hide))
        self.screen_manager.add_widget(TransactionsScreen())
        self.screen_manager.add_widget(TransactionKBScreen(firebase=self.firebase, user_data_store=user_data_store))
        self.screen_manager.add_widget(SettingsScreen(store=user_data_store, snackbar=self.show_snackbar))
        self.screen_manager.add_widget(PersonalInfoScreen(store=user_data_store, snackbar=self.show_snackbar))
        self.screen_manager.add_widget(ReportsScreen())

        self.enter_app(screen_manager=self.screen_manager)

        return self.screen_manager

    def on_start(self):
        Window.bind(on_keyboard=self.on_keyboard)
        if platform == "android": self.start_message_listener()

    def enter_app(self, screen_manager):
        self.profile_photo = "assets/images/default_avatar.jpg"
        if user_data_store.exists("profile_photo"): self.profile_photo = user_data_store.get("profile_photo")["location"]

        if user_data_store.exists("acc_was_added") and user_data_store.get("acc_was_added")["status"] == False:
            screen_manager.current = "wallet_setup_screen"

        elif user_data_store.exists("credentials") and user_data_store.exists("acc_was_added") and user_data_store.get("acc_was_added")["status"] == True:
            refresh_token = user_data_store.get("credentials")["refresh_token"]
            id_token, uid = self.refresh_id_token(refresh_token=refresh_token)

            if id_token:
                full_name = self.firebase.get_data(id_token=id_token, path=f"users/{uid}/user_profile")["Full name"]
                email = self.firebase.get_data(id_token=id_token, path=f"users/{uid}/user_profile")["Email Address"]
                screen_manager.current = "home_screen"
                Clock.schedule_once(lambda dt: self.update_ui(name=full_name, email=email), 0)
                self.load_user_data(id_token=id_token, uid=uid, full_name=full_name)

            elif refresh_token == "": screen_manager.current = "onboarding_screen"

            else:
                no_internet_screen = NoInternetScreen()
                no_internet_screen.enter_app_callback = self.enter_app
                screen_manager.add_widget(no_internet_screen)
                screen_manager.current = "no_internet_screen"

        else:
            screen_manager.add_widget(WelcomeScreen(switch_screen=self.switch_screen))
            screen_manager.current = "welcome_screen"

    def load_user_data(self, id_token, uid, full_name):
        existing_raw_data = self.firebase.get_data(id_token=id_token, path=f"users/{uid}/raw_data")
        next_key = WalletSetupScreen().get_next_account_key(existing_raw_data)
        prev_number = int(next_key.split("_")[1]) - 1
        prev_key = f"account_{prev_number}"
        transactions = self.firebase.get_data(id_token=id_token, path=f"users/{uid}/raw_data/{prev_key}")
        user_phone = self.firebase.get_data(id_token=id_token, path=f"users/{uid}/raw_data/{prev_key}")["Account ID"]
        user_data_store.put("user_phone", user_phone=user_phone)

        if transactions and "Transactions" in transactions: transactions = transactions["Transactions"]
        else: transactions = []

        try:
          existing_kb = self.firebase.get_data(
              id_token=id_token,
              path=f"users/{uid}/knowledge_base"
          )
        except Exception: existing_kb = {}

        knowledge_base = {}

        if existing_kb and "Knowledge Base" in existing_kb:
            knowledge_base = existing_kb["Knowledge Base"]

        self.data_handler.parser = MpesaMessageParser(
            raw_data=transactions,
            user_name=full_name.capitalize(),
            user_data_store=user_data_store,
            firebase=self.firebase, id_token=id_token, uid=uid,
            knowledge_base=knowledge_base
        )

        self.data_handler.all_transactions = self.data_handler.parser.get_parsed_msgs()

    def greeting_text(self):
        if 0 <= self.current_hour <= 11: return "Good Morning,"
        if 12 <= self.current_hour <= 15: return "Good Afternoon,"
        if 16 <= self.current_hour <= 23: return "Good Evening,"

    def update_ui(self, name, email):
        self.full_name = name
        self.email_address = email
        self.profile_photo = ""
        if user_data_store.exists("profile_photo"): self.profile_photo = user_data_store.get("profile_photo")["location"]
        else: self.profile_photo = "assets/images/default_avatar.jpg"

        h_screen = self.root.get_screen("home_screen") # h means home
        s_screen = self.root.get_screen("settings_screen") # s means settings
        pi_screen = self.root.get_screen("personal_info_screen") # pi means personal info

        h_screen.ids.home_dp.source = self.profile_photo
        h_screen.ids.greetings.text = f"[color=a6a6a6]{self.greeting_text()}[/color] [size=18dp]{self.full_name.split()[0]}[/size]"
        s_screen.ids.settings_dp.source = self.profile_photo
        s_screen.ids.settings_name.text = self.full_name
        s_screen.ids.settings_mail.text = self.email_address
        pi_screen.ids.pi_dp.source = self.profile_photo
        pi_screen.ids.pi_name.text = f"[color=a6a6a6][size=14dp][b]Full name[/b][/size][/color]\n{self.full_name}"
        pi_screen.ids.pi_mail.text = f"[color=a6a6a6][size=14dp][b]Email address[/b][/size][/color]\n{self.email_address}"

    def start_message_listener(self):
        Clock.schedule_interval(self.get_new_mpesa_messages, 360)

    def get_new_mpesa_messages(self, dt):
        wallet_setup_screen = App.get_running_app().root.get_screen("wallet_setup_screen")
        if user_data_store.exists("mpesa_acc_was_added") and user_data_store.get("mpesa_acc_was_added")["status"] == True:
            wallet_setup_screen.fetch_mpesa_messages(silent=True)

    def go_back(self):
        if self.root.current == "home_screen":
            if self.root.get_screen("home_screen").ids.bottom_nav.current != "home_tab":
                self.root.get_screen("home_screen").ids.bottom_nav.switch_tab("home_tab")
                self.root.get_screen("home_screen").ids.bottom_nav.current = "home_tab"
                return True
            return False

        if self.screen_stack:
            self.root.current = self.screen_stack.pop()
            return True
        return False

    def on_keyboard(self, window, key, *args):
        if key == 27 or key == 1001:
            if self.root.current == "wallet_setup_screen" or self.root.current == "welcome_screen" or self.root.current == "onboarding_screen" or self.root.get_screen("home_screen").ids.bottom_nav.current == "home_tab":
                return False
            self.go_back()
            return True

    def switch_screen(self, screen_name):
        self.root.transition = FadeTransition(duration=.2, clearcolor=self._dark)
        current_screen = self.root.current
        if current_screen != screen_name:
            self.screen_stack.append(current_screen)
            self.root.current = screen_name

    def card_to_show_or_hide(self, card_id):
        card = None
        reports_screen = self.root.get_screen("reports_screen")
        wallet_setup_screen = self.root.get_screen("wallet_setup_screen")
        if card_id == "daily_report_card": card = reports_screen.ids.daily_report_card
        if card_id == "weekly_report_card": card = reports_screen.ids.weekly_report_card
        if card_id == "monthly_report_card": card = reports_screen.ids.monthly_report_card
        if card_id == "yearly_report_card": card = reports_screen.ids.yearly_report_card
        if card_id == "add_mpesa_acc_card": card = wallet_setup_screen.ids.add_mpesa_acc_card
        if card_id == "add_paypal_acc_card": card = wallet_setup_screen.ids.add_paypal_acc_card
        if card_id == "add_crypto_wallet_card": card = wallet_setup_screen.ids.add_crypto_wallet_card
        if card_id == "coming_soon_info_card": card = wallet_setup_screen.ids.coming_soon_info_card

        return card

    def show_card(self, card):
        show_card_animation = Animation(y=0, d=.3, t="out_quad")
        show_card_animation.start(card)

    def hide_card(self, card):
        hide_card_animation = Animation(y=-card.height, d=.3, t="out_quad")
        hide_card_animation.start(card)

    @staticmethod
    def show_snackbar(text, background="#ff2f3f"):
        Snackbar(
            text=f"{text}", font_size=dp(16), bg_color=background,
            snackbar_animation_dir="Top", snackbar_x="20dp",
            snackbar_y=Window.height - dp(96),
            radius=[11.5, 11.5, 11.5, 11.5],
            size_hint_x=(
                Window.width - (dp(20) * 2)
            ) / Window.width
        ).open()

    def refresh_id_token(self, refresh_token):
        try:
            res = self.firebase.refresh_token(refresh_token=refresh_token)
            new_id_token = res['id_token']
            new_refresh_token = res['refresh_token']
            uid = res['user_id']

            user_data_store.put("credentials", uid=uid, id_token=new_id_token, refresh_token=new_refresh_token)
            return new_id_token, uid

        except Exception as e:
            self.show_snackbar(text="Failed to refresh token!")
            if self.screen_manager.current == "no_internet_screen":
                NoInternetScreen().show_no_internet()
            return None, None


if __name__ == "__main__":
    PersonalFinanceTrackerApp().run()
