from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton # noqa
from UI.reusables import TextFieldNormal # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<FullNameScreen>:
    name: "full_name_input_screen"
    md_bg_color: app._dark

    TopLeftBackButton:

    MDLabel:
        padding: dp(25)
        text: "Enter your full name"
        font_size: "26dp"
        bold: True
        pos_hint: {"center_y": .85}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._white

    TextFieldNormal:
        id: first_name
        hint_text: "  First name "
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .75}
        on_text: app.enable_submit_btn()

    TextFieldNormal:
        id: last_name
        hint_text: "  Last name "
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .64}
        on_text: app.enable_submit_btn()

    # submit full name btn
    MDCard:
        id: submit_btn_bg
        md_bg_color: app._tinted
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
            font_size: "20dp"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: 
                app.get_name()
                app.change_screen_wt("wallet_setup_screen", "left")

"""

Builder.load_string(KV)


class FullNameScreen(MDScreen):
    pass

