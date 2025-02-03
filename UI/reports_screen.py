from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton, HiddenCard, CloseCardButton # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<ReportsScreen>:
    name: "reports_screen"
    md_bg_color: app._dark

    TopLeftBackButton:
        text_color: app._white

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

                CloseCardButton:
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
                    font_size: "22dp"
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

                CloseCardButton:
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
                    font_size: "22dp"
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

                CloseCardButton:
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
                    font_size: "22dp"
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

                CloseCardButton:
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
                    font_size: "22dp"
                    size_hint: (1, 1)
                    line_color: app._invisible
                    _no_ripple_effect: True

"""

Builder.load_string(KV)


class ReportsScreen(MDScreen):
    pass