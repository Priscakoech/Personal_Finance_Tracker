
from jnius import autoclass
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.clipboard import Clipboard
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from UI.reusables import TopLeftBackButton, GridCard, CustomLabel, TextFieldNormal, Spacer, CryptoHelpDialog # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """
<WalletSetupScreen>:
    name: "wallet_setup_screen"
    md_bg_color: app._dark

    # Custom Top App Bar
    MDCard:
        size_hint: (1, None)
        height: dp(59)
        radius: dp(0)
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

    Image:
        source: "assets/images/link_icon.png"
        size_hint: (None, None)
        width: "100dp"
        height: "100dp"
        pos_hint: {"center_x": .46, "center_y": .78}

    Image:
        source: "assets/images/wallet_icon.png"
        size_hint: (None, None)
        width: "28dp"
        height: "28dp"
        pos_hint: {"center_x": .54, "center_y": .745}

    MDLabel:
        text: "Link a Wallet"
        font_size: "36dp"
        bold: True
        pos_hint: {"center_y": .65}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._white

    # ------------------------- account options --------------------------
    MDBoxLayout:
        size_hint: (.95, .6)
        pos_hint: {"center_x": .5, "bottom": 0}
        padding: dp(6), dp(32), dp(6), dp(17.5)
        spacing: dp(11.5)
        orientation: "vertical"

        MDBoxLayout:
            padding: dp(6)
            spacing: dp(23)
            size_hint: (1, None)
            height: dp(156)

            GridCard:
                size_hint: (1, 1)
                icon_path: "assets/images/mpesa_icon.png"
                grid_card_txt: "M-PESA"
                on_release: app.show_card(app.card_to_show_or_hide("add_mpesa_acc_card"))

            GridCard:
                size_hint: (1, 1)
                icon_path: "assets/images/crypto_icon.png"
                grid_card_txt: "Crypto"
                on_release: app.show_card(app.card_to_show_or_hide("add_crypto_wallet_card"))

        MDBoxLayout:
            padding: dp(6)
            spacing: dp(23)
            size_hint: (1, None)
            height: dp(156)

            GridCard:
                size_hint: (1, 1)
                md_bg_color: app._tinted
                icon_path: "assets/images/paypal_icon.png"
                grid_card_txt: "PayPal"
                on_release: app.show_card(app.card_to_show_or_hide("add_paypal_acc_card"))

            GridCard:
                size_hint: (1, 1)
                md_bg_color: app._tinted
                icon_path: "assets/images/card_icon1.png"
                grid_card_txt: "Card"
                on_release: app.show_card(app.card_to_show_or_hide("coming_soon_info_card"))

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(56)

    HiddenCard:
        id: add_mpesa_acc_card
        size_hint_y: 1

        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(23)

            MDBoxLayout:
                orientation: "horizontal"
                size_hint: (1, None)
                height: dp(32)
                pos_hint: {"top": 1}

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("33dp", "33dp")
                    radius: self.height / 2
                    md_bg_color: app._tinted
                    line_color: app._blue

                    CloseCardButton:
                        size_hint: (1, 1)
                        on_release: app.hide_card(app.card_to_show_or_hide("add_mpesa_acc_card"))

                MDBoxLayout:
                    size_hint: (1, 1)

                    CustomLabel:
                        text: "[b]Link Your M-PESA Account[/b]"
                        font_size: "18dp"
                        halign: "center"

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("36dp", "33dp")

                    Image:
                        source: "assets/images/mpesa_icon.png"
                        pos_hint: {"center_y": .5}

            MDFloatLayout:
                MDBoxLayout:
                    id: acc_exists
                    orientation: "vertical"
                    opacity: 0
                    size_hint: (1, 1)
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)
                    padding: dp(0), dp(88), dp(0), dp(0)

                    MDBoxLayout:
                        md_bg_color: app._tinted
                        size_hint: (1, None)
                        height: "106dp"
                        pos_hint: {"center_x": .5, "center_y": .73}    
                        radius: dp(11.5), dp(11.5), dp(0), dp(0)
                        padding: dp(11.5)

                        MDBoxLayout:
                            MDIcon:
                                icon: "information"
                                pos_hint: {"center_y": .5}
                                theme_text_color: "Custom"
                                text_color: app._white

                            MDLabel:
                                text: "MPESA account already exists\\nYou can only link one account..."
                                padding: dp(11.5)
                                pos_hint: {"center_y": .5}
                                font_size: "15dp"
                                bold: True
                                markup: True
                                halign: "left"
                                theme_text_color: "Custom"
                                text_color: app._white

                    MDCard:
                        md_bg_color: app._light
                        background: "assets/images/bg5.jpg"
                        radius: dp(0), dp(0), dp(11.5), dp(11.5)
                        size_hint: (1, None)
                        height: dp(46)

                        MDRectangleFlatButton:
                            _no_ripple_effect: True
                            line_color: app._invisible
                            size_hint: (1, 1)
                            text: "GOT IT"
                            theme_text_color: "Custom"
                            text_color: "#ffffff"
                            line_color: app._invisible
                            on_release: 
                                if acc_exists.opacity == 1: app.hide_card(app.card_to_show_or_hide("add_mpesa_acc_card"))

                    MDBoxLayout:

                MDBoxLayout:
                    id: acc_exists_not
                    orientation: "vertical"
                    opacity: 1
                    size_hint: (1, 1)
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(26)

                    MDBoxLayout:
                        md_bg_color: app._tinted
                        size_hint: (1, None)
                        height: "123dp"
                        pos_hint: {"center_x": .5, "center_y": .73}    
                        radius: dp(11.5)
                        padding: dp(11.5)

                        MDBoxLayout:
                            size_hint: (None, 1)
                            width: dp(23)

                            MDIcon:
                                icon: "information"
                                pos_hint: {"top": .98}
                                theme_text_color: "Custom"
                                text_color: app._white
    
                        MDBoxLayout:
                            orientation: "vertical"
                            size_hint: (1, 1)
                            spacing: dp(3)

                            MDLabel:
                                text: "This action requires you to grant the app permission to access your messages. " +\
                                    "Make sure that the phone number you are providing, has it's corresponding" +\
                                    " SIM Card mounted on this device."
                                padding: dp(11.5)
                                pos_hint: {"center_y": .5}
                                font_size: "15dp"
                                bold: True
                                halign: "left"
                                theme_text_color: "Custom"
                                text_color: app._white

                    MDBoxLayout:
                        size_hint: (1, None)
                        height: dp(40)

                        TextFieldNormal:
                            id: mpesa_phone_number
                            hint_text: "M-PESA Number"
                            helper_text: "Format: 0712xxx123 or 0111XXX123"
                            input_type: "number"
                            multiline: False
                            pos_hint: {"center_x": .5, "center_y": .5}

                    Spacer:

                    MDBoxLayout:
                        size_hint: (1, None)
                        height: dp(53)

                        MDCard:
                            md_bg_color: app._green
                            size_hint: (1, 1)
                            pos_hint: {"center_x": .5, "center_y": .5}
                            radius: dp(11.5)

                            MDRectangleFlatIconButton:
                                _no_ripple_effect: True
                                text: "Link"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app._dark
                                font_size: "20dp"
                                size_hint: (1, 1)
                                line_color: app._invisible
                                on_release: root.fetch_mpesa_messages()

                    MDBoxLayout:

    HiddenCard:
        id: add_crypto_wallet_card
        size_hint_y: 1

        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(23)

            MDBoxLayout:
                orientation: "horizontal"
                size_hint: (1, None)
                height: dp(32)
                pos_hint: {"top": 1}

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("33dp", "33dp")
                    radius: self.height / 2
                    md_bg_color: app._tinted
                    line_color: app._blue

                    CloseCardButton:
                        size_hint: (1, 1)
                        on_release: app.hide_card(app.card_to_show_or_hide("add_crypto_wallet_card"))

                MDBoxLayout:
                    size_hint: (1, 1)

                    CustomLabel:
                        text: "[b]Link Your Crypto Wallet[/b]"
                        font_size: "18dp"
                        halign: "center"

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("36dp", "33dp")

                    Image:
                        source: "assets/images/crypto_icon.png"
                        pos_hint: {"center_y": .5}

            MDBoxLayout:
                orientation: "horizontal"
                md_bg_color: app._tinted
                size_hint: (1, None)
                height: "90dp"
                pos_hint: {"center_x": .5, "center_y": .73}    
                radius: dp(11.5)
                padding: dp(11.5)

                MDBoxLayout:
                    size_hint: (None, 1)
                    width: dp(23)

                    MDIcon:
                        icon: "information"
                        pos_hint: {"top": 1}
                        theme_text_color: "Custom"
                        text_color: app._white
    
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint: (1, 1)
                    spacing: dp(3)

                    MDBoxLayout:
                        orientation: "vertical"
                        size_hint: (1, 1)

                        MDLabel:
                            text: "Supported wallets are:-"
                            padding: dp(12.5), dp(0), dp(0), dp(8)
                            pos_hint: {"center_y": .5}
                            font_size: "15dp"
                            bold: True
                            halign: "left"
                            theme_text_color: "Custom"
                            text_color: app._white

                    MDBoxLayout:
                        orientation: "horizontal"
                        size_hint: (1, 1)
                        spacing: dp(8)
                        padding: dp(12.5), dp(0), dp(0), dp(0)

                        MDBoxLayout:
                            size_hint: (None, None)
                            size: ("33dp", "33dp")
                            radius: self.height / 2

                            Image:
                                source: "assets/images/binance_icon.jpg"
                                size_hint: (1, 1)
                                pos_hint: {"center_x": .5, "center_y": .5}

                        MDBoxLayout:
                            size_hint: (None, None)
                            size: ("33dp", "33dp")
                            radius: self.height / 2

                            Image:
                                source: "assets/images/bybit_icon.png"
                                size_hint: (1, 1)
                                pos_hint: {"center_x": .5, "center_y": .5}

                        MDBoxLayout:
                            size_hint: (None, None)
                            size: ("33dp", "33dp")
                            radius: self.height / 2

                            Image:
                                source: "assets/images/metamask_icon.webp"
                                size_hint: (1, 1)
                                pos_hint: {"center_x": .5, "center_y": .5}


                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("36dp", "36dp")
                    radius: self.height / 2
                    line_color: app._blue
                    md_bg_color: app._tinted
                    pos_hint: {"center_y": .5}

                    MDCard:
                        md_bg_color: app._invisible
                        size_hint: (1, 1)
                        radius: self.height / 2
                        ripple_behavior: True
                        padding: dp(6)
                        on_release: app.root.get_screen('wallet_setup_screen').open_crypto_help_dialog()

                        MDIcon:
                            icon: "help-circle"
                            pos_hint: {"center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app._white

            MDBoxLayout:
                size_hint: (1, None)
                height: dp(52)
                spacing: dp(8)

                TextFieldNormal:
                    id: wallet_name
                    size_hint_x: 1
                    hint_text: "Wallet"
                    readonly: True
                    on_touch_down:
                        if self.collide_point(*args[1].pos): app.root.get_screen('wallet_setup_screen').show_wallet_menu(self)

                TextFieldNormal:
                    id: blockchain_network
                    size_hint_x: 1
                    hint_text: "Blockchain Network"
                    readonly: True
                    on_touch_down:
                        if self.collide_point(*args[1].pos): app.root.get_screen('wallet_setup_screen').show_network_menu(self)

            MDBoxLayout:
                size_hint: (1, None)
                height: dp(52)
                orientation: "horizontal"

                TextFieldNormal:
                    id: api_key
                    disabled: True
                    size_hint_x: 1
                    hint_text: "Wallet API Key"
                    multiline: False
                    radius: [11.5, 0, 0, 11.5]

                MDBoxLayout:
                    md_bg_color: app._blue if api_key_paste_btn.disabled != True else app._gray
                    size_hint: (None, 1)
                    width: dp(100)
                    radius: dp(0), dp(11.5), dp(11.5), dp(0)

                    MDFlatButton:
                        id: api_key_paste_btn
                        disabled: True
                        size_hint: (1, 1)
                        pos_hint: {"center_y": .5}
                        radius: dp(0)
                        text: "Paste"
                        theme_text_color: "Custom"
                        text_color: "#ffffff"
                        font_size: "18dp"
                        on_release: app.root.get_screen('wallet_setup_screen').paste_text(api_key)

            MDBoxLayout:
                size_hint: (1, None)
                height: dp(52)
                orientation: "horizontal"

                TextFieldNormal:
                    id: api_secret
                    disabled: True
                    size_hint_x: 1
                    hint_text: "Wallet API Secret"
                    multiline: False
                    radius: [11.5, 0, 0, 11.5]

                MDBoxLayout:
                    md_bg_color: app._blue if api_key_paste_btn.disabled != True else app._gray
                    size_hint: (None, 1)
                    width: dp(100)
                    radius: dp(0), dp(11.5), dp(11.5), dp(0)

                    MDFlatButton:
                        id: api_secret_paste_btn
                        disabled: True
                        size_hint: (1, 1)
                        pos_hint: {"center_y": .5}
                        radius: dp(0)
                        text: "Paste"
                        theme_text_color: "Custom"
                        text_color: "#ffffff"
                        font_size: "18dp"
                        on_release: app.root.get_screen('wallet_setup_screen').paste_text(api_secret)

            MDBoxLayout:
                size_hint: (1, None)
                height: dp(52)
                orientation: "horizontal"

                TextFieldNormal:
                    id: wallet_address
                    disabled: True
                    size_hint: (1, None)
                    hint_text: "Wallet Address"
                    multiline: False
                    radius: [11.5, 0, 0, 11.5]

                MDBoxLayout:
                    md_bg_color: app._blue if wallet_address_paste_btn.disabled != True else app._gray
                    size_hint: (None, 1)
                    width: dp(100)
                    radius: dp(0), dp(11.5), dp(11.5), dp(0)

                    MDFlatButton:
                        id: wallet_address_paste_btn
                        disabled: True
                        size_hint: (1, 1)
                        pos_hint: {"center_y": .5}
                        radius: dp(0)
                        text: "Paste"
                        theme_text_color: "Custom"
                        text_color: "#ffffff"
                        font_size: "18dp"
                        on_release: app.root.get_screen('wallet_setup_screen').paste_text(wallet_address)

            MDBoxLayout:
                size_hint: (1, None)
                height: dp(50)

                MDRectangleFlatButton:
                    _no_ripple_effect: True
                    id: submit_button
                    md_bg_color: app._blue
                    line_color: app._invisible
                    size_hint: (1, 1)
                    text: "Link Wallet"
                    theme_text_color: "Custom"
                    text_color: "#ffffff"
                    font_size: "20dp"
                    disabled: True
                    on_release:
                        app.root.get_screen('wallet_setup_screen').submit_wallet()
                        app.hide_card(app.card_to_show_or_hide("add_crypto_wallet_card"))

            MDBoxLayout:

    HiddenCard:
        id: add_paypal_acc_card
        size_hint_y: 1

        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(23)

            MDBoxLayout:
                orientation: "horizontal"
                size_hint: (1, None)
                height: dp(32)
                pos_hint: {"top": 1}

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("33dp", "33dp")
                    radius: self.height / 2
                    md_bg_color: app._tinted
                    line_color: app._blue

                    CloseCardButton:
                        size_hint: (1, 1)
                        on_release: app.hide_card(app.card_to_show_or_hide("add_paypal_acc_card"))

                MDBoxLayout:
                    size_hint: (1, 1)

                    CustomLabel:
                        text: "[b]Link Your PayPal Account[/b]"
                        font_size: "18dp"
                        halign: "center"

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("36dp", "33dp")

                    Image:
                        source: "assets/images/paypal_icon.png"
                        pos_hint: {"center_y": .5}

            MDBoxLayout:
                Image:
                    size_hint: (.7, .7)
                    source: "assets/images/coming_soon_banner.png"
                    pos_hint: {"center_y": .5}

            MDBoxLayout:
                MDLabel:
                    padding: dp(6)
                    text: "This feature is not yet available, but it's on the way. Stay tuned for updates!"
                    font_size: "20dp"
                    bold: True
                    pos_hint: {"center_y": 1}
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app._white

    HiddenCard:
        id: coming_soon_info_card
        size_hint_y: 1

        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(23)

            MDBoxLayout:
                orientation: "horizontal"
                size_hint: (1, None)
                height: dp(32)
                pos_hint: {"top": 1}

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("33dp", "33dp")
                    radius: self.height / 2
                    md_bg_color: app._tinted
                    line_color: app._blue

                    CloseCardButton:
                        size_hint: (1, 1)
                        on_release: app.hide_card(app.card_to_show_or_hide("coming_soon_info_card"))

                MDBoxLayout:
                    size_hint: (1, 1)

                    CustomLabel:
                        text: "[b]Link Your Card[/b]"
                        font_size: "18dp"
                        halign: "center"

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("36dp", "33dp")

                    Image:
                        source: "assets/images/card_icon1.png"
                        pos_hint: {"center_y": .5}

            MDBoxLayout:
                Image:
                    size_hint: (.7, .7)
                    source: "assets/images/coming_soon_banner.png"
                    pos_hint: {"center_y": .5}

            MDBoxLayout:
                MDLabel:
                    padding: dp(6)
                    text: "This feature is not yet available, but it's on the way. Stay tuned for updates!"
                    font_size: "20dp"
                    bold: True
                    pos_hint: {"center_y": 1}
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app._white

"""

Builder.load_string(KV)


class WalletSetupScreen(MDScreen):
    network_menu, wallet_menu, crypto_help_dialog = None, None, None
    def __init__(self, store=None, firebase=None, show_snackbar=None, hide_card=None, card_to_show_or_hide=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._green, self._blue = "#2fc46c", "#005eff"

        self.wallets = {
            "Binance": ["BNB Chain"],
            "Bybit": ["Ethereum", "BNB Chain"],
            "MetaMask": ["Ethereum", "Polygon", "BNB Chain"],
        }
        self.wallet_requires_api = {"Binance": True, "Bybit": True, "MetaMask": False}
        self.user_data_store = store
        self.firebase = firebase
        self.id_token =  None
        self.u_id = None
        self.show_snackbar = show_snackbar
        self.hide_card = hide_card
        self.card_to_show_or_hide = card_to_show_or_hide

    def on_enter(self, *args):
        self.id_token = self.user_data_store.get("credentials")["id_token"] if self.user_data_store.exists("credentials") else None
        self.u_id = self.user_data_store.get("credentials")["uid"] if self.user_data_store.exists("credentials") else None
        if self.user_data_store.exists("mpesa_acc_was_added"):
            if self.user_data_store.get("mpesa_acc_was_added")["status"]:
                self.ids.acc_exists.opacity = 1
                self.ids.acc_exists_not.opacity = 0
                self.ids.mpesa_phone_number.disabled = True

    def get_next_account_key(self, existing_data: dict | None) -> str:
        numbers = []
        if existing_data:
            for key in existing_data:
                if key.startswith("account_"):
                    try: numbers.append(int(key.split("_")[1]))
                    except ValueError: pass
        return f"account_{max(numbers) + 1 if numbers else 1}"

    # methods for handling mpesa stuff...
    def fetch_mpesa_messages(self, silent=False):
        phone = self.ids.mpesa_phone_number.text
        if phone and len(phone) != 10 and self.manager.current == "wallet_setup_screen":
            self.show_snackbar("Phone number MUST be 10 digits...")
        else:
            if platform == "android":
                from android.permissions import request_permissions, Permission
                request_permissions(
                    [Permission.READ_SMS, Permission.RECEIVE_SMS],
                    lambda permissions, grants: self.on_permissions_granted(permissions, grants, silent)
                )

    def on_permissions_granted(self, permissions, grants, silent):
        if all(grants):
            if not silent:
                Clock.schedule_once(lambda dt: self.show_snackbar("Parsing your data...", background=self._green), 0.3)
            Clock.schedule_once(lambda dt: self.load_mpesa_messages(silent), 1)
        else:
            if not silent:
                Clock.schedule_once(lambda dt: self.show_snackbar("Permissions denied. Cannot fetch MPESA messages..."), 0.3)

    def load_mpesa_messages(self, silent):
        self.id_token = self.user_data_store.get("credentials")["id_token"] if self.user_data_store.exists("credentials") else None
        self.u_id = self.user_data_store.get("credentials")["uid"] if self.user_data_store.exists("credentials") else None
        messages = self.read_sms_from_sender("MPESA")
        phone = self.ids.mpesa_phone_number.text

        if messages:
            app = App.get_running_app()
            if not all([self.firebase, self.id_token, self.u_id]): return
            try:
                existing_raw_data = self.firebase.get_data(
                    id_token=self.id_token,
                    path=f"users/{self.u_id}/raw_data"
                )
            except Exception: existing_raw_data = {}
            next_key = self.get_next_account_key(existing_raw_data)

            try:
                self.firebase.put_data(
                    id_token=self.id_token,
                    path=f"users/{self.u_id}/raw_data/{next_key}",
                    data={
                        "Account Type": "M-PESA",
                        "Account ID": phone,
                        "Transactions": messages
                    }
                )
            except Exception:
                if not silent: self.show_snackbar("Failed to sync data.")

            self.user_data_store.put("acc_was_added", status=True)

            if not silent:
                try: full_name = self.firebase.get_data(id_token=self.id_token, path=f"users/{self.u_id}/user_profile")["Full name"]
                except Exception: self.show_snackbar("Failed to fetch profile info.")
                app.load_user_data(id_token=self.id_token, uid=self.u_id, full_name=full_name)
                self.update_link_mpesa_card_content()
        else:
            if not silent: Clock.schedule_once(lambda dt: self.show_snackbar("No MPESA messages found."), 0.3)
        self.ids.mpesa_phone_number.text = ""

    def update_link_mpesa_card_content(self):
        self.hide_card(self.card_to_show_or_hide("add_mpesa_acc_card"))
        self.ids.acc_exists.opacity = 1
        self.ids.acc_exists_not.opacity = 0
        self.ids.mpesa_phone_number.disabled = True
        self.manager.current = "home_screen"
        self.user_data_store.put("mpesa_acc_was_added", status=True)

    def read_sms_from_sender(self, sender):
        messages = []
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Uri = autoclass('android.net.Uri')
            inbox_uri = Uri.parse("content://sms/inbox")
            resolver = PythonActivity.mActivity.getContentResolver()

            selection = "address = ?"
            selection_args = [sender]

            cursor = resolver.query(inbox_uri, None, selection, selection_args, "date DESC")

            if cursor and cursor.getCount() > 0:
                while cursor.moveToNext():
                    body = cursor.getString(cursor.getColumnIndex("body"))
                    date = cursor.getString(cursor.getColumnIndex("date"))
                    full_msg = f"{sender}:\n{body}"
                    messages.append(full_msg)
                cursor.close()
            else:
                Clock.schedule_once(lambda dt: self.show_snackbar("No MPESA messages found."), 0.6)

        except Exception as e:
            print(f"SMS Extraction Error:\n{str(e)}")
            Clock.schedule_once(lambda dt: self.show_snackbar("Error fetching MPESA messages."), 0.6)

        return messages

    # methods for handling crypto wallet stuff...
    def show_wallet_menu(self, field):
        menu_items = [
            {"viewclass": "OneLineListItem", "text": wallet, "on_release": lambda x=wallet: self.set_wallet(field, x)}
            for wallet in self.wallets.keys()
        ]
        self.wallet_menu = MDDropdownMenu(caller=field, items=menu_items, width_mult=4)
        self.wallet_menu.open()

    def set_wallet(self, field, wallet):
        field.text = wallet
        self.wallet_menu.dismiss()
        self.ids.blockchain_network.text = ""
        self.ids.api_key.text = ""
        self.ids.api_key.disabled = not self.wallet_requires_api[wallet]
        self.ids.api_key_paste_btn.disabled = not self.wallet_requires_api[wallet]
        self.ids.api_secret.text = ""
        self.ids.api_secret.disabled = not self.wallet_requires_api[wallet]
        self.ids.api_secret_paste_btn.disabled = not self.wallet_requires_api[wallet]
        self.ids.wallet_address.text = ""
        self.ids.wallet_address.disabled = self.wallet_requires_api[wallet]
        self.ids.wallet_address_paste_btn.disabled = self.wallet_requires_api[wallet]
        self.validate_form()

    def show_network_menu(self, field):
        selected_wallet = self.ids.wallet_name.text
        if selected_wallet and selected_wallet in self.wallets:
            menu_items = [
                {"viewclass": "OneLineListItem", "text": network, "on_release": lambda x=network: self.set_network(field, x)}
                for network in self.wallets[selected_wallet]
            ]
            self.network_menu = MDDropdownMenu(caller=field, items=menu_items, width_mult=4)
            self.network_menu.open()

    def set_network(self, field, network):
        field.text = network
        self.network_menu.dismiss()
        self.validate_form()

    def paste_text(self, text_field):
        text_field.text = Clipboard.paste()
        self.validate_form()

    def validate_form(self):
        wallet_selected = self.ids.wallet_name.text != ""
        network_selected = self.ids.blockchain_network.text != ""
        api_key_filled = self.ids.api_key.text != "" if not self.ids.api_key.disabled else True
        api_secret_filled = self.ids.api_secret.text != "" if not self.ids.api_secret.disabled else True
        address_filled = self.ids.wallet_address.text != "" if not self.ids.wallet_address.disabled else True
        self.ids.submit_button.disabled = not (wallet_selected and network_selected and api_key_filled and api_secret_filled and address_filled)

    def submit_wallet(self):
        Clock.schedule_once(lambda dt: self.show_snackbar("Coming soon...", background=self._blue), 0)
        wallet_name = self.ids.wallet_name.text
        wallet_blockchain_network = self.ids.blockchain_network.text
        wallet_api_key = self.ids.api_key.text if not self.ids.api_key.disabled else ""
        wallet_api_secret = self.ids.api_secret.text if not self.ids.api_secret.disabled else ""
        wallet_address = self.ids.wallet_address.text if not self.ids.wallet_address.disabled else ""

        self.ids.wallet_name.text = ""
        self.ids.blockchain_network.text = ""
        self.ids.api_key.text = ""
        self.ids.api_secret.text = ""
        self.ids.wallet_address.text = ""
        self.ids.api_key.disabled = True
        self.ids.api_key_paste_btn.disabled = True
        self.ids.api_secret.disabled = True
        self.ids.api_secret_paste_btn.disabled = True
        self.ids.wallet_address.disabled = True
        self.ids.wallet_address_paste_btn.disabled = True
        self.ids.submit_button.disabled = True

        # self.user_data_store.put(
        #     f"{wallet_name}", 
        #     blockchain_network=f"{wallet_blockchain_network}",
        #     api_key=f"{wallet_api_key}", 
        #     api_secret=f"{wallet_api_secret}",
        #     address=f"{wallet_address}"
        # )
        # self.manager.current = "home_screen"

    def open_crypto_help_dialog(self):
        self.crypto_help_dialog = CryptoHelpDialog()
        self.crypto_help_dialog.open()

    def close_crypto_help_dialog(self):
        self.crypto_help_dialog.dismiss()
