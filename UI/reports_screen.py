
from kivy.app import App
from kivy.utils import platform
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from UI.reusables import TopLeftBackButton, GridCard, CustomLabel, HiddenCard, HiddenCardReportsContent, DownloadReportButton, CloseCardButton # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂


KV = """
<ReportsScreen>:
    name: "reports_screen"
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
        source: "assets/images/reports_icon.png"
        size_hint: (.23, .23)
        pos_hint: {"center_x": .5, "center_y": .8}

    MDLabel:
        padding: dp(46)
        text: "Download\\nFinancial Reports"
        font_size: "36dp"
        bold: True
        pos_hint: {"center_y": .65}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._white

    # ------------------------- report options --------------------------
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
                icon_path: "assets/images/daily.png"
                grid_card_txt: "Daily Report"
                on_release: app.show_card(app.card_to_show_or_hide("daily_report_card"))

            GridCard:
                size_hint: (1, 1)
                icon_path: "assets/images/weekly.png"
                grid_card_txt: "Weekly Report"
                on_release: app.show_card(app.card_to_show_or_hide("weekly_report_card"))

        MDBoxLayout:
            padding: dp(6)
            spacing: dp(23)
            size_hint: (1, None)
            height: dp(156)

            GridCard:
                size_hint: (1, 1)
                icon_path: "assets/images/monthly.png"
                grid_card_txt: "Monthly Report"
                on_release: app.show_card(app.card_to_show_or_hide("monthly_report_card"))

            GridCard:
                size_hint: (1, 1)
                icon_path: "assets/images/yearly.png"
                grid_card_txt: "Yearly Report"
                on_release: app.show_card(app.card_to_show_or_hide("yearly_report_card"))

        MDBoxLayout:
            md_bg_color: app._tinted
            size_hint: (1, None)
            height: dp(56)
            padding: dp(8), dp(0), dp(0), dp(0)
            radius: dp(11.5)

            MDBoxLayout:
                size_hint: (None, None)
                size: ("26dp", "23dp")
                pos_hint: {"center_y": .5}
                MDIcon:
                    icon: "information"
                    pos_hint: {"center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app._white

            MDBoxLayout:
                CustomLabel:
                    text: "[b] The reports are available in [color=00afff][size=16sp].csv[/size][/color] format only.[/b]"
                    padding: dp(11.5)
                    font_size: "14dp"

    HiddenCard:
        id: daily_report_card

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
                        on_release: app.hide_card(app.card_to_show_or_hide("daily_report_card"))

                MDBoxLayout:
                    CustomLabel:
                        text: "[b]Daily report[/b]"
                        font_size: "20dp"
                        halign: "center"

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("38dp", "38dp")
                    Image:
                        source: "assets/images/daily.png"
                        pos_hint: {"center_y": .5}

            HiddenCardReportsContent:
                date_time_label: f"\\n[size=23dp]{app.today},[/size]\\n[size=26dp]{app.month} {app.today_date}, {app.year}[/size]"
                info_text_label: "Tap the 'Download' button and check your 'Downloads Folder' after a couple of seconds...\\n\\n[color=00afff]File name pattern: [i]pft_dr_***.csv[/i]"

            DownloadReportButton:
                on_release: root.on_download_report_pressed("daily")

    HiddenCard:
        id: weekly_report_card

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
                        on_release: app.hide_card(app.card_to_show_or_hide("weekly_report_card"))

                MDBoxLayout:
                    CustomLabel:
                        text: "[b]Weekly report[/b]"
                        font_size: "20dp"
                        halign: "center"

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("38dp", "38dp")
                    Image:
                        source: "assets/images/weekly.png"
                        pos_hint: {"center_y": .5}

            HiddenCardReportsContent:
                date_time_label: f"\\n[size=23dp]Year {app.week_number_year}: Week {app.current_week_number}[/size]\\n[size=19dp]{app.week_number_start_date} - {app.week_number_end_date}[/size]"
                info_text_label: "Tap the 'Download' button,  and check your 'Downloads Folder' after a couple of seconds...\\n\\n[color=00afff]File name pattern: [i]pft_wr_***.csv[/i]"

            DownloadReportButton:
                on_release: root.on_download_report_pressed("weekly")

    HiddenCard:
        id: monthly_report_card

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
                        on_release: app.hide_card(app.card_to_show_or_hide("monthly_report_card"))

                MDBoxLayout:
                    CustomLabel:
                        text: "[b]Monthly report[/b]"
                        font_size: "20dp"
                        halign: "center"

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("38dp", "38dp")
                    Image:
                        source: "assets/images/monthly.png"
                        pos_hint: {"center_y": .5}

            HiddenCardReportsContent:
                date_time_label: f"[size=23dp]For the month of\\n{app.previous_month}[/size]"
                info_text_label: "Tap the 'Download' button and check your 'Downloads Folder' after a couple of seconds...\\n\\n[color=00afff]File name pattern: [i]pft_mr_***.csv[/i]"

            DownloadReportButton:
                on_release: root.on_download_report_pressed("monthly")

    HiddenCard:
        id: yearly_report_card

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
                        on_release: app.hide_card(app.card_to_show_or_hide("yearly_report_card"))

                MDBoxLayout:
                    CustomLabel:
                        text: "[b]Yearly report[/b]"
                        font_size: "20dp"
                        halign: "center"

                MDBoxLayout:
                    size_hint: (None, None)
                    size: ("38dp", "38dp")
                    Image:
                        source: "assets/images/yearly.png"
                        pos_hint: {"center_y": .5}

            HiddenCardReportsContent:
                date_time_label: f"\\n[size=26dp]Year {app.year},[/size]\\n[size=23dp]1 January - {app.today_date} {app.month}[/size]"
                info_text_label: "Tap the 'Download' button and check your 'Downloads Folder' after a couple of seconds...\\n\\n[color=00afff]File name pattern: [i]pft_yr_***.csv[/i]"

            DownloadReportButton:
                on_release: root.on_download_report_pressed("yearly")

"""

Builder.load_string(KV)


class ReportsScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._green = "#2fc46c"
        self.parser = None

    def on_enter(self):
        app = App.get_running_app()
        self.parser = app.data_handler.parser

    def _download_report(self, csv_type):
        app = App.get_running_app()
        self.parser = app.data_handler.parser
        filepath = self.parser.export_to_csv(csv_type=csv_type)

        if filepath:
             Clock.schedule_once(lambda dt: app.show_snackbar(text=f"pft_{csv_type}_report Downloaded Successfully!", background=self._green), 1)
        else:
             Clock.schedule_once(lambda dt: app.show_snackbar(text="Download failed. Try again."), 1)

    def on_download_report_pressed(self, csv_type):
        self._download_report(csv_type)
