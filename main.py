from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivy.uix.screenmanager import SlideTransition, NoTransition, CardTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.textfield import MDTextField
from kivymd.utils.set_bars_colors import set_bars_colors
from datetime import datetime, timedelta
import re
import calendar
import webbrowser


# from openai import OpenAI
# from kivy.core.window import Window

#Window.softinput_mode = "pan"

# ############################################## API KEYS ###############################################

# ------------------------------------------- GOOGLE AUTH -----------------------------------------------
CLIENT_ID = ""
CLIENT_SK = ""

# -------------------------------------------- OPENAI --------------------------------------------------
OPENAI_API_KEY = ""

# --------------------------------------- GOOGLE AUTHENTICATION ----------------------------------------
# from kivyauth.google_auth import initialize_google, login_google, logout_google


UI = """

# ########################################### CUSTOM WIDGETS ###########################################
<TopLeftBackButton>:
    icon: "arrow-left"
    pos_hint: {"center_x": .1, "center_y": .935}
    theme_text_color: "Custom"
    text_color: app._dark
    _no_ripple_effect: True

<TextFieldNormal>:
    size_hint_x: .85
    mode: "rectangle"
    line_color_focus: app._white
    line_color_normal: app._white
    text_color_focus: app._white
    text_color_normal: app._white
    hint_text_color_focus: app._white
    hint_text_color_normal: app._white
    icon_right_color_focus: app._white
    icon_right_color_normal: app._white

<PasswordTextField>:
    size_hint: .85, None
    height: password.height - 10

    MDTextField:
        id: password
        hint_text: root.hint_text
        text: root.text
        password: True
        mode: "rectangle"
        line_color_focus: app._white
        line_color_normal: app._white
        text_color_focus: app._white
        text_color_normal: app._white
        hint_text_color_focus: app._white
        hint_text_color_normal: app._white

    MDIconButton:
        icon: "eye-off"
        pos_hint: {"center_y": .5}
        pos: password.width - self.width, 0
        theme_icon_color: "Custom"
        icon_color: app._white
        _no_ripple_effect: True
        on_release:
            self.icon = "eye" if self.icon == "eye-off" else "eye-off"
            password.password = False if password.password is True else True

<CustomCardBackground>:
    md_bg_color: app._white
    size_hint: (.9, .08)
    radius: dp(11.5), dp(11.5), dp(11.5), (11.5)

<DynamicCard>:
    md_bg_color: app._dark
    size_hint: (1, .8)
    pos_hint: {"center_x": .5, "center_y": .4}
    padding: (0, 40, 0, 100)
    radius: dp(30), dp(30), dp(0), dp(0)

<CustomTabs>:
    indicator_color: app._blue
    text_color_active: app._blue
    text_color_normal: app._gray
    tab_indicator_anim: True
    background_color: app._invisible
    underline_color: app._invisible
    
<InsightCard>:
    size_hint: (1, 1)
    pos_hint: {"center_x": .5, "center_y": .5}
    padding: (6, 100)
    md_bg_color: app._dark
    padding: dp(6), dp(11.5)

<HiddenCard>:
    md_bg_color: app._green
    background: "assets/images/bg5.jpg"
    size_hint: 1, .55
    y: -self.height
    pos_hint: {"center_x": .5}
    radius: dp(46), dp(46), dp(0), dp(0)
    padding: dp(23)

<CLoseCardButton>:
    _no_ripple_effect: True
    icon: "close"
    theme_text_color: "Custom"
    text_color: app._white
    md_bg_color: app._invisible
    size_hint_y: .9
    pos_hint: {"center_y": .5, "left": 1}


# ############################################### SCREENS ################################################

# -------------------------------------------- WELCOME SCREEN --------------------------------------------
<WelcomeScreen>:
    name: "welcome_screen"
    md_bg_color: app._dark

    Image:
        source: "assets/images/pft_logo.png"
        size_hint: (.75, .75)
        pos_hint: {"center_x": .5, "center_y": .7}

    MDLabel:
        padding: dp(25)
        text: "Track, Get Insights, and Visualize the flow of your finances easily."
        font_style: "H4"
        bold: True
        pos_hint: {"center_y": .4}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._gray

    # get started btn
    MDCard:
        md_bg_color: app._white
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .18}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        on_release: app.change_screen_wt("onboarding_screen", "left")

        MDBoxLayout:
            padding: (96, 0)
            MDLabel:
                text: "Get started"
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._dark
                font_size: "18dp"

            MDIcon:
                icon: "arrow-right"
                halign: "center"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app._dark

    MDLabel:
        text: "By tapping on 'Get started', you are accepting our\\n" +\
            "[ref=privacy][u][color=00afff]Privacy Policy[/color][/u][/ref] and " +\
            "[ref=terms][u][color=00afff]Terms of Use[/color][/u][/ref]"
        markup: True
        font_style: "Subtitle2"
        pos_hint: {"center_y": .063}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._gray
        on_ref_press: app.goto_hyperlink(args[1])


# -------------------------------------------- ONBOARDING SCREEN --------------------------------------------
<OnboardingScreen>:
    name: "onboarding_screen"
    md_bg_color: app._dark

    TopLeftBackButton:
        text_color: app._white
        on_release: app.change_screen_wt("welcome_screen", "right")

    Image:
        source: "assets/images/onboarding.png"
        size_hint: (1, .5)
        pos_hint: {"center_x": .5, "center_y": .7}

    MDLabel:
        text: "Let's get you\\nonboard!"
        bold: True
        padding: dp(25)
        font_style: "H4"
        pos_hint: {"center_y": .35}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._gray

    # continue with google btn
    MDCard:
        md_bg_color: app._white
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .18}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: True

        MDRectangleFlatIconButton:
            icon: "assets/images/google_icon.png"
            text: "        Continue with Google"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._dark
            font_size: "18dp"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: 
                app.open_browser()
                app.change_screen_wt("full_name_input_screen", "left")

    MDLabel:
        text: "'Continue with Google' action will complete in your\\nweb browser."
        padding: dp(27)
        font_style: "Subtitle2"
        pos_hint: {"center_y": .06}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._gray


# ------------------------------------------ FULL NAME SCREEN -------------------------------------------
<FullNameScreen>:
    name: "full_name_input_screen"
    md_bg_color: app._dark

    TopLeftBackButton:
        text_color: app._white
        on_release: app.change_screen_wt("onboarding_screen", "right")

    MDLabel:
        text: "Enter your full name"
        bold: True
        padding: dp(25)
        font_style: "H5"
        pos_hint: {"center_y": .85}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._gray

    TextFieldNormal:
        id: first_name
        hint_text: "First name"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .75}
        on_text: app.enable_submit_btn()

    TextFieldNormal:
        id: last_name
        hint_text: "Last name"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .64}
        on_text: app.enable_submit_btn()

    # submit full name btn
    MDCard:
        id: submit_btn_bg
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .52}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: False

        MDRectangleFlatIconButton:
            id: submit_btn
            disabled: True
            text: "Submit"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._dark
            font_size: "18dp"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: 
                app.get_name()
                app.change_screen_wt("wallet_setup_screen", "left")


# -------------------------------------------- PRIVACY POLICY SCREEN ---------------------------------------      
<PrivacyPolicyScreen>:
    name: "privacy_policy_screen"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .95}    
        radius: dp(11.5)

        TopLeftBackButton:
            text_color: app._white
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("welcome_screen", "right")

        MDLabel:
            padding: (23, 0)
            text: "Privacy Policy"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: app._white
            pos_hint: {"center_y": .5}
            halign: "right"

# -------------------------------------------- TERMS OF USE SCREEN -----------------------------------------
<TermsOfUseScreen>:
    name: "terms_of_use_screen"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .95}    
        radius: dp(11.5)

        TopLeftBackButton:
            text_color: app._white
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("welcome_screen", "right")

        MDLabel:
            padding: (23, 0)
            text: "Terms of Use"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: app._white
            pos_hint: {"center_y": .5}
            halign: "right"

# -------------------------------------------- WALLET SETUP SCREEN ------------------------------------------
<WalletSetupScreen>
    name: "wallet_setup_screen"
    md_bg_color: app._dark

    TopLeftBackButton:
        theme_text_color: "Custom"
        text_color: app._white
        on_release: app.change_screen_wt("onboarding_screen", "right")

    Image:
        source: "assets/images/link_icon.png"
        size_hint: (.25, .25)
        pos_hint: {"center_x": .5, "center_y": .78}

    MDLabel:
        text: "Link a Wallet"
        bold: True
        padding: dp(25)
        font_style: "H4"
        pos_hint: {"center_y": .65}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._gray

    # ------------------------- account options --------------------------
    # ----- mpesa ------
    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.4, .18)
        pos_hint: {"center_x": .275, "center_y": .423}    
        radius: dp(23)
        padding: dp(20)
        on_release: app.change_screen_wt("add_mpesa_acc_screen", "left")

        MDRelativeLayout:
            orientation: "vertical"
            Image:
                source: "assets/images/mpesa_icon.png"
                size_hint: (.6, .6)
                pos_hint: {"center_x": .5, "center_y": .7}

            MDLabel:
                text: "m-pesa"
                font_style: "Body1"
                pos_hint: {"center_y": .15}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._white

    # ----- card ------
    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.4, .18)
        pos_hint: {"center_x": .725, "center_y": .423}    
        radius: dp(23)
        padding: dp(20)
        on_release: app.change_screen_wt("add_card_screen", "left")

        MDRelativeLayout:
            orientation: "vertical"
            Image:
                source: "assets/images/card_icon1.png"
                size_hint: (.7, .7)
                pos_hint: {"center_x": .5, "center_y": .7}

            MDLabel:
                text: "Card"
                font_style: "Body1"
                pos_hint: {"center_y": .15}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._white

    # ----- paypal ------
    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.4, .18)
        pos_hint: {"center_x": .275, "center_y": .21}    
        radius: dp(23)
        padding: dp(20)
        on_release: app.change_screen_wt("add_paypal_acc_screen", "left")

        MDRelativeLayout:
            orientation: "vertical"
            Image:
                source: "assets/images/paypal_icon.png"
                size_hint: (.6, .6)
                pos_hint: {"center_x": .5, "center_y": .7}

            MDLabel:
                text: "PayPal"
                font_style: "Body1"
                pos_hint: {"center_y": .15}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._white

    # ----- crypto -----
    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.4, .18)
        pos_hint: {"center_x": .725, "center_y": .21}    
        radius: dp(23)
        padding: dp(20)
        on_release: app.change_screen_wt("add_crypto_wallet_screen", "left")

        MDRelativeLayout:
            orientation: "vertical"
            Image:
                source: "assets/images/crypto_icon.png"
                size_hint: (.7, .7)
                pos_hint: {"center_x": .5, "center_y": .7}

            MDLabel:
                text: "Crypto"
                font_style: "Body1"
                pos_hint: {"center_y": .15}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._white


# ----------------------------------------- ADD MPESA ACCOUNT SCREEN ----------------------------------------
<AddMpesaAccScreen>:
    name: "add_mpesa_acc_screen"
    md_bg_color: app._dark

    TopLeftBackButton:
        text_color: app._white
        on_release: app.change_screen_wt("wallet_setup_screen", "right")

    MDLabel:
        text: "Link Your M-Pesa Account"
        bold: True
        padding: dp(25)
        font_style: "H5"
        pos_hint: {"center_y": .85}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._gray

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.87, .2)
        pos_hint: {"center_x": .5, "center_y": .7}    
        radius: dp(11.5)
        padding: dp(11.5)

        MDBoxLayout:
            MDIcon:
                icon: "information"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app._gray

            MDLabel:
                text: "This action requires you to grant the app permission to access your messages." +\
                    "\\n" + "\\nMake sure that the phone number you are providing, has it's corresponding" +\
                     " SIM Card mounted on this device."
                padding: dp(11.5)
                size_hint_y: None
                pos_hint: {"center_y": .5}
                font_style: "Subtitle2"
                halign: "left"
                theme_text_color: "Custom"
                text_color: app._gray

    TextFieldNormal:
        id: mpesa_phone_number
        hint_text: "M-Pesa Phone Number"
        input_type: "number" 
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .52}

    # add mpesa account  btn
    MDCard:
        md_bg_color: app._green
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .4}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: True

        MDRectangleFlatIconButton:
            text: "Submit"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._dark
            font_size: "36px"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.change_screen_wt("home_screen", "left")


# ------------------------------------------- ADD CARD SCREEN ----------------------------------------
<AddCardScreen>:
    name: "add_card_screen"
    md_bg_color: app._dark

    TopLeftBackButton:
        text_color: app._white
        on_release: app.change_screen_wt("wallet_setup_screen", "right")

    MDLabel:
        text: "Link Your Card"
        bold: True
        padding: dp(25)
        font_style: "H5"
        pos_hint: {"center_y": .85}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._gray

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.87, .09)
        pos_hint: {"center_x": .5, "center_y": .75}    
        radius: dp(11.5)
        padding: dp(11.5)

        MDBoxLayout:
            MDIcon:
                icon: "information"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app._gray

            MDLabel:
                text: "Supported cards are [color=0000ff]VISA[/color] and [color=ffaa23]MASTERCARD[/color]"
                markup: True
                padding: dp(11.5)
                size_hint_y: None
                pos_hint: {"center_y": .5}
                font_style: "Subtitle2"
                halign: "left"
                theme_text_color: "Custom"
                text_color: app._gray

    TextFieldNormal:
        id: card_holder_name
        hint_text: "Card holder name"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .65}

    TextFieldNormal:
        id: card_number
        hint_text: "Card number"
        input_type: "number"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .53}

    MDBoxLayout:
        size_hint_x: .85
        orientation: "horizontal"
        spacing: dp(23)
        pos_hint: {"center_x": .5}

        TextFieldNormal:
            id: card_expiry_date
            hint_text: "Expiry"
            multiline: False
            pos_hint: {"center_x": .5, "center_y": .41}

        PasswordTextField:
            id: cvv_number
            hint_text: "CVV"
            input_type: "number"
            multiline: False
            pos_hint: {"center_x": .5, "center_y": .4063}

    # add card btn
    MDCard:
        md_bg_color: app._blue
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .3}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: True

        MDRectangleFlatIconButton:
            text: "Add Card"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._dark
            font_size: "36px"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.change_screen_wt("home_screen", "left")


# ----------------------------------------- ADD PAYPAL ACCOUNT SCREEN ------------------------------------
<AddPaypalAccScreen>:
    name: "add_paypal_acc_screen"
    md_bg_color: app._dark

    TopLeftBackButton:
        text_color: app._white
        on_release: app.change_screen_wt("wallet_setup_screen", "right")

    MDLabel:
        text: "Link Your PayPal Account"
        bold: True
        padding: dp(25)
        font_style: "H5"
        pos_hint: {"center_y": .85}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._gray

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.87, .09)
        pos_hint: {"center_x": .5, "center_y": .73}    
        radius: dp(11.5)
        padding: dp(11.5)

        MDBoxLayout:
            MDIcon:
                icon: "information"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app._gray

            MDLabel:
                text: "This action will complete in your web browser"
                padding: dp(11.5)
                size_hint_y: None
                pos_hint: {"center_y": .5}
                font_style: "Subtitle2"
                halign: "left"
                theme_text_color: "Custom"
                text_color: app._gray

    # add paypal account  btn
    MDCard:
        md_bg_color: app._blue
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .63}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: True

        MDRectangleFlatIconButton:
            text: "Link Paypal Account"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._white
            font_size: "36px"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.change_screen_wt("home_screen", "left")


# ------------------------------------------- ADD CRYPTO WALLET SCREEN ---------------------------------------
<AddCryptoWalletScreen>:
    name: "add_crypto_wallet_screen"
    md_bg_color: app._dark

    TopLeftBackButton:
        text_color: app._white
        on_release: app.change_screen_wt("wallet_setup_screen", "right")

    MDLabel:
        text: "Link Your Crypto Wallet"
        bold: True
        padding: dp(25)
        font_style: "H5"
        pos_hint: {"center_y": .85}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._gray

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.87, .13)
        pos_hint: {"center_x": .5, "center_y": .75}    
        radius: dp(11.5)
        padding: dp(11.5)

        MDBoxLayout:
            MDIcon:
                icon: "information"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app._gray

            MDLabel:
                text: "Supported wallets are:-"
                markup: True
                padding: dp(11.5)
                size_hint_y: None
                pos_hint: {"center_y": .5}
                font_style: "Subtitle2"
                halign: "left"
                theme_text_color: "Custom"
                text_color: app._gray

    TextFieldNormal:
        id: wallet
        hint_text: "Wallet"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .62}

    TextFieldNormal:
        id: wallet_api
        hint_text: "Wallet API"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .5}

    TextFieldNormal:
        id: wallet_chain
        hint_text: "Blockchain Network"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .38}

    TextFieldNormal:
        id: wallet_address
        hint_text: "Wallet Address"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .26}

    # add crypto wallet btn
    MDCard:
        md_bg_color: app._blue
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .15}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: True

        MDRectangleFlatIconButton:
            text: "Add Wallet"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._dark
            font_size: "36px"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.change_screen_wt("home_screen", "left")


# ----------------------------------------------- HOME SCREEN --------------------------------------------
<HomeScreen>:
    name: "home_screen"
    md_bg_color: app._dark

    MDLabel:
        text: f"[color=a6a6a6]{app.greeting_text()}[/color]\\n[size=24sp]{app.full_name}[/size]"
        markup: True
        halign: "left"
        pos_hint: {"center_y": .93}
        theme_text_color: "Custom"
        text_color: app._white
        font_style: "Subtitle1"
        bold: True
        padding: dp(23)

    MDLabel:
        text: "Overview"
        halign: "left"
        pos_hint: {"center_y": .865}
        theme_text_color: "Custom"
        text_color: app._white
        font_style: "Body1"
        bold: True
        padding: dp(23)

    Carousel:
        id: carousel
        loop: True
        scroll_distance: 11.5
        scroll_timeout: 163
        on_index: app.change_indicator_color(self.index)

        MDCard:
            md_bg_color: (.6, .6, 1, .2)
            size_hint: (.95, .34)
            pos_hint: {"center_x": .5, "center_y": .66}
            radius: dp(23)
            padding: dp(8.5)

            MDBoxLayout:
                orientation: "vertical"

                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: dp(8)

                    MDCard:
                        md_bg_color: app._red
                        size_hint: (1, .9)
                        pos_hint: {"center_y": .5}
                        radius: dp(17.5)
                        padding: dp(6)

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                text: f"Today's Spending\\n[size=12sp]Ksh.[/size] [size=18sp]65,543.00[/size]"
                                markup: True
                                padding: dp(6)
                                halign: "center"
                                pos_hint: {"center_y": .75}
                                font_style: "Subtitle2"
                                theme_text_color: "Custom"
                                text_color: app._white

                    MDCard:
                        md_bg_color: app._green
                        size_hint: (1, .9)
                        pos_hint: {"center_y": .5}
                        radius: dp(17.5)
                        padding: dp(6)

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                text: f"Today's Income\\n[size=12sp]Ksh.[/size] [size=18sp]165,543.00[/size]"
                                markup: True
                                padding: dp(6)
                                halign: "center"
                                pos_hint: {"center_y": .75}
                                font_style: "Subtitle2"
                                theme_text_color: "Custom"
                                text_color: app._dark
      
                MDCard:
                    md_bg_color: app._blue
                    size_hint: (1, .35)
                    pos_hint: {"center_x": .5}
                    radius: dp(11.5)
                    padding: dp(6.3)

                    MDLabel:
                        text: "[size=16sp]Account Balance[/size]"
                        markup: True
                        bold: True
                        halign: "left"
                        font_style: "Subtitle1"
                        theme_text_color: "Custom"
                        text_color: app._dark

                    MDLabel:
                        text: f"[size=12sp]Ksh.[/size] 2,454.89"
                        markup: True
                        bold: True
                        halign: "right"
                        font_style: "Subtitle1"
                        theme_text_color: "Custom"
                        text_color: app._dark

        MDCard:
            md_bg_color: "#ffffff"
            size_hint: (.95, .34)
            pos_hint: {"center_x": .5, "center_y": .66}
            radius: dp(23)
            padding: dp(8.5)

            MDRelativeLayout:
                orientation: "vertical"

                Image:
                    id: chart
                    source: "assets/images/income_expenditure_graph.png"
                    size_hint: (1, 1)
                    pos_hint: {"center_x": .5, "center_y": .5}

                MDCard:
                    md_bg_color: app._blue
                    size_hint: (None, None)
                    size: ("46dp", "46dp")
                    pos_hint: {"top": .0863, "right": .98}
                    radius: self.height / 2

                    MDIconButton:
                        icon: "chevron-right"
                        on_release: app.change_screen_wt("insight_screen2", "left")

                MDCard:
                    md_bg_color: app._blue
                    size_hint: (None, None)
                    size: ("46dp", "46dp")
                    pos_hint: {"top": .0863, "right": .8}
                    radius: self.height / 2

                    MDIconButton:
                        icon: "chart-bar"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: 
                            self.icon = "chart-line" if self.icon == "chart-bar" else "chart-bar"
                            app.change_chart()

    # ------------------------- indicators...
    MDBoxLayout:
        orientation: "horizontal"
        size_hint: (None, None)
        size: ("63dp", "23dp")
        pos_hint: {"center_x": .5, "center_y": .47}
        spacing: dp(8.5)
        padding: dp(11.5)

        MDCard:
            id: slide1_indicator_color
            md_bg_color: app._blue
            size_hint: (None, None)
            size: ("7.63dp", "7.63dp")
            pos_hint: {"center_y": .5}
            radius: self.height / 2

        MDCard:
            id: slide2_indicator_color
            md_bg_color: app._gray
            size_hint: (None, None)
            size: ("7.63dp", "7.63dp")
            pos_hint: {"center_y": .5}
            radius: self.height / 2


    # ---------------------- minimalistic "transactions" overview --------------------------  
    MDCard:
        md_bg_color: app._green
        background: "assets/images/bg5.jpg"
        size_hint: 1, .45
        pos_hint: {"center_x": .5, "center_y": .225}
        radius: dp(46), dp(46), dp(0), dp(0)
        padding: dp(23)

        MDCard:
            md_bg_color: app._invisible
            size_hint: (1, .123)
            pos_hint: {"center_x": .5, "top": 1.023}
            padding: dp(0)

            MDLabel:
                text: "Transactions"
                halign: "left"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app._white
                font_style: "Body1"
                bold: True

            MDBoxLayout:
                md_bg_color: app._invisible
                size_hint: (None, 1)
                width: "123dp"

                MDCard:
                    md_bg_color: app._invisible
                    size: (1, 1)
                    on_release: app.change_screen_wt("transactions_screen", "left")

                    MDLabel:
                        text: "View all"
                        halign: "right"
                        pos_hint: {"center_y": .5}
                        theme_text_color: "Custom"
                        text_color: app._gray
                        font_style: "Subtitle1"
                        bold: True
                        padding: dp(6)

                    MDIcon:
                        icon: "chevron-right"
                        halign: "right"
                        pos_hint: {"center_y": .5}    
                        theme_text_color: "Custom"
                        text_color: app._gray    

    MDCard:
        md_bg_color: app._invisible
        size_hint: (.95, .29)
        pos_hint: {"center_x": .5, "top": .37}    
        radius: dp(0)
        padding: dp(0)

        MDScrollView:
            MDList:
                id: minimalistic_transactions

    # ---------------------------- custom bottom navigation bar -----------------------------
    MDCard:
        md_bg_color: app._invisible
        size_hint: (.95, .085)
        pos_hint: {"center_x": .5, "top": .085}    
        radius: dp(11.5)
        padding: dp(20)

        MDBoxLayout:
            orientation: "horizontal"
            spacing: dp(23)

            MDCard:
                md_bg_color: app._invisible
                size_hint: (1, 3)
                pos_hint: {"center_y": .5}    

                MDRelativeLayout:
                    MDIconButton:
                        _no_ripple_effect: True
                        icon: "assets/images/chome_icon.png"
                        pos_hint: {"center_x": .5, "center_y": .5}

            MDCard:
                md_bg_color: app._invisible
                size_hint: (1, 3)
                pos_hint: {"center_y": .5}

                MDRelativeLayout:
                    MDIconButton:
                        _no_ripple_effect: True
                        icon: "assets/images/cwallet_icon.png"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.change_screen_wt("wallet_screen", "left")

            MDCard:
                md_bg_color: app._invisible
                size_hint: (1, 3)
                pos_hint: {"center_y": .5}

                MDRelativeLayout:
                    MDIconButton:
                        _no_ripple_effect: True
                        icon: "assets/images/insight.png"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.change_screen_wt("insight_screen1", "left")

            MDCard:
                md_bg_color: app._invisible
                size_hint: (1, 3)
                pos_hint: {"center_y": .5}

                MDRelativeLayout:
                    MDIconButton:
                        _no_ripple_effect: True
                        icon: "assets/images/csettings_icon.png"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.change_screen_wt("settings_screen", "left")

    # ------------------------------------ User Profile -----------------------------------
    MDCard:
        background: app.profile_photo
        md_bg_color: app._white
        line_color: (.6, .6, 1, .5)
        line_width: dp(2.3)
        size_hint: (None, None)
        width: "63dp"
        height: "63dp"
        radius: self.height / 2
        pos_hint: {"right": .965, "top": .973}
        on_release: app.change_screen_wt("personal_info_screen", "left")


# ---------------------------------------------- TRANSACTIONS SCREEN --------------------------------------------
<TransactionsScreen>:
    name: "transactions_screen"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .95}    
        radius: dp(11.5)

        TopLeftBackButton:
            text_color: app._white
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("home_screen", "right", "pop")

        MDLabel:
            padding: (23, 0)
            text: "Transactions"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: app._white
            pos_hint: {"center_y": .5}
            halign: "center"

        MDIconButton:
            _no_ripple_effect: True
            icon: "assets/images/csettings_icon.png"
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("settings_screen", "left")

    MDCard:
        md_bg_color: app._invisible
        size_hint: (.9, .85)
        pos_hint: {"center_x": .5, "top": .83}    
        radius: dp(11.5)

        CustomTabs:
            Tab:
                title: "All"
    
                MDScrollView:
                    do_scroll_x: False
                    do_scroll_y: True
    
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(20)
                        adaptive_height: True
    
                        # Example for Today's Date
                        MDLabel:
                            text: "Tuesday, 14th January, 2024"
                            font_style: "H6"
                            halign: "left"
                            size_hint_y: None
                            height: dp(46)
    
                        MDCard:
                            md_bg_color: app._green
                            size_hint: (1, None)
                            height: dp(120)
                            radius: dp(11.5)
                            padding: dp(10)
                            BoxLayout:
                                orientation: "vertical"
                                MDLabel:
                                    text: "Transaction ID: 12345"
                                    font_style: "Body1"
                                MDLabel:
                                    text: "+ 100.00"
                                    font_style: "H5"
                                MDLabel:
                                    text: "From: PRISCA KOECH"
                                    font_style: "Body2"
                                MDLabel:
                                    text: "AT: 09:45 AM"
                                    font_style: "Caption"
    
                        # Another Transaction for Today
                        MDCard:
                            md_bg_color: app._blue
                            size_hint: (1, None)
                            height: dp(120)
                            radius: dp(11.5)
                            line_color: app._white
                            padding: dp(10)
                            BoxLayout:
                                orientation: "vertical"
                                MDLabel:
                                    text: "Transaction ID: 54321"
                                    font_style: "Body1"
                                    theme_text_color: "Primary"
                                MDLabel:
                                    text: "Amount: $75.00"
                                    font_style: "Body2"
                                    theme_text_color: "Secondary"
                                MDLabel:
                                    text: "Time: 12:30 PM"
                                    font_style: "Caption"
                                    theme_text_color: "Hint"
    
                        # Example for Yesterday's Date
                        MDLabel:
                            text: "13th January, Monday, 2024"
                            font_style: "H6"
                            halign: "center"
                            size_hint_y: None
                            height: dp(40)
    
                        MDCard:
                            md_bg_color: app._red
                            size_hint: (1, None)
                            height: dp(120)
                            radius: dp(11.5)
                            line_color: app._white
                            padding: dp(10)
                            BoxLayout:
                                orientation: "vertical"
                                MDLabel:
                                    text: "Transaction ID: 67890"
                                    font_style: "Body1"
                                MDLabel:
                                    text: "Amount: $100.00"
                                    font_style: "Body2"
                                MDLabel:
                                    text: "Time: 03:00 PM"
                                    font_style: "Caption"
                                    
                        Widget:  # Spacer to prevent disappearing content
                            size_hint_y: None
                            height: dp(50)


            Tab:
                title: "M-PESA"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            id: mpesa_transactions
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "PayPal"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            id: paypal_transactions
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "Card"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            id: card_transactions
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "Crypto"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            id: crypto_transactions
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height


# ---------------------------------------------- WALLET SCREEN --------------------------------------------
<WalletScreen>:
    name: "wallet_screen"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .95}    
        radius: dp(11.5)

        TopLeftBackButton:
            text_color: app._white
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("home_screen", "right", "pop")

        MDLabel:
            padding: (23, 0)
            text: "Wallet"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: app._white
            pos_hint: {"center_y": .5}
            halign: "center"

        MDIconButton:
            _no_ripple_effect: True
            icon: "assets/images/csettings_icon.png"
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("settings_screen", "left")
        
    MDLabel:
        text: "Total Assets"
        font_style: "Subtitle2"
        pos_hint: {"center_y": .75}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._gray

    MDLabel:
        text: "[size=15sp]Ksh.[/size] [size=26sp]1,378.96[/size]"
        markup: True
        font_style: "H6"
        pos_hint: {"center_y": .7}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._white

    MDCard:
        md_bg_color: app._green
        background: "assets/images/bg5.jpg"
        size_hint: 1, .58
        pos_hint: {"center_x": .5, "center_y": .29}
        radius: dp(46), dp(46), dp(0), dp(0)
        padding: dp(23)

        MDCard:
            md_bg_color: app._invisible
            size_hint: (1, .123)
            pos_hint: {"center_x": .5, "top": 1}
            padding: dp(0)
            radius: dp(0)

            MDLabel:
                text: "My wallets"
                halign: "left"
                pos_hint: {"center_y": .9}
                theme_text_color: "Custom"
                text_color: app._white
                font_style: "Body1"
                bold: True      

    MDCard:
        md_bg_color: app._invisible
        size_hint: (.95, .4)
        pos_hint: {"center_x": .5, "top": .523}    
        radius: dp(0)
        padding: dp(0)

        MDScrollView:
            MDList:
                TwoLineListItem:
                    divider: None
                    _no_ripple_effect: True

                    MDCard:
                        md_bg_color: app._invisible
                        size_hint: (1, 1)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        padding: dp(6)

                        MDCard:
                            md_bg_color: (.6, .6, 1, .05)
                            padding: dp(0), dp(0), dp(10), dp(0)
                            radius: dp(11.5)
                            padding: dp(6)

                            MDBoxLayout:
                                size_hint: (None, None)
                                width: "50dp"
                                height: "50dp"
                                pos_hint: {"center_y": .5}

                                Image:
                                    source: "assets/images/mpesa_icon.png"
                                    size_hint: (1,.9)
                                    pos_hint: {"center_y": .5}

                            MDBoxLayout:
                                orientation: "vertical"
                                padding: dp(11.5)

                                MDLabel:
                                    text: "M-PESA\\n[color=a6a6a6][b][size=11sp]0795923160[/size][/b]"
                                    markup: True
                                    halign: "left"
                                    font_style: "Subtitle1"
                                    theme_text_color: "Custom"
                                    text_color: app._white

                            MDBoxLayout:
                                MDLabel:
                                    text: "[size=13sp]Ksh. 128.57\\n[color=a6a6a6]$ 1.00[/size]"
                                    markup: True
                                    pos_hint: {"center_x": .5, "center_y": .5}
                                    halign: "right"
                                    theme_text_color: "Custom"
                                    text_color: app._white

                TwoLineListItem:
                    divider: None
                    _no_ripple_effect: True

                    MDCard:
                        md_bg_color: app._invisible
                        size_hint: (1, 1)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        padding: dp(6)

                        MDCard:
                            md_bg_color: (.6, .6, 1, .05)
                            padding: dp(0), dp(0), dp(10), dp(0)
                            radius: dp(11.5)
                            padding: dp(6)

                            MDBoxLayout:
                                size_hint: (None, None)
                                width: "50dp"
                                height: "50dp"
                                pos_hint: {"center_y": .5}

                                Image:
                                    source: "assets/images/paypal_icon.png"
                                    size_hint: (1,.9)
                                    pos_hint: {"center_y": .5}

                            MDBoxLayout:
                                orientation: "vertical"
                                padding: dp(11.5)

                                MDLabel:
                                    text: "PayPal\\n[color=a6a6a6][b][size=11sp]dav***@gmail.com[/size][/b]"
                                    markup: True
                                    halign: "left"
                                    font_style: "Subtitle1"
                                    theme_text_color: "Custom"
                                    text_color: app._white

                            MDBoxLayout:
                                MDLabel:
                                    text: "[size=13sp]Ksh. 128.57\\n[color=a6a6a6]$ 1.00[/size]"
                                    markup: True
                                    pos_hint: {"center_x": .5, "center_y": .5}
                                    halign: "right"
                                    theme_text_color: "Custom"
                                    text_color: app._white

    # add wallet btn
    MDCard:
        md_bg_color: app._white
        size_hint: (.9, .07)
        pos_hint: {"center_x": .5, "center_y": .08}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: True

        MDRectangleFlatIconButton:
            icon: "plus"
            icon_text_color: "Custom"
            icon_color: app._dark
            text: "  Add Wallet"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._dark
            font_size: "36px"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.change_screen_wnt("wallet_setup_screen")


# ---------------------------------------------- INSIGHTS SCREEN --------------------------------------------
# -------------------------------------------- TEXT BASED INSIGHTS ------------------------------------------
<InsightScreen1>:
    name: "insight_screen1"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .97}    
        radius: dp(11.5)

        TopLeftBackButton:
            text_color: app._white
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("home_screen", "right", "pop")

        MDLabel:
            padding: (23, 0)
            text: "Insights"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: app._white
            pos_hint: {"center_y": .5}
            halign: "center"

        MDIconButton:
            _no_ripple_effect: True
            icon: "assets/images/csettings_icon.png"
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("settings_screen", "left")

    MDCard:
        md_bg_color: app._gray
        size_hint: (.9, .06)
        pos_hint: {"center_x": .5, "top": .87}    
        radius: dp(11.5)

        MDBoxLayout:
            orientation: "horizontal"

            MDCard:
                md_bg_color: app._blue
                size_hint: (1, 1)
                pos_hint: {"center_y": .5}    
                radius: dp(11.5)

                MDLabel:
                    padding: 8
                    text: "Text-based Insights"
                    font_style: "Body1"
                    theme_text_color: "Custom"
                    text_color: app._white
                    pos_hint: {"center_y": .5}
                    halign: "center"

            MDCard:
                md_bg_color: app._gray
                size_hint: (1, 1)
                pos_hint: {"center_y": .5}    
                radius: dp(11.5)
                on_release: app.change_screen_wnt("insight_screen2")

                MDLabel:
                    padding: 8
                    text: "Visual Insights"
                    font_style: "Body1"
                    theme_text_color: "Custom"
                    text_color: app._dark
                    pos_hint: {"center_y": .5}
                    halign: "center"

    MDCard:
        md_bg_color: app._invisible
        size_hint: (.9, .65)
        pos_hint: {"center_x": .5, "top": .8}    
        radius: dp(11.5)

        CustomTabs:
            Tab:
                title: "Today's Insight"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

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

                        MDBoxLayout:
                            id: general_insight
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

    # insight generator btn
    MDCard:
        id: btn_bg
        md_bg_color: app._white
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .1}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)

        MDRectangleFlatIconButton:
            id: generate_button
            disabled: False
            text: "Generate Insight"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._dark
            font_size: "36px"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.start_text_animation()

    MDLabel:
        text: "Powered by ChatGPT-4o mini"
        font_style: "Subtitle2"
        pos_hint: {"center_y": .036}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._gray

# ----------------------------------------------- VISUAL INSIGHTS ------------------------------------------
<InsightScreen2>:
    name: "insight_screen2"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .97}    
        radius: dp(11.5)

        TopLeftBackButton:
            text_color: app._white
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("home_screen", "right", "pop")

        MDLabel:
            padding: (23, 0)
            text: "Insights"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: app._white
            pos_hint: {"center_y": .5}
            halign: "center"

        MDIconButton:
            _no_ripple_effect: True
            icon: "assets/images/csettings_icon.png"
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("settings_screen", "left")

    MDCard:
        md_bg_color: app._gray
        size_hint: (.9, .06)
        pos_hint: {"center_x": .5, "top": .87}    
        radius: dp(11.5)

        MDBoxLayout:
            orientation: "horizontal"

            MDCard:
                md_bg_color: app._gray
                size_hint: (1, 1)
                pos_hint: {"center_y": .5}    
                radius: dp(11.5)
                on_release: app.change_screen_wnt("insight_screen1")

                MDLabel:
                    padding: 8
                    text: "Text-based Insights"
                    font_style: "Body1"
                    theme_text_color: "Custom"
                    text_color: app._dark
                    pos_hint: {"center_y": .5}
                    halign: "center"

            MDCard:
                md_bg_color: app._blue
                size_hint: (1, 1)
                pos_hint: {"center_y": .5}    
                radius: dp(11.5)

                MDLabel:
                    padding: 8
                    text: "Visual Insights"
                    font_style: "Body1"
                    theme_text_color: "Custom"
                    text_color: app._white
                    pos_hint: {"center_y": .5}
                    halign: "center"
                    
    MDCard:
        md_bg_color: app._invisible
        size_hint: (.9, .79)
        pos_hint: {"center_x": .5, "top": .8}    
        radius: dp(11.5)

        CustomTabs:
            Tab:
                title: "Today's Insight"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True
                        effect_cls: "ScrollEffect" 
                        bar_color: app._invisible

                        MDBoxLayout:
                            # id: daily_insight
                            orientation: "vertical"
                            padding: dp(0)
                            spacing: dp(11.5)
                            adaptive_height: True

                            MDCard:
                                md_bg_color: app._red
                                size_hint: (1, None)
                                height: dp(230)
                                pos_hint: {"center_x": .5}    
                                radius: dp(11.5)

                            MDCard:
                                md_bg_color: app._red
                                size_hint: (1, None)
                                height: dp(230)
                                pos_hint: {"center_x": .5}    
                                radius: dp(11.5)
                                line_color: app._white

                            MDCard:
                                md_bg_color: app._green
                                size_hint: (1, None)
                                height: dp(230)
                                pos_hint: {"center_x": .5}    
                                radius: dp(11.5)

                            MDCard:
                                md_bg_color: app._green
                                size_hint: (1, None)
                                height: dp(230)
                                pos_hint: {"center_x": .5}    
                                radius: dp(11.5)

                            
            Tab:
                title: "Weekly Insight"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            # id: weekly_insight
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "Monthly Insight"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            # id: monthly_insight
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "Yearly Insight"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            # id: yearly_insight
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

            Tab:
                title: "General Insight"

                InsightCard:
                    MDScrollView:
                        do_scroll_x: False
                        do_scroll_y: True

                        MDBoxLayout:
                            # id: general_insight
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height

# ----------------------------------------------- SETTINGS SCREEN -----------------------------------------      
<SettingsScreen>:
    name: "settings_screen"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .95}    
        radius: dp(11.5)

        TopLeftBackButton:
            text_color: app._white
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("home_screen", "right", "pop")

        MDLabel:
            padding: (23, 0)
            text: "Settings"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: app._white
            pos_hint: {"center_y": .5}
            halign: "center"

        MDIconButton:
            icon: "logout"
            theme_text_color: "Custom"
            text_color: (1, .6, .6, 1)
            pos_hint: {"center_y": .5}
            halign: "right"
            _no_ripple_effect: True
            padding: 17.5

    MDCard:
        background: app.profile_photo
        md_bg_color: app._white
        line_color: app._dark
        size_hint: (None, None)
        width: "136dp"
        height: "136dp"
        radius: self.height / 2
        pos_hint: {"center_x": .5, "center_y": .75}

    MDLabel:
        text: app.full_name
        halign: "center"
        pos_hint: {"center_y": .63,}
        theme_text_color: "Custom"
        text_color: app._white
        font_style: "H5"
        bold: True

    MDLabel:
        text: "davidxanderbilt@gmail.com"
        halign: "center"
        pos_hint: {"center_y": .59,}
        theme_text_color: "Custom"
        text_color: app._gray
        font_style: "Subtitle1"
        bold: True

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .52}    
        radius: dp(11.5)
        padding: dp(6)
        on_release: app.change_screen_wt("personal_info_screen", "left")

        MDBoxLayout:
            size_hint: (None, None)
            size: ("43sp", "43sp")
            pos_hint: {"center_y": .5}

            Image:
                source: "assets/images/personal_info_icon.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.43, .6)

        MDBoxLayout:
            MDLabel:
                text: "  Personal Information"
                font_size: "16sp"
                theme_text_color: "Custom"
                text_color: app._white
                pos_hint: {"center_y": .5}

        MDBoxLayout:
            size_hint: (None, None)
            size: ("23sp", "23sp")
            pos_hint: {"center_y": .5}

            MDIcon:
                icon: "chevron-right"
                theme_text_color: "Custom"
                text_color: app._white
                pos_hint: {"center_y": .5}

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .41}    
        radius: dp(11.5)
        padding: dp(6)
        on_release: app.change_screen_wt("reports_screen", "left")

        MDBoxLayout:
            size_hint: (None, None)
            size: ("43sp", "43sp")
            pos_hint: {"center_y": .5}

            Image:
                source:  "assets/images/reports_icon.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.53, .63)

        MDBoxLayout:
            MDLabel:
                text: "  Financial Reports"
                font_size: "16sp"
                theme_text_color: "Custom"
                text_color: app._white
                pos_hint: {"center_y": .5}

        MDBoxLayout:
            size_hint: (None, None)
            size: ("23sp", "23sp")
            pos_hint: {"center_y": .5}

            MDIcon:
                icon: "chevron-right"
                theme_text_color: "Custom"
                text_color: app._white
                pos_hint: {"center_y": .5}

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .3}    
        radius: dp(11.5)
        padding: dp(6)
        on_release: app.change_screen_wt("privacy_policy_screen", "left")
        
        MDBoxLayout:
            size_hint: (None, None)
            size: ("43sp", "43sp")
            pos_hint: {"center_y": .5}

            Image:
                source:  "assets/images/privacy_policy_icon.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.66, .66)

        MDBoxLayout:
            MDLabel:
                text: "  Privacy Policy"
                font_size: "16sp"
                theme_text_color: "Custom"
                text_color: app._white
                pos_hint: {"center_y": .5}

        MDBoxLayout:
            size_hint: (None, None)
            size: ("23sp", "23sp")
            pos_hint: {"center_y": .5}

            MDIcon:
                icon: "chevron-right"
                theme_text_color: "Custom"
                text_color: app._white
                pos_hint: {"center_y": .5}

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .19}    
        radius: dp(11.5)
        padding: dp(6)
        on_release: app.change_screen_wt("terms_of_use_screen", "left")
        
        MDBoxLayout:
            size_hint: (None, None)
            size: ("43sp", "43sp")
            pos_hint: {"center_y": .5}

            Image:
                source:  "assets/images/terms_of_use_icon.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: (.66, .66)

        MDBoxLayout:
            MDLabel:
                text: "  Terms of Use"
                font_size: "16sp"
                theme_text_color: "Custom"
                text_color: app._white
                pos_hint: {"center_y": .5}

        MDBoxLayout:
            size_hint: (None, None)
            size: ("23sp", "23sp")
            pos_hint: {"center_y": .5}

            MDIcon:
                icon: "chevron-right"
                theme_text_color: "Custom"
                text_color: app._white
                pos_hint: {"center_y": .5}

    MDLabel:
        text: "Personal Finance Tracker" +\"\\nv1.0"
        halign: "center"
        pos_hint: {"center_y": .04,}
        theme_text_color: "Custom"
        text_color: app._gray
        font_style: "Subtitle2"

# -------------------------------------------- PERSONAL INFO SCREEN ---------------------------------------      
<PersonalInfoScreen>:
    name: "personal_info_screen"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .95}    
        radius: dp(11.5)

        TopLeftBackButton:
            text_color: app._white
            pos_hint: {"center_y": .5}
            on_release: app.change_screen_wt("settings_screen", "right", "pop")

        MDLabel:
            padding: (11.5, 0)
            text: "Personal Information"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: app._white
            pos_hint: {"center_y": .5}
            halign: "left"

    MDCard:
        background: app.profile_photo
        md_bg_color: app._white
        line_color: app._dark
        size_hint: (None, None)
        width: "160dp"
        height: "160dp"
        radius: self.height / 2
        pos_hint: {"center_x": .5, "center_y": .63}

        MDRelativeLayout:
            MDCard:
                md_bg_color: app._blue
                size_hint: (None, None)
                width: "55dp"
                height: "55dp"
                radius: self.height / 2
                pos_hint: {"right": 1, "top": .3}
                on_release: app.show_card(app.card_to_show_or_hide("change_avatar"))

                MDIcon:
                    padding: dp(15)
                    icon: "pencil"
                    theme_text_color: "Custom"
                    text_color: app._white
                    pos_hint: { "center_y": .5}

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .1)
        pos_hint: {"center_x": .5, "top": .45}    
        radius: dp(11.5)
        padding: dp(23), dp(11.5)

        MDBoxLayout:
            orientation: "vertical"

            MDLabel:
                text: "Full name"
                font_style: "Subtitle2"
                theme_text_color: "Custom"
                text_color: app._gray
                pos_hint: {"center_y": .5}
                halign: "left"

            MDLabel:
                text: app.full_name
                font_style: "Body1"
                theme_text_color: "Custom"
                text_color: app._white
                pos_hint: {"center_y": .5}
                halign: "left"

    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.9, .1)
        pos_hint: {"center_x": .5, "top": .32}    
        radius: dp(11.5)
        padding: dp(23), dp(11.5)

        MDBoxLayout:
            orientation: "vertical"

            MDLabel:
                text: "Email address"
                font_style: "Subtitle2"
                theme_text_color: "Custom"
                text_color: app._gray
                pos_hint: {"center_y": .5}
                halign: "left"

            MDLabel:
                text: "davidxanderbilt@gmail.com"
                font_style: "Body1"
                theme_text_color: "Custom"
                text_color: app._white
                pos_hint: {"center_y": .5}
                halign: "left"

    HiddenCard:
        id: change_avatar
        size_hint_y: .2

        MDRelativeLayout:
            orientation: "vertical"

            MDCard:
                md_bg_color: app._invisible
                size_hint: (1, .1)
                pos_hint: {"center_x": .5, "top": 1}

                CLoseCardButton:
                    md_bg_color: app._invisible
                    size_hint: None, None
                    on_release: app.hide_card(app.card_to_show_or_hide("change_avatar"))

                MDLabel:
                    text: "Change Avatar    "
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: app._white
                    pos_hint: {"center_y": .5}
                    halign: "center"

            MDCard:
                md_bg_color: (.6, .6, 1, .1)
                size_hint: (1, .65)
                pos_hint: {"center_x": .5, "center_y": .2}
                radius: dp(11.5)
                padding: dp(11.5)
                on_release: app.change_profile_pic()

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("36sp", "36sp")
                    pos_hint: {"center_y": .5}

                    MDIcon:
                        icon: "camera-burst"
                        theme_text_color: "Custom"
                        text_color: app._white
                        pos_hint: {"center_y": .5}

                MDBoxLayout:
                    MDLabel:
                        text: "Choose from library"
                        font_size: "18sp"
                        theme_text_color: "Custom"
                        text_color: app._white
                        pos_hint: {"center_y": .5}

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("23sp", "23sp")
                    pos_hint: {"center_y": .5}

                    MDIcon:
                        icon: "chevron-right"
                        theme_text_color: "Custom"
                        text_color: app._white
                        pos_hint: {"center_y": .5}


# -------------------------------------------- REPORTS SCREEN ------------------------------------------
<ReportsScreen>:
    name: "reports_screen"
    md_bg_color: app._dark

    TopLeftBackButton:
        theme_text_color: "Custom"
        text_color: app._white
        on_release: app.change_screen_wt("settings_screen", "right", "pop")

    Image:
        source: "assets/images/reports_icon.png"
        size_hint: (.23, .23)
        pos_hint: {"center_x": .5, "center_y": .8}

    MDLabel:
        text: "Download Financial Reports"
        bold: True
        padding: dp(46)
        font_style: "H4"
        pos_hint: {"center_y": .65}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._gray

    # ------------------------- report options --------------------------
    # ----- daily -----
    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.4, .18)
        pos_hint: {"center_x": .275, "center_y": .45}    
        radius: dp(23)
        padding: dp(0), dp(20)
        on_release: app.show_card(app.card_to_show_or_hide("daily_report_card"))

        MDRelativeLayout:
            orientation: "vertical"
            
            Image:
                source: "assets/images/daily.png"
                size_hint: (.6, .6)
                pos_hint: {"center_x": .5, "center_y": .7}

            MDLabel:
                text: "Daily Report"
                font_style: "Body1"
                pos_hint: {"center_y": .15}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._white

    # ----- weekly -----
    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.4, .18)
        pos_hint: {"center_x": .725, "center_y": .45}    
        radius: dp(23)
        padding: dp(0), dp(20)
        on_release: app.show_card(app.card_to_show_or_hide("weekly_report_card"))

        MDRelativeLayout:
            orientation: "vertical"
            
            Image:
                source: "assets/images/weekly.png"
                size_hint: (.6, .6)
                pos_hint: {"center_x": .5, "center_y": .7}

            MDLabel:
                text: "Weekly Report"
                font_style: "Body1"
                pos_hint: {"center_y": .15}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._white

    # ----- monthly ----- 
    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.4, .18)
        pos_hint: {"center_x": .275, "center_y": .24}    
        radius: dp(23)
        padding: dp(0), dp(20)
        on_release: app.show_card(app.card_to_show_or_hide("monthly_report_card"))

        MDRelativeLayout:
            orientation: "vertical"
            
            Image:
                source: "assets/images/monthly.png"
                size_hint: (.6, .6)
                pos_hint: {"center_x": .5, "center_y": .7}

            MDLabel:
                text: "Monthly Report"
                font_style: "Body1"
                pos_hint: {"center_y": .15}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._white

    # ----- yearly -----
    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.4, .18)
        pos_hint: {"center_x": .725, "center_y": .24}    
        radius: dp(23)
        padding: dp(0), dp(20)
        on_release: app.show_card(app.card_to_show_or_hide("yearly_report_card"))
        
        MDRelativeLayout:
            orientation: "vertical"
            
            Image:
                source: "assets/images/yearly.png"
                size_hint: (.6, .6)
                pos_hint: {"center_x": .5, "center_y": .7}
            
            MDLabel:
                text: "Yearly Report"
                font_style: "Body1"
                pos_hint: {"center_y": .15}
                halign: "center"
                theme_text_color: "Custom"
                text_color: app._white
                
    MDCard:
        md_bg_color: (.6, .6, 1, .1)
        size_hint: (.85, .09)
        pos_hint: {"center_x": .5, "center_y": .063}    
        radius: dp(11.5)
        padding: dp(11.5)

        MDBoxLayout:
            MDIcon:
                icon: "information"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app._gray

            MDLabel:
                text: "The reports are available in [color=00afff][size=16sp].csv[/size][/color] format only."
                markup: True
                padding: dp(11.5)
                size_hint_y: None
                pos_hint: {"center_y": .5}
                font_style: "Subtitle2"
                halign: "left"
                theme_text_color: "Custom"
                text_color: app._gray

    HiddenCard:
        id: daily_report_card

        MDRelativeLayout:
            orientation: "vertical"

            MDCard:
                md_bg_color: app._invisible
                size_hint: (1, .163)
                pos_hint: {"center_x": .5, "top": 1}

                CLoseCardButton:
                    on_release: app.hide_card(app.card_to_show_or_hide("daily_report_card"))

                MDLabel:
                    text: "Daily report    "
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: app._white
                    pos_hint: {"center_y": .5}
                    halign: "center"

                MDIcon:
                    icon: "assets/images/daily.png"
                    pos_hint: {"center_y": .53}
                    halign: "right"
                    padding: dp(11.5), dp(8)

            MDCard:
                md_bg_color: (.6, .6, 1, .1)
                size_hint: (1, .3)
                pos_hint: {"center_x": .5, "center_y": .66}    
                radius: dp(11.5)
                padding: dp(23), dp(0), dp(0), dp(11.5)

                MDLabel:
                    text: f"\\n[size=23sp]{app.today},[/size]" +\
                        f"\\n[size=26sp]{app.month} {app.today_date}, {app.year}[/size]"
                    markup: True
                    pos_hint: {"center_y": .5}
                    font_style: "Subtitle2"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: app._white

            MDCard:
                md_bg_color: (.6, .6, 1, .1)
                size_hint: (1, .323)
                pos_hint: {"center_x": .5, "center_y": .318}
                radius: dp(11.5)
                padding: dp(11.5)

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("36sp", "36sp")
                    pos_hint: {"center_y": .5}

                    MDIcon:
                        icon: "information"
                        pos_hint: {"center_y": .5}
                        theme_text_color: "Custom"
                        text_color: app._gray

                MDBoxLayout:
                    MDLabel:
                        text: "Once you hit the 'Download' button, check your 'Documents Folder' after" +\
                            " a couple of seconds...\\n\\n[color=00afff]File name pattern: [i]pft_dr_***.csv[/i]"
                        markup: True
                        size_hint_y: None
                        pos_hint: {"center_y": .5}
                        font_style: "Subtitle2"
                        halign: "left"
                        theme_text_color: "Custom"
                        text_color: app._gray

            # daily report download btn
            MDCard:
                md_bg_color: app._white
                size_hint: (1, .163)
                pos_hint: {"center_x": .5, "center_y": .05}
                radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)

                MDRectangleFlatIconButton:
                    icon: "download"
                    text: "    Download"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app._dark
                    theme_icon_color: "Custom"
                    icon_color: app._dark
                    font_size: "36px"
                    size_hint: (1, 1)
                    line_color: app._invisible
                    _no_ripple_effect: True

    HiddenCard:
        id: weekly_report_card

        MDRelativeLayout:
            orientation: "vertical"

            MDCard:
                md_bg_color: app._invisible
                size_hint: (1, .163)
                pos_hint: {"center_x": .5, "top": 1}

                CLoseCardButton:
                    on_release: app.hide_card(app.card_to_show_or_hide("weekly_report_card"))

                MDLabel:
                    text: "Weekly report    "
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: app._white
                    pos_hint: {"center_y": .5}
                    halign: "center"

                MDIcon:
                    icon: "assets/images/weekly.png"
                    pos_hint: {"center_y": .53}
                    halign: "right"
                    padding: dp(11.5), dp(8)

            MDCard:
                md_bg_color: (.6, .6, 1, .1)
                size_hint: (1, .3)
                pos_hint: {"center_x": .5, "center_y": .66}    
                radius: dp(11.5)
                padding: dp(23), dp(0), dp(0), dp(11.5)

                MDLabel:
                    text: f"\\n[size=23sp]Year {app.week_number_year}: Week {app.current_week_number}[/size]" +\
                        f"\\n[size=19sp]{app.week_number_start_date} - {app.week_number_end_date}[/size]"
                    markup: True
                    pos_hint: {"center_y": .5}
                    font_style: "Subtitle2"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: app._white

            MDCard:
                md_bg_color: (.6, .6, 1, .1)
                size_hint: (1, .323)
                pos_hint: {"center_x": .5, "center_y": .318}
                radius: dp(11.5)
                padding: dp(11.5)

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("36sp", "36sp")
                    pos_hint: {"center_y": .5}

                    MDIcon:
                        icon: "information"
                        pos_hint: {"center_y": .5}
                        theme_text_color: "Custom"
                        text_color: app._gray

                MDBoxLayout:
                    MDLabel:
                        text: "Once you hit the 'Download' button, check your 'Documents Folder' after" +\
                            " a couple of seconds...\\n\\n[color=00afff]File name pattern: [i]pft_wr_***.csv[/i]"
                        markup: True
                        size_hint_y: None
                        pos_hint: {"center_y": .5}
                        font_style: "Subtitle2"
                        halign: "left"
                        theme_text_color: "Custom"
                        text_color: app._gray

            # weekly report download btn
            MDCard:
                md_bg_color: app._white
                size_hint: (1, .163)
                pos_hint: {"center_x": .5, "center_y": .05}
                radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)

                MDRectangleFlatIconButton:
                    icon: "download"
                    text: "    Download"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app._dark
                    theme_icon_color: "Custom"
                    icon_color: app._dark
                    font_size: "36px"
                    size_hint: (1, 1)
                    line_color: app._invisible
                    _no_ripple_effect: True
       
    HiddenCard:
        id: monthly_report_card

        MDRelativeLayout:
            orientation: "vertical"

            MDCard:
                md_bg_color: app._invisible
                size_hint: (1, .163)
                pos_hint: {"center_x": .5, "top": 1}

                CLoseCardButton:
                    on_release: app.hide_card(app.card_to_show_or_hide("monthly_report_card"))

                MDLabel:
                    text: "Monthly report    "
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: app._white
                    pos_hint: {"center_y": .5}
                    halign: "center"

                MDIcon:
                    icon: "assets/images/monthly.png"
                    pos_hint: {"center_y": .53}
                    halign: "right"
                    padding: dp(11.5), dp(8)

            MDCard:
                md_bg_color: (.6, .6, 1, .1)
                size_hint: (1, .3)
                pos_hint: {"center_x": .5, "center_y": .66}    
                radius: dp(11.5)
                padding: dp(23), dp(0), dp(6), dp(11.5)

                MDLabel:
                    text: f"[size=23sp]For the month of\\n{app.previous_month}[/size]"
                    markup: True
                    pos_hint: {"center_y": .5}
                    font_style: "Subtitle2"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: app._white

            MDCard:
                md_bg_color: (.6, .6, 1, .1)
                size_hint: (1, .323)
                pos_hint: {"center_x": .5, "center_y": .318}
                radius: dp(11.5)
                padding: dp(11.5)

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("36sp", "36sp")
                    pos_hint: {"center_y": .5}

                    MDIcon:
                        icon: "information"
                        pos_hint: {"center_y": .5}
                        theme_text_color: "Custom"
                        text_color: app._gray

                MDBoxLayout:
                    MDLabel:
                        text: "Once you hit the 'Download' button, check your 'Documents Folder' after" +\
                            " a couple of seconds...\\n\\n[color=00afff]File name pattern: [i]pft_mr_***.csv[/i]"
                        markup: True
                        size_hint_y: None
                        pos_hint: {"center_y": .5}
                        font_style: "Subtitle2"
                        halign: "left"
                        theme_text_color: "Custom"
                        text_color: app._gray

            # monthly report download btn
            MDCard:
                md_bg_color: app._white
                size_hint: (1, .163)
                pos_hint: {"center_x": .5, "center_y": .05}
                radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)

                MDRectangleFlatIconButton:
                    icon: "download"
                    text: "    Download"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app._dark
                    theme_icon_color: "Custom"
                    icon_color: app._dark
                    font_size: "36px"
                    size_hint: (1, 1)
                    line_color: app._invisible
                    _no_ripple_effect: True

    HiddenCard:
        id: yearly_report_card
        
        MDRelativeLayout:
            orientation: "vertical"

            MDCard:
                md_bg_color: app._invisible
                size_hint: (1, .163)
                pos_hint: {"center_x": .5, "top": 1}

                CLoseCardButton:
                    on_release: app.hide_card(app.card_to_show_or_hide("yearly_report_card"))

                MDLabel:
                    text: "Yearly report    "
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: app._white
                    pos_hint: {"center_y": .5}
                    halign: "center"

                MDIcon:
                    icon: "assets/images/yearly.png"
                    pos_hint: {"center_y": .53}
                    halign: "right"
                    padding: dp(11.5), dp(8)

            MDCard:
                md_bg_color: (.6, .6, 1, .1)
                size_hint: (1, .3)
                pos_hint: {"center_x": .5, "center_y": .66}    
                radius: dp(11.5)
                padding: dp(23), dp(0), dp(0), dp(11.5)

                MDLabel:
                    text: f"\\n[size=26sp]Year {app.year},[/size]" +\
                        f"\\n[size=23sp]1 January - {app.today_date} {app.month}[/size]"
                    markup: True
                    pos_hint: {"center_y": .5}
                    font_style: "Subtitle2"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: app._white

            MDCard:
                md_bg_color: (.6, .6, 1, .1)
                size_hint: (1, .323)
                pos_hint: {"center_x": .5, "center_y": .318}
                radius: dp(11.5)
                padding: dp(11.5)

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("36sp", "36sp")
                    pos_hint: {"center_y": .5}

                    MDIcon:
                        icon: "information"
                        pos_hint: {"center_y": .5}
                        theme_text_color: "Custom"
                        text_color: app._gray

                MDBoxLayout:
                    MDLabel:
                        text: "Once you hit the 'Download' button, check your 'Documents Folder' after" +\
                            " a couple of seconds...\\n\\n[color=00afff]File name pattern: [i]pft_yr_***.csv[/i]"
                        markup: True
                        size_hint_y: None
                        pos_hint: {"center_y": .5}
                        font_style: "Subtitle2"
                        halign: "left"
                        theme_text_color: "Custom"
                        text_color: app._gray

            # yearly report download btn
            MDCard:
                md_bg_color: app._white
                size_hint: (1, .163)
                pos_hint: {"center_x": .5, "center_y": .05}
                radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)

                MDRectangleFlatIconButton:
                    icon: "download"
                    text: "    Download"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app._dark
                    theme_icon_color: "Custom"
                    icon_color: app._dark
                    font_size: "36px"
                    size_hint: (1, 1)
                    line_color: app._invisible
                    _no_ripple_effect: True


# ############################################## SCREEN MANAGER #############################################
MDScreenManager:
    WelcomeScreen:
    PrivacyPolicyScreen:
    TermsOfUseScreen:
    OnboardingScreen:
    FullNameScreen:
    WalletSetupScreen:
    AddMpesaAccScreen:
    CardScreen:
    AddCardScreen:
    PayPalAccountScreen:
    AddPaypalAccScreen:
    CryptoAccountScreen:
    AddCryptoWalletScreen:
    HomeScreen:
    TransactionsScreen:
    WalletScreen:
    InsightScreen1:
    InsightScreen2:
    SettingsScreen:
    PersonalInfoScreen:
    ReportsScreen:


"""


