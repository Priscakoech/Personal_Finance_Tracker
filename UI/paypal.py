from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<AddPaypalAccScreen>:
    name: "add_paypal_acc_screen"
    md_bg_color: app._dark

    TopLeftBackButton:

    MDLabel:
        padding: dp(25)
        text: "Link Your PayPal Account"
        font_size: "26dp"
        bold: True
        pos_hint: {"center_y": .87}
        halign: "left"
        theme_text_color: "Custom"
        text_color: app._white

    MDCard:
        md_bg_color: app._tinted
        size_hint: (.87, None)
        height: "60dp"
        pos_hint: {"center_x": .5, "center_y": .77}    
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
                pos_hint: {"center_y": .5}
                font_size: "15dp"
                bold: True
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
            font_size: "20dp"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.change_screen_wt("home_screen", "left")

"""

Builder.load_string(KV)


class AddPaypalAccScreen(MDScreen):
    pass
