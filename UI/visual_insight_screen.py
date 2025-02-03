from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import InsightScreenTopBar, InsightCard, CustomTabs, Tab # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<InsightScreen2>:
    name: "insight_screen2"
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
                md_bg_color: app._invisible
                size_hint: (.9, .9)
                pos_hint: {"center_y": .5}    
                radius: dp(11.5)
                on_release: app.change_screen_wnt("insight_screen1")

                MDLabel:
                    padding: 8
                    text: "Text-based Insights"
                    font_size: "15dp"
                    bold: True
                    pos_hint: {"center_y": .5}
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app._gray

            MDCard:
                md_bg_color: app._blue
                size_hint: (.9, .9)
                pos_hint: {"center_y": .5}    
                radius: dp(11.5)

                MDLabel:
                    padding: 8
                    text: "Visual Insights"
                    font_size: "15dp"
                    bold: True
                    pos_hint: {"center_y": .5}
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app._white

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

"""

Builder.load_string(KV)


class InsightScreen2(MDScreen):
    pass