# ######################################## CUSTOM WIDGETS DEFINITION ########################################

class TopLeftBackButton(MDIconButton):
    pass


class PasswordTextField(MDRelativeLayout):
    text, hint_text = StringProperty(), StringProperty()

    def on_kv_post(self, base_widget):
        self.ids.password.bind(
            text=self.setter("text"),
            hint_text=self.setter("hint_text"),
        )


class TextFieldNormal(MDTextField):
    pass


class CustomCardBackground(MDCard):
    pass


class DynamicCard(MDCard):
    pass


class Tab(MDRelativeLayout, MDTabsBase):
    pass


class CustomTabs(MDTabs):
    pass


class InsightCard(MDCard):
    pass


class HiddenCard(MDCard):
    pass


class CLoseCardButton(MDIconButton):
    pass


# ############################################### SCREENS ################################################

class WelcomeScreen(MDScreen):
    pass


class OnboardingScreen(MDScreen):
    pass


class FullNameScreen(MDScreen):
    pass


class PrivacyPolicyScreen(MDScreen):
    pass


class TermsOfUseScreen(MDScreen):
    pass


class WalletSetupScreen(MDScreen):
    pass


class AddMpesaAccScreen(MDScreen):
    pass


class CardScreen(MDScreen):
    pass


class AddCardScreen(MDScreen):
    pass


