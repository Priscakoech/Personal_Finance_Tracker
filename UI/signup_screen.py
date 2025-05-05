
import threading
from kivy.app import App
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from requests.exceptions import HTTPError, ConnectionError, Timeout
from kivy.clock import Clock
from UI.reusables import TextFieldNormal, PasswordTextField # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """

<SignUpScreen>:
    name: "signup_screen"
    md_bg_color: app._dark

    MDBoxLayout:
        orientation: "vertical"
        background: "assets/images/bg5.jpg"
        md_bg_color: app._light
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint: (.9, None)
        height: dp(350)
        pos_hint: {"center_x": .5, "top": .98}
        spacing: dp(20)
        radius: dp(23)
        padding: dp(8), dp(23), dp(8), dp(8)

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(52)
            TextFieldNormal:
                id: signup_name
                size_hint: (1, 1)
                hint_text: "Full name"

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(52)
            TextFieldNormal:
                id: signup_mail
                size_hint: (1, 1)
                hint_text: "Email"

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(52)
            PasswordTextField:
                id: signup_pass
                size_hint: (1, 1)
                hint_text: "Password"

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(11.5)

        MDCard:
            md_bg_color: app._blue
            size_hint: (.96, None)
            height: dp(52)
            pos_hint: {"center_x": .5}
            radius: dp(11.5)

            MDRectangleFlatButton:
                text: "Sign Up"
                halign: "center"
                theme_text_color: "Custom"
                text_color: "#ffffff"
                font_size: "20dp"
                size_hint: (1, 1)
                line_color: app._invisible
                _no_ripple_effect: True
                on_release: 
                    root.signup() if len(signup_name.text) >= 6 and len(signup_mail.text) >= 6 and len(signup_pass.text) >= 6 else None

                MDSpinner:
                    id: signup_spinner
                    size_hint: (None, None)
                    size: dp(23), dp(23)
                    pos_hint: {"center_x": .5, "center_y": .5}
                    line_width: 3
                    color: .6, .6, 1, 1
                    active: False

        MDBoxLayout:

"""

Builder.load_string(KV)


class SignUpScreen(MDScreen):
    def __init__(self, store=None, firebase=None, show_snackbar=None, update_ui=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._green =  "#2fc46c"

        self.user_data_store = store
        self.firebase = firebase
        self.show_snackbar = show_snackbar
        self.update_ui = update_ui

        self.u_id = None
        self.id_token = None
        self.refresh_token = None

    def signup(self):
        self.ids.signup_spinner.active = True
        threading.Thread(target=self._signup_thread, daemon=True).start()

    def _signup_thread(self):
        full_name = self.ids.signup_name.text.capitalize()
        email = self.ids.signup_mail.text
        password = self.ids.signup_pass.text

        try:
            user = self.firebase.signup(email=email, password=password)

            if "localId" not in user or "idToken" not in user or "refreshToken" not in user:
                Clock.schedule_once(lambda dt: self._show_error("Firebase response error"), 0)
                return

            self.u_id = user["localId"]
            self.id_token = user["idToken"]
            self.refresh_token = user["refreshToken"]

            self.user_data_store.put("credentials", uid=self.u_id, id_token=self.id_token, refresh_token=self.refresh_token)
            self.user_data_store.put("acc_was_added", status=False)

            self.firebase.put_data(
                id_token=self.id_token,
                path=f"users/{self.u_id}/user_profile",
                data={"Full name": full_name, "Email Address": email}
            )

            Clock.schedule_once(lambda dt: self._on_signup_success(full_name, email), 0)

        except HTTPError as e:
            try:
                error_msg = e.response.json()['error']['message']
                snackbar_msg = self.firebase.get_firebase_error_msg(error_msg)
                Clock.schedule_once(lambda dt: self._show_error(snackbar_msg), 0)
            except:
                Clock.schedule_once(lambda dt: self._show_error("Failed to parse Firebase error!"), 0)
        except (ConnectionError, Timeout):
            Clock.schedule_once(lambda dt: self._show_error("No internet connection!"), 0)
        except Exception:
            Clock.schedule_once(lambda dt: self._show_error("An unexpected error occurred!"), 0)

    def _on_signup_success(self, full_name, email):
        self.ids.signup_spinner.active = False
        Clock.schedule_once(lambda dt: self.show_snackbar(text="Successfully created an account!", background=self._green), 0)
        self.ids.signup_name.text = ""
        self.ids.signup_mail.text = ""
        self.ids.signup_pass.text = ""
        Clock.schedule_once(lambda dt: self.update_ui(name=full_name, email=email), 0)
        Clock.schedule_once(lambda dt: self.go_to_wallet_setup(), 2)

    def _show_error(self, message):
        self.ids.signup_spinner.active = False
        self.show_snackbar(text=message)

    @staticmethod
    def go_to_wallet_setup():
        App.get_running_app().root.current = "wallet_setup_screen"
