from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import SlideIndicator, NavIconButton # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<HomeScreen>:
    name: "home_screen"
    md_bg_color: app._dark

    MDLabel:
        padding: dp(23)
        text: f"[color=a6a6a6]{app.greeting_text()}[/color]\\n[size=24dp]{app.full_name}[/size]\\n\\nOverview"
        markup: True
        halign: "left"
        font_size: "16dp"
        bold: True
        pos_hint: {"center_y": .91}
        theme_text_color: "Custom"
        text_color: app._white

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

    # -------- indicators --------
    MDBoxLayout:
        orientation: "horizontal"
        size_hint: (None, None)
        size: ("63dp", "23dp")
        pos_hint: {"center_x": .5, "center_y": .47}
        spacing: dp(8.5)
        padding: dp(11.5)

        SlideIndicator:
            id: slide1_indicator_color
            md_bg_color: app._blue

        SlideIndicator:
            id: slide2_indicator_color

    # ---------------------- minimalistic "transactions" overview --------------------------  
    MDCard:
        md_bg_color: app._green
        background: "assets/images/bg5.jpg"
        size_hint: (1, .45)
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
                font_size: "16dp"
                bold: True
                theme_text_color: "Custom"
                text_color: app._white

            MDBoxLayout:
                md_bg_color: app._invisible
                size_hint: (None, 1)
                width: "123dp"

                MDCard:
                    md_bg_color: app._invisible
                    size: (1, 1)
                    on_release: app.change_screen_wt("transactions_screen", "left")

                    MDLabel:
                        padding: dp(6)
                        text: "View all"
                        halign: "right"
                        pos_hint: {"center_y": .5}
                        font_size: "16dp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: app._gray

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
    MDBoxLayout:
        md_bg_color: app._invisible
        size_hint: (.95, None)
        height: "60dp"
        pos_hint: {"center_x": .5, "bottom": .085}    
        radius: dp(11.5)
        orientation: "horizontal"
        padding: (17.5, 5)
        spacing: dp(17.5)

        NavIconButton:
            icon: "assets/images/home_icon.png"

        NavIconButton:
            icon: "assets/images/wallet_icon.png"
            on_release: app.change_screen_wt("wallet_screen", "left")

        NavIconButton:
            icon: "assets/images/insight.png"
            on_release: app.change_screen_wt("insight_screen1", "left")

        NavIconButton:
            icon: "assets/images/settings_icon.png"
            on_release: app.change_screen_wt("settings_screen", "left")

    # ------------------------------------ User Profile -----------------------------------
    MDCard:
        background: app.profile_photo
        md_bg_color: app._white
        size_hint: (None, None)
        width: "63dp"
        height: "63dp"
        radius: self.height / 2
        pos_hint: {"right": .965, "top": .973}
        on_release: app.change_screen_wt("personal_info_screen", "left")

"""

Builder.load_string(KV)


class HomeScreen(MDScreen):
    pass