class PayPalAccountScreen(MDScreen):
    pass


class AddPaypalAccScreen(MDScreen):
    pass


class CryptoAccountScreen(MDScreen):
    pass


class AddCryptoWalletScreen(MDScreen):
    pass


class HomeScreen(MDScreen):
    pass


class TransactionsScreen(MDScreen):
    pass


class WalletScreen(MDScreen):
    pass


class InsightScreen1(MDScreen):
    pass


class InsightScreen2(MDScreen):
    pass


class SettingsScreen(MDScreen):
    pass


class PersonalInfoScreen(MDScreen):
    pass


class ReportsScreen(MDScreen):
    pass


# ######################################## Markdown to KivyMD ###########################################

class MarkdownFormatter:
    def __init__(self):
        self.patterns = {
            r'^\#\s*(.*?)$': '[b]\\1[/b]',  # For handling titles...
            r'\*\*(.*?)\*\*': '[b]\\1[/b]',  # For handling subtitles...
            r'\*(.*?)\*': '[b][i]\\1[/i][/b]',  # For handling italics...
            r'^\-\s*(.*?)$': '    • \\1',  # For handling lists...
        }

    def format_text(self, text):
        """Formats the text by applying KivyMD-style markup replacements."""
        for (pattern, replacement) in self.patterns.items():
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

        return text


