from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from BACKEND.custom_markdown_formatter import MarkdownFormatter
from UI.reusables import TopLeftBackButton, InsightCard, Spacer, LabelChunks # noqa
# The "# noqa" comment suppresses the 'UNUSED IMPORTS' Warnings! 🙂🙂

KV = """
<TermsOfUseScreen>:
    name: "terms_of_use_screen"
    md_bg_color: app._dark

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(1.63)

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

            MDBoxLayout:
                size_hint: (1, 1)
                padding: dp(11.5), dp(0), dp(0), dp(0)

                CustomLabel:
                    text: "[size=18dp]Terms of Use[/size]"
                    bold: True
                    halign: "left"

        MDBoxLayout:
            md_bg_color: app._lightgray
            size_hint: (.98, None)
            height: dp(1.8)
            pos_hint: {"center_x": .5}

        InsightCard:
            padding: dp(17.5), dp(6), dp(17.5), dp(11.5)
            pos_hint: {"center_x": .5}
            radius: dp(0)

            MDScrollView:
                id: terms_of_use_scroll
                do_scroll_x: False
                do_scroll_y: True

                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height

                    Spacer:
                    Image:
                        source: "assets/images/terms_of_use_icon.png"
                        size_hint: (None, None)
                        size: ("136dp", "136dp")

                    Spacer:
                    Spacer:
                    LabelChunks:
                        text: root.chunk1
                    LabelChunks:
                        text: root.chunk2
                    LabelChunks:
                        text: root.chunk3

"""

Builder.load_string(KV)


class TermsOfUseScreen(MDScreen):
    chunk1, chunk2, chunk3 = StringProperty(""), StringProperty(""), StringProperty("")

    def on_pre_enter(self, *args):
        with open("assets/pft_terms_of_use.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        chunk_size = 50
        chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

        self.chunk1 = MarkdownFormatter().format_text("".join(chunks[0]))
        self.chunk2 = MarkdownFormatter().format_text("".join(chunks[1]))
        self.chunk3 = MarkdownFormatter().format_text("".join(chunks[2]))

    def on_pre_leave(self, *args):
        self.ids.terms_of_use_scroll.scroll_y = 1
