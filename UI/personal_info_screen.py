from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton, CustomLabel, HiddenCard, CloseCardButton, LeftIconContainer, RightArrow # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<PersonalInfoScreen>:
    name: "personal_info_screen"
    md_bg_color: app._dark

    MDCard:
        md_bg_color: app._tinted
        size_hint: (.9, .085)
        pos_hint: {"center_x": .5, "top": .95}    
        radius: dp(11.5)

        TopLeftBackButton:
            pos_hint: {"center_y": .5}

        MDLabel:
            padding: (11.5, 0)
            text: "Personal Information"
            font_style: "H6"
            pos_hint: {"center_y": .5}
            halign: "left"
            theme_text_color: "Custom"
            text_color: app._white

    MDCard:
        background: app.profile_photo
        md_bg_color: app._white
        line_color: app._dark
        size_hint: (None, None)
        size: ("160dp", "160dp")
        radius: self.height / 2
        pos_hint: {"center_x": .5, "center_y": .63}

        MDRelativeLayout:
            MDCard:
                md_bg_color: app._blue
                size_hint: (None, None)
                size: ("55dp", "55dp")
                radius: self.height / 2
                pos_hint: {"right": 1, "top": .3}
                on_release: app.show_card(app.card_to_show_or_hide("change_avatar"))

                MDIcon:
                    padding: dp(15)
                    icon: "pencil"
                    pos_hint: { "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app._white

    MDCard:
        md_bg_color: app._tinted
        size_hint: (.9, .1)
        pos_hint: {"center_x": .5, "top": .45} 
        radius: dp(11.5)
        padding: dp(23)

        MDBoxLayout:
            CustomLabel:
                text: f"[color=a6a6a6][size=14dp][b]Full name[/b][/size][/color]\\n{app.full_name}"

    MDCard:
        md_bg_color: app._tinted
        size_hint: (.9, .1)
        pos_hint: {"center_x": .5, "top": .32}    
        radius: dp(11.5)
        padding: dp(23)

        MDBoxLayout:
            CustomLabel:
                text: f"[color=a6a6a6][size=14dp][b]Email address[/b][/size][/color]\\n{app.email_address}"

    HiddenCard:
        id: change_avatar
        size_hint_y: .2

        MDRelativeLayout:
            orientation: "vertical"

            MDCard:
                md_bg_color: app._invisible
                size_hint: (1, .1)
                pos_hint: {"center_x": .5, "top": 1}

                CloseCardButton:
                    md_bg_color: app._invisible
                    size_hint: None, None
                    on_release: app.hide_card(app.card_to_show_or_hide("change_avatar"))

                MDLabel:
                    text: "Change Avatar    "
                    font_style: "H6"
                    pos_hint: {"center_y": .5}
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app._white

            MDCard:
                md_bg_color: app._tinted
                size_hint: (1, .65)
                pos_hint: {"center_x": .5, "center_y": .2}
                radius: dp(11.5)
                padding: dp(11.5)
                on_release: app.change_profile_pic()

                LeftIconContainer:
                    MDIcon:
                        icon: "camera-burst"
                        theme_text_color: "Custom"
                        text_color: app._white
                        pos_hint: {"center_y": .5}

                MDBoxLayout:
                    CustomLabel:
                        text: "Choose from library"
                        font_size: "17dp"

                RightArrow:

"""

Builder.load_string(KV)


class PersonalInfoScreen(MDScreen):
    pass