# ################################################ APP ################################################

class PersonalFinanceTrackerApp(MDApp):
    def __init__(self):
        super().__init__()
        self.title = "Personal Finance Tracker"
        self.theme_cls.theme_style = "Dark"

        self.from_screen = "welcome_screen"

        # colors
        self._dark, self._light, self._white, self._gray, self._blue, self._green, self._invisible, self._red = (
            "#00001fff", "#c800f0", "#dddddd", "#a6a6a6", "#005eff", "#2fc46c", (1, 1, 1, 0), "#ff2f3f"
        )

        self.full_name = "Prisca Koech"
        self.email_address = "davidxanderbilt@gmail.com"
        self.profile_photo = "assets/images/dp1.jpg"

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


    def set_bars_colors(self):
        set_bars_colors(get_color_from_hex(self._dark), get_color_from_hex(self._dark), "Light")


    def build(self):
        # initialize_google(self.after_login, self.error_listener, self.client_id, self.client_sk)
        self.set_bars_colors()
        return Builder.load_string(UI)

    def change_screen_wt(self, screen_name, direction, mode="push"):
        """change screen with transition"""
        pop_screen_list = [
            "home_screen", "transactions_screen", "wallet_screen", "insight_screen1", "insight_screen2",
            "settings_screen", "personal_info_screen", "reports_screen"
        ]

        if self.root.current in pop_screen_list:
            self.root.transition = CardTransition(direction=direction, mode=mode)

        else: self.root.transition = SlideTransition(direction=direction)
        self.root.current = screen_name

    def change_screen_wnt(self, screen_name):
        """change screen with no transition"""
        self.root.transition = NoTransition()
        self.root.current = screen_name

    def goto_hyperlink(self, ref):
        if ref == "privacy":
            self.change_screen_wt("privacy_policy_screen", "left")

        elif ref == "terms":
            self.change_screen_wt("terms_of_use_screen", "left")

    def enable_submit_btn(self):
        """Enables the submit button if the lengths of first_name, and last_name are greater than 0"""
        current_screen = self.root.get_screen("full_name_input_screen")

        if len(current_screen.ids.first_name.text) > 0 and len(current_screen.ids.last_name.text) > 0:
            current_screen.ids.submit_btn_bg.md_bg_color = self._white
            current_screen.ids.submit_btn_bg.ripple_behavior = True
            current_screen.ids.submit_btn.disabled = False

        else:
            current_screen.ids.submit_btn_bg.md_bg_color = (.6, .6, 1, .1)
            current_screen.ids.submit_btn_bg.ripple_behavior = False
            current_screen.ids.submit_btn.disabled = True

    def get_name(self):
        first_name = self.root.get_screen("full_name_input_screen").ids.first_name.text
        last_name = self.root.get_screen("full_name_input_screen").ids.last_name.text
        full_name = f"{first_name} {last_name}"
        return full_name

    def greeting_text(self):
        if 0 <= self.current_hour <= 11: return "Good Morning,"
        if 12 <= self.current_hour <= 15: return "Good Afternoon,"
        if 16 <= self.current_hour <= 23: return "Good Evening,"

    def change_chart(self):
        self.root.get_screen("home_screen").ids.chart.source = "assets/images/income_expenditure_bar.png" \
            if self.root.get_screen("home_screen").ids.chart.source == "assets/images/income_expenditure_graph.png" \
            else "assets/images/income_expenditure_graph.png"

    @staticmethod
    def change_profile_pic():
        MDFileManager()

    def change_indicator_color(self, current_slide_index):
        # Resetting all indicator colors to gray...
        self.root.get_screen("home_screen").ids.slide1_indicator_color.md_bg_color = "#a6a6a6"
        self.root.get_screen("home_screen").ids.slide2_indicator_color.md_bg_color = "#a6a6a6"

        # Changing indicator colors to blue based on the current slide index
        if current_slide_index == 0:
            self.root.get_screen("home_screen").ids.slide1_indicator_color.md_bg_color = "#005eff"
        if current_slide_index == 1:
            self.root.get_screen("home_screen").ids.slide2_indicator_color.md_bg_color = "#005eff"

    @staticmethod
    def transaction_data():
        all_transactions = {
            "M-PESA": {
                "transaction_1": {
                    "date": "31/12/24 at 3:14 PM", # mm/dd/yy
                    "activity": "sent",
                    "amount": "100.00",
                    "transaction_cost": "0.00",
                    "to_acc": "Prisca Koech 0700245601",
                    "from_acc": "",
                    "balance": "362.63"
                },

                "transaction_2": {
                    "date": "1/1/25 at 4:07 PM",  # mm/dd/yy
                    "activity": "received",
                    "amount": "100.00",
                    "transaction_cost": "",
                    "to_acc": "",
                    "from_acc": "Prisca Koech 0700245601",
                    "balance": "462.63"
                }

            },

            "Card": {},
            "PayPal": {},
            "Crypto": {}
        }

        return all_transactions

    def minimalistic_transactions_view(self):
        data = self.transaction_data()

        for i in range(10):
            list_item = TwoLineListItem(divider=None, _no_ripple_effect=True)

            list_item_container = MDCard(
                md_bg_color=(.6, 1, .6, 0),
                size_hint=(1, 1),
                pos_hint={"center_x": .5, "center_y": .5},
                padding=dp(6)
            )

            list_item_bg = MDCard(
                md_bg_color=(.6, .6, 1, .05),
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
                text=f"M-PESA\n[color=a6a6a6][b][size=14sp]1/1/25 at 4:07 PM[/size][/b]",
                markup=True,
                halign="left",
                font_style="Subtitle1",
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

    def on_start(self):
        # Add the labels to their respective cards
        for tab_id, tab_data in self.tab_insights.items():
            self.root.get_screen("insight_screen1").ids[tab_id].add_widget(tab_data["label"])

        self.minimalistic_transactions_view()

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
            Clock.schedule_once(lambda dt, t_id=tab_id: self.animate_text(t_id), 0.06)

        # Schedule re-enabling the button after every 24hrs
        Clock.schedule_once(lambda dt: self.enable_button(), 24 * 60 * 60)

    def animate_text(self, tab_id, step=0):
        """Animates text chat-gpt style"""
        insight_text = self.tab_insights[tab_id]["text"]
        label = self.tab_insights[tab_id]["label"]

        if step < len(insight_text):
            label.text += insight_text[step]
            Clock.schedule_once(lambda dt: self.animate_text(tab_id, step + 1), 0.06)

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

    def after_login(self, name, email, photo_uri):
        user_credentials = {
            "Full name": name,
            "Email": email,
            "Avatar": photo_uri,
        }

        print(user_credentials)

        self.change_screen_wt("wallet_setup_screen", "left")

    def error_listener(self):
        pass

    # @staticmethod
    # def login():
    #     login_google()
    #
    # def logout(self):
    #     logout_google(self.after_logout)

    def after_logout(self):
        self.change_screen_wnt("onboarding_screen")

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
        
    def open_browser(self):
           pass
           # webbrowser.open("www.google.com")


# #####################################################################################################################

PersonalFinanceTrackerApp().run()
