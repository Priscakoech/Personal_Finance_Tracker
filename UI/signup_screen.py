
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
        full_name = self.ids.signup_name.text
        email = self.ids.signup_mail.text
        password = self.ids.signup_pass.text

        try:
            user = self.firebase.signup(email=email, password=password)

            if "localId" not in user or "idToken" not in user or "refreshToken" not in user:
                raise ValueError("Invalid response from Firebase")

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

            Clock.schedule_once(lambda dt: self.show_snackbar(text="Successfully created an account!", background=self._green), 0)
            self.ids.signup_name.text = ""
            self.ids.signup_mail.text = ""
            self.ids.signup_pass.text = ""

            Clock.schedule_once(lambda dt: self.go_to_wallet_setup(), 4)

            full_name = self.firebase.get_data(id_token=self.id_token, path=f"users/{self.u_id}/user_profile")["Full name"]
            email = self.firebase.get_data(id_token=self.id_token, path=f"users/{self.u_id}/user_profile")["Email Address"]
            self.update_ui(name=full_name, email=email)

            return True

        except HTTPError as e:
            try:
                error_msg = e.response.json()['error']['message']
                snackbar_msg = self.firebase.get_firebase_error_msg(error_msg)
                self.show_snackbar(text=snackbar_msg)
            except Exception: self.show_snackbar(text="Failed to parse Firebase error!")
        except (ConnectionError, Timeout): self.show_snackbar(text="No internet connection!")
        except Exception: self.show_snackbar(text="An unexpected error occurred!")


    @staticmethod
    def go_to_wallet_setup():
        App.get_running_app().root.current = "wallet_setup_screen"
