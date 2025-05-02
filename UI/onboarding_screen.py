
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import FadeTransition
from UI.signin_screen import SignInScreen
from UI.signup_screen import SignUpScreen
from UI.reusables import TextFieldNormal, PasswordTextField # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """
<OnboardingScreen>:
    name: "onboarding_screen"
    md_bg_color: app._dark

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(1.63)
        padding: dp(0), dp(23), dp(0), dp(0)

        MDBoxLayout:
            size_hint: (.4, None)
            height: dp(100)
            spacing: dp(17.5)
            padding: dp(23)
            pos_hint: {"center_x": .52}

            MDBoxLayout:
                size_hint: (None, None)
                size: ("36dp", "36dp")
                pos_hint: {"center_y": .5}

                Image:
                    source: "assets/images/pft_icon.png"
                    size_hint: (1, 1)
                    pos_hint: {"center_x": .5, "center_y": .46}

            MDBoxLayout:
                size_hint: (None, 1)
                width: dp(48)
                CustomLabel:
                    text: "[b][size=21dp]pft[/size][/b]"
                    text_color: "#ffffff"
                    
        MDBoxLayout:
            md_bg_color: app._dark
            orientation: "vertical"
            padding: dp(0), dp(10), dp(0), dp(8)
            spacing: dp(12.5)

            MDBoxLayout:
                size_hint: (.6, None)
                height: dp(54)
                pos_hint: {"center_x": .5}
                orientation: "horizontal"
                spacing: dp(23)
                padding: dp(8)
                radius: dp(11.5)

                MDCard:
                    md_bg_color: app._invisible
                    orientation: "vertical"
                    size_hint: (1, 1)
                    radius: dp(12)
                    on_release: 
                        signin_tab.md_bg_color = app._blue if signup_tab.md_bg_color == app._blue else  app._blue
                        signup_tab.md_bg_color = app._invisible
                        root.switch_onboarding_tab("signin_screen")

                    CustomLabel:
                        text: "[size=19dp]Sign In[/size]"
                        halign: "center"
                        text_color: "#ffffff"

                    MDBoxLayout:
                        id: signin_tab
                        md_bg_color: app._blue
                        size_hint: (1, None)
                        height: dp(3)

                MDCard:
                    orientation: "vertical"
                    md_bg_color: app._invisible
                    size_hint: (1, 1)
                    radius: dp(12)
                    on_release: 
                        signup_tab.md_bg_color = app._blue if signin_tab.md_bg_color == app._blue else  app._blue
                        signin_tab.md_bg_color = app._invisible
                        root.switch_onboarding_tab("signup_screen")

                    CustomLabel:
                        text: "[size=19dp]Sign Up[/size]"
                        halign: "center"
                        text_color: "#ffffff"

                    MDBoxLayout:
                        id: signup_tab
                        size_hint: (1, None)
                        height: dp(3)

            MDScreenManager:
                id: onboarding_screen_manager

"""

Builder.load_string(KV)


class OnboardingScreen(MDScreen):
    def __init__(self, store=None, firebase=None, show_snackbar=None, update_ui=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dark = "#00001fff"

        self.user_data_store = store
        self.firebase = firebase
        self.show_snackbar = show_snackbar
        self.update_ui = update_ui


    def on_enter(self, *args):
        if not hasattr(self, 'onboarding_screens_loaded'):
            signin_screen = SignInScreen(
                store=self.user_data_store, firebase=self.firebase, show_snackbar=self.show_snackbar, update_ui=self.update_ui
            )

            signup_screen = SignUpScreen(
                store=self.user_data_store, firebase=self.firebase, show_snackbar=self.show_snackbar, update_ui=self.update_ui
            )

            self.ids.onboarding_screen_manager.add_widget(signin_screen)
            self.ids.onboarding_screen_manager.add_widget(signup_screen)
            self.onboarding_screens_loaded = True

    def switch_onboarding_tab(self, screen_name):
        self.ids.onboarding_screen_manager.transition = FadeTransition(duration=.2, clearcolor=self._dark)
        self.ids.onboarding_screen_manager.current = screen_name
