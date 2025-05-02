
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.utils import platform
from UI.reusables import TopLeftBackButton, CustomLabel, FileChooserDialog # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """
<PersonalInfoScreen>:
    name: "personal_info_screen"
    md_bg_color: app._dark

    # Custom Top App Bar
    MDCard:
        size_hint: (1, None)
        height: dp(61)
        radius: dp(0)
        pos_hint: {"top": 1}
        md_bg_color: app._dark
        orientation: "vertical"

        MDBoxLayout:
            size_hint: (1, None)
            height: dp(60)
            padding: dp(17.5)

            MDBoxLayout:
                md_bg_color: app._lightgray
                size_hint: (None, None)
                size: ("34dp", "34dp")
                pos_hint: {"center_y": .5}
                radius: self.height / 2
                line_color: app._blue

                TopLeftBackButton:

            MDBoxLayout:
                size_hint: (1, 1)
                padding: dp(11.5), dp(0), dp(0), dp(0)

                CustomLabel:
                    text: "[size=18dp]Personal Info[/size]"
                    bold: True
                    halign: "left"

        MDBoxLayout:
            md_bg_color: app._lightgray
            size_hint: (.98, None)
            height: dp(1.8)
            pos_hint: {"center_x": .5}

    MDBoxLayout:
        size_hint: (None, None)
        size: ("170dp", "170dp")
        pos_hint: {"center_x": .51, "center_y": .66}

        MDBoxLayout:
            id: profile_photo_background
            size_hint: (None, None)
            size: ("160dp", "160dp")
            radius: self.height / 2
            line_color: app._blue

            FitImage:
                id: pi_dp # pi means "personal info"
                source: app.profile_photo
                radius: profile_photo_background.height / 2
                pos_hint: {"center_x": .5, "center_y": .5}

        MDBoxLayout:
            size_hint: (None, .95)
            width: dp(17.5)
            pos_hint: {"center_y": .5}
            padding: dp(-36), dp(0), dp(0), dp(0)

            MDCard:
                ripple_behavior: True
                md_bg_color: app._blue
                size_hint: (None, None)
                size: ("55dp", "55dp")
                radius: self.height / 2
                on_release: root.open_file_dialog()

                MDIcon:
                    padding: dp(15)
                    icon: "pencil"
                    pos_hint: { "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app._white

    MDCard:
        md_bg_color: app._lightgray
        size_hint: (.9, .1)
        pos_hint: {"center_x": .5, "top": .45} 
        radius: dp(11.5)
        padding: dp(23)

        MDBoxLayout:
            CustomLabel:
                id: pi_name # pi means "personal info"
                text: f"[color=a6a6a6][size=14dp][b]Full name[/b][/size][/color]\\n{app.full_name}"

    MDCard:
        md_bg_color: app._lightgray
        size_hint: (.9, .1)
        pos_hint: {"center_x": .5, "top": .32}    
        radius: dp(11.5)
        padding: dp(23)

        MDBoxLayout:
            CustomLabel:
                id: pi_mail # pi means "personal info"
                text: f"[color=a6a6a6][size=14dp][b]Email address[/b][/size][/color]\\n{app.email_address}"

"""

Builder.load_string(KV)


class PersonalInfoScreen(MDScreen):
    def __init__(self, store=None, snackbar=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_data_store = store
        self.show_snackbar = snackbar

    def open_file_dialog(self):
        def _launch_file_chooser():
            def on_file_selected(file_path):
                self.profile_photo = file_path
                self.user_data_store.put("profile_photo", location=file_path)

            dialog = FileChooserDialog(on_select_callback=on_file_selected)
            Clock.schedule_once(lambda dt: dialog.open(), 0.3)

        if platform == "android":
            from android.permissions import check_permission, request_permissions, Permission # type: ignore
            read_granted = check_permission(Permission.READ_EXTERNAL_STORAGE)
            write_granted = check_permission(Permission.WRITE_EXTERNAL_STORAGE)

            if read_granted and write_granted: _launch_file_chooser()
            else:
                def permission_callback(permissions, grants):
                    if all(grants): _launch_file_chooser()
                    else: self.show_snackbar(text="Please Enable storage access in settings.")

                request_permissions(
                    [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE],
                    permission_callback
                )

        else: _launch_file_chooser()
