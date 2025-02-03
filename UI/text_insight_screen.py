from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import InsightScreenTopBar, InsightCard, CustomTabs, Tab # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<InsightScreen1>:
    name: "insight_screen1"
    md_bg_color: app._dark

    InsightScreenTopBar:

    MDCard:
        md_bg_color: app._tinted
        size_hint: (.9, .06)
        pos_hint: {"center_x": .5, "top": .87}    
        radius: dp(11.5)

        MDBoxLayout:
            orientation: "horizontal"

            MDCard:
                md_bg_color: app._blue
                size_hint: (.9, .9)
                pos_hint: {"center_y": .5}    
                radius: dp(11.5)

                MDLabel:
                    padding: 8
                    text: "Text-based Insights"
                    font_size: "15dp"
                    bold: True
                    pos_hint: {"center_y": .5}
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app._white

            MDCard:
                md_bg_color: app._invisible
                size_hint: (.9, .9)
                pos_hint: {"center_y": .5}    
                radius: dp(11.5)
                on_release: app.change_screen_wnt("insight_screen2")

                MDLabel:
                    padding: 8
                    text: "Visual Insights"
                    font_size: "15dp"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: app._gray
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
            font_size: "22dp"
            size_hint: (1, 1)
            line_color: app._invisible
            _no_ripple_effect: True
            on_release: app.start_text_animation()

    MDLabel:
        text: "Powered by ChatGPT-4o mini"
        font_size: "14dp"
        bold: True
        pos_hint: {"center_y": .036}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._gray

"""

Builder.load_string(KV)


class InsightScreen1(MDScreen):
    pass
