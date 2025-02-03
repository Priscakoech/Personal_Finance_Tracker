from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton # noqa
from UI.reusables import TextFieldNormal # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<AddMpesaAccScreen>:
    name: "add_mpesa_acc_screen"
    md_bg_color: app._dark

    TopLeftBackButton:

    MDLabel:
        padding: dp(25)
        text: "Link Your M-PESA Account"
        font_size: "26dp"
        bold: True
        pos_hint: {"center_y": .87}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._white

    MDCard:
        md_bg_color: app._tinted
        size_hint: (.87, None)
        height: "123dp"
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
                text: "This action requires you to grant the app permission to access your messages. " +\
                    "Make sure that the phone number you are providing, has it's corresponding" +\
                    " SIM Card mounted on this device."
                padding: dp(11.5)
                pos_hint: {"center_y": .5}
                font_size: "15dp"
                bold: True
                halign: "left"
                theme_text_color: "Custom"
                text_color: app._gray

    TextFieldNormal:
        id: mpesa_phone_number
        hint_text: "  M-PESA Number "
        helper_text: "  Format: 0712xxx123 or 0111XXX123"
        input_type: "number" 
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .56}

    # add mpesa account  btn
    MDCard:
        md_bg_color: app._green
        size_hint: (.85, .07)
        pos_hint: {"center_x": .5, "center_y": .42}
        radius: dp(11.5), dp(11.5), dp(11.5), dp(11.5)
        ripple_behavior: True

        MDRectangleFlatIconButton:
            text: "Link"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app._dark
            font_size: "20dp"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.change_screen_wt("home_screen", "left")

"""

Builder.load_string(KV)


class AddMpesaAccScreen(MDScreen):
    pass
