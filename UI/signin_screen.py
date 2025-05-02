
from kivy.app import App
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from requests.exceptions import HTTPError, ConnectionError, Timeout
from kivy.clock import Clock
from UI.reusables import TextFieldNormal, PasswordTextField, CustomInputDialog # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """
<SignInScreen>:
    name: "signin_screen"
    md_bg_color: app._dark

    MDBoxLayout:
        background: "assets/images/bg5.jpg"
        md_bg_color: app._light
        radius: dp(23)
        orientation: "vertical"
        size_hint: (.9, None)
        height: dp(290)
        pos_hint: {"center_x": .5, "top": .98}
        orientation: "vertical"
        spacing: dp(20)
        padding: dp(8), dp(23), dp(8), dp(8)

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(52)
            TextFieldNormal:
                id: signin_mail
                size_hint: (1, 1)
                hint_text: "Email"

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(52)
            PasswordTextField:
                id: signin_pass
                size_hint: (1, 1)
                hint_text: "Password"

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(17.5)
            padding: dp(8), dp(-43), dp(0), dp(8)

            MDBoxLayout:
                size_hint: (1, 1)

            MDTextButton:
                size_hint: (None, None)
                size: ("153dp", "36dp")
                text: " Forgot Password?"
                theme_text_color: "Custom"
                text_color: "#ffffff"
                font_size: "18dp"
                on_release: root.open_password_reset_dialog()

        MDCard:
            md_bg_color: app._blue
            size_hint: (.96, None)
            height: dp(52)
            pos_hint: {"center_x": .5}
            radius: dp(11.5)

            MDRectangleFlatButton:
                text: "Sign In"
                halign: "center"
                theme_text_color: "Custom"
                text_color: "#ffffff"
                font_size: "20dp"
                size_hint: (1, 1)
                line_color: app._invisible
                _no_ripple_effect: True
                on_release:
                    root.signin() if len(signin_mail.text) >= 6 and len(signin_pass.text) >= 6 else None

        MDBoxLayout:

"""

Builder.load_string(KV)


class SignInScreen(MDScreen):
    def __init__(self, store=None, firebase=None, show_snackbar=None, update_ui=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._green =  "#2fc46c"
        self.input_dialog = None

        self.user_data_store = store
        self.firebase = firebase
        self.show_snackbar = show_snackbar
        self.update_ui = update_ui

        self.u_id = None
        self.id_token = None
        self.refresh_token = None

    def signin(self):
        email, password = self.ids.signin_mail.text, self.ids.signin_pass.text

        try:
            user = self.firebase.signin(email=email, password=password)

            if "localId" not in user or "idToken" not in user or "refreshToken" not in user:
                raise ValueError("Invalid response from Firebase")

            self.u_id = user["localId"]
            self.id_token = user["idToken"]
            self.refresh_token = user["refreshToken"]
            self.user_data_store.put("credentials", uid=self.u_id, id_token=self.id_token, refresh_token=self.refresh_token)

            Clock.schedule_once(lambda dt: self.show_snackbar("Successfully logged in!", background=self._green), 0)
            self.ids.signin_mail.text = ""
            self.ids.signin_pass.text = ""

            full_name = self.firebase.get_data(id_token=self.id_token, path=f"users/{self.u_id}/user_profile")["Full name"]
            email = self.firebase.get_data(id_token=self.id_token, path=f"users/{self.u_id}/user_profile")["Email Address"]
            self.update_ui(name=full_name, email=email)
            App.get_running_app().load_user_data(id_token=self.id_token, uid=self.u_id, full_name=full_name)
            Clock.schedule_once(lambda dt: self.go_to_home(), 4)

            return True

        except HTTPError as e:
            try:
                error_msg = e.response.json()['error']['message']
                snackbar_msg = self.firebase.get_firebase_error_msg(error_msg)
                self.show_snackbar(text=snackbar_msg)
            except: self.show_snackbar(text="Failed to parse Firebase error!")
        except (ConnectionError, Timeout): self.show_snackbar(text="No internet connection!")
        except Exception: self.show_snackbar(text="An unexpected error occurred!")

    def open_password_reset_dialog(self):
        self.input_dialog = CustomInputDialog()
        self.input_dialog.open()

    def request_password_reset_link(self, email):
        try:
            self.firebase.send_password_reset_email(email=email)
            Clock.schedule_once(lambda dt: self.show_snackbar("Password Reset Link sent to your email!", background=self._green), 2)
            self.input_dialog.dismiss()
        except (ConnectionError, Timeout): self.show_snackbar("No internet connection!")
        except Exception: self.show_snackbar("An unexpected error occurred!")

    @staticmethod
    def go_to_home():
        App.get_running_app().root.current = "home_screen"
