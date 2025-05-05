
import os
from plyer import storagepath
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
from kivy.animation import Animation
from kivy.utils import platform, get_color_from_hex
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ColorProperty
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.modalview import ModalView
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.textfield import MDTextField
from kivymd_extensions.akivymd.uix.charts import AKPieChart, PieChartNumberLabel
from kivymd_extensions.akivymd.helper import point_on_circle
from BACKEND.custom_markdown_formatter import MarkdownFormatter


REUSABLES = """

<TopLeftBackButton>:
    icon: "arrow-left"
    size_hint: (1, 1)
    icon_size: "22dp"
    pos_hint: {"center_x": .5, "center_y": .5}
    theme_text_color: "Custom"
    text_color: app._white
    _no_ripple_effect: True
    on_release: app.go_back()

<TextFieldNormal>:
    font_size: "17dp"
    mode: "fill"
    helper_text_mode: "persistent"
    fill_color_normal: app._white
    fill_color_focus: app._white
    line_color_focus: app._blue
    hint_text_color_focus: "#222222"
    hint_text_color_normal: "#222222"
    text_color_normal: "#222222"
    text_color_focus: "#000000"
    line_color: app._blue
    radius: [10, 10, 10, 10]

<PasswordTextField>:
    size_hint: .85, None
    height: password.height - 10

    MDTextField:
        id: password
        hint_text: root.hint_text
        text: root.text
        password: True
        font_size: "17dp"
        mode: "fill"
        helper_text_mode: "persistent"
        fill_color_normal: app._white
        fill_color_focus: app._white
        line_color_focus: app._blue
        hint_text_color_focus: "#222222"
        hint_text_color_normal: "#222222"
        text_color_normal: "#222222"
        text_color_focus: "#000000"
        line_color: app._blue
        radius: [10, 10, 10, 10]

    MDIconButton:
        icon: "eye-off"
        pos_hint: {"center_y": .5}
        pos: password.width - self.width, 0
        theme_icon_color: "Custom"
        icon_color: "#222222"
        _no_ripple_effect: True
        on_release:
            self.icon = "eye" if self.icon == "eye-off" else "eye-off"
            password.password = False if password.password is True else True

<KeyItem>:
    spacing: dp(6)
    size_hint_y: None
    height:  dp(15)

    MDBoxLayout:
        md_bg_color: root.key_color
        size_hint: (None, None)
        size: ("10dp", "10dp")
        pos_hint: {"center_y": .5}

    MDBoxLayout:
        CustomLabel:
            text: f"[size=12dp]{root.key_text}[/size]"

<WidgetContainer>:
    md_bg_color: app._tinted
    size_hint: (.9, .085)
    radius: dp(11.5)
    padding: dp(6)

<LeftIconContainer>:
    size_hint: (None, None)
    size: ("43dp", "43dp")
    pos_hint: {"center_y": .5}

<GridCard>:
    md_bg_color: app._lightgray
    radius: dp(23)
    padding: dp(6), dp(33), dp(6), dp(11.5)
    orientation: "vertical"

    MDBoxLayout:
        size_hint: (None, None)
        size: ("52dp", "52dp")
        pos_hint: {"center_x": .5}
        Image:
            source: root.icon_path
            size_hint: (1, 1)
            pos_hint: {"center_x": .5, "center_y": .5}

    MDBoxLayout:

    MDBoxLayout:
        size_hint: (1, None)
        height: dp(32)

        CustomLabel:
            text: root.grid_card_txt
            halign: "center"

<CustomLabel>:
    halign: "left"
    markup: True
    font_size: "16dp"
    pos_hint: {"center_y": .5}
    theme_text_color: "Custom"
    text_color: app._white

<LabelChunks>:
    markup: True
    size_hint_y: None
    height: self.texture_size[1] + dp(10)
    halign: "left"
    valign: "top"

<RightArrow>:
    size_hint: (None, None)
    size: ("23dp", "23dp")
    pos_hint: {"center_y": .5}

    MDIcon:
        icon: "chevron-right"
        theme_text_color: "Custom"
        text_color: app._white
        pos_hint: {"center_y": .5}

<HiddenCard>:
    md_bg_color: app._green
    background: "assets/images/bg5.jpg"
    size_hint: (1, .55)
    y: -self.height
    pos_hint: {"center_x": .5}
    radius: dp(46), dp(46), dp(0), dp(0)
    padding: dp(23)
    on_touch_move: root.on_touch_move(args[1])

<HiddenCardReportsContent>:
    orientation: "vertical"
    spacing: dp(17.5)

    MDBoxLayout:
        md_bg_color: app._tinted
        padding: dp(11.5)
        radius: dp(11.5)

        CustomLabel:
            text: root.date_time_label
            halign: "left"

    MDBoxLayout:
        md_bg_color: app._tinted
        padding: dp(11.5)
        radius: dp(11.5)
        spacing: dp(11.5)

        MDBoxLayout:
            size_hint: (None, 1)
            width: dp(23)

            MDIcon:
                icon: "information"
                pos_hint: {"center_y": .5}
                theme_text_color: "Custom"
                text_color: app._white

        MDBoxLayout:
            MDLabel:
                text: root.info_text_label
                markup: True
                bold: True
                pos_hint: {"center_y": .5}
                font_style: "Subtitle2"
                halign: "left"
                theme_text_color: "Custom"
                text_color: app._white

<DownloadReportButton>:
    md_bg_color: app._white
    size_hint: (1, None)
    height: dp(48)
    pos_hint: {"center_x": .5}
    radius: dp(11.5)
    ripple_behavior: True

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
        on_release: root.trigger_download()

<CloseCardButton>:
    _no_ripple_effect: True
    icon: "close"
    theme_text_color: "Custom"
    text_color: app._white
    md_bg_color: app._invisible
    size_hint_y: .9
    pos_hint: {"center_y": .5, "left": 1}

<CustomTabs>:
    indicator_color: app._blue
    text_color_active: app._blue
    text_color_normal: app._gray
    tab_indicator_anim: True
    background_color: app._invisible
    underline_color: app._invisible

<InsightCard>:
    size_hint: (1, 1)
    pos_hint: {"center_x": .5, "center_y": .5}
    padding: (6, 100)
    md_bg_color: app._dark
    padding: dp(6), dp(11.5)

<CustomCard>:
    md_bg_color: app._green
    background: "assets/images/bg5.jpg"
    size_hint: (1, None)
    height: dp(228)
    pos_hint: {"center_x": .5}
    radius: dp(11.5)

<CustomCardLayout>:
    orientation: "vertical"
    spacing: dp(3)

<CustomCardIdentifier>:
    text: root.text
    size_hint: (1, None)
    height: dp(17.5)
    padding: dp(6)

<CustomCardTitleBar>:
    size_hint: (1, .23)
    md_bg_color: app._red
    pos_hint: {"top": 1}
    radius: dp(11.5), dp(11.5), dp(0), dp(0)

    CustomLabel:
        text: root.title
        padding: dp(6)

<CustomCardGraph>:
    orientation: "vertical"
    size_hint: (1, 1)
    md_bg_color: app._tinted
    radius: dp(0), dp(0), dp(11.5), dp(11.5)

<CustomCardTitleBarAlt>:
    orientation: "horizontal"
    spacing: dp(3)
    size_hint: (1, .23)
    radius: dp(11.5), dp(11.5), dp(0), dp(0)

    MDBoxLayout:
        CustomLabel:
            text: root.left_text
            padding: dp(6)

    MDBoxLayout:
        size_hint: (None, 1)
        width: dp(150)

        CustomLabel:
            text: root.right_text
            padding: dp(6)

<CustomCardListItem>:
    orientation: "horizontal"
    spacing: dp(3)
    size_hint: (1, None)
    height: dp(32)
    md_bg_color: app._lightgray
    padding: dp(4), dp(0), dp(0), dp(0)

    MDBoxLayout:
        size_hint: (None, None)
        size: ("24dp", "24dp")
        pos_hint: {"top": 1}
        radius: self.height / 2
        pos_hint: {"center_y": .5}

        MDCard:
            background: root.icon_path
            md_bg_color: root.c_bg_color

    MDBoxLayout:
        size_hint: (1, 1)
        pos_hint: {"top": 1}

        CustomLabel:
            text: root.left_text
            padding: dp(3)

    MDBoxLayout:
        size_hint: (None, 1)
        width: dp(150)
        pos_hint: {"top": 1}

        CustomLabel:
            text: root.right_text
            padding: dp(6)

<ExpenseCategoryCard>:
    height: dp(200)
    CustomCardLayout:
        CustomCardTitleBarAlt:
            md_bg_color: app._red
            left_text: "[b][color=ffffff]Spending Category[/color][/b]"
            right_text: "[b][color=ffffff]Amount[/color][/b]"

        CustomCardGraph:
            md_bg_color: app._light
            background: "assets/images/bg5.jpg"
            CustomCardListItem:
                md_bg_color: app._invisible
                icon_path: ""
                c_bg_color: "#f28500"
                left_text: "Friends & Family"
                right_text: root.e_cat_val1

            CustomCardListItem:
                icon_path: ""
                c_bg_color: "#8887f1"
                left_text: "Housing"
                right_text: root.e_cat_val2

            CustomCardListItem:
                md_bg_color: app._invisible
                icon_path: ""
                c_bg_color: "#ffd046"
                left_text: "Utilities"
                right_text: root.e_cat_val3

            CustomCardListItem:
                icon_path: ""
                c_bg_color: "#e78777"
                left_text: "Groceries"
                right_text: root.e_cat_val4

            CustomCardListItem:
                md_bg_color: app._invisible
                icon_path: ""
                c_bg_color: "#bed09c"
                left_text: "Miscellaneous"
                right_text: root.e_cat_val5

<IncomeCategoryCard>:
    height: dp(200)
    CustomCardLayout:
        CustomCardTitleBarAlt:
            md_bg_color: app._green
            left_text: "[b][color=00001f]Income Category[/color][/b]"
            right_text: "[b][color=00001f]Amount[/color][/b]"

        CustomCardGraph:
            md_bg_color: app._light
            background: "assets/images/bg5.jpg"
            CustomCardListItem:
                md_bg_color: app._invisible
                icon_path: ""
                c_bg_color: "#f28500"
                left_text: "Friends & Family"
                right_text: root.i_cat_val1

            CustomCardListItem:
                icon_path: ""
                c_bg_color: "#66dd66"
                left_text: "Salary"
                right_text: root.i_cat_val2

            CustomCardListItem:
                md_bg_color: app._invisible
                icon_path: ""
                c_bg_color: "#90d3c2"
                left_text: "Investments"
                right_text: root.i_cat_val3

            CustomCardListItem:
                icon_path: ""
                c_bg_color: "#66ac85"
                left_text: "Side Gigs"
                right_text: root.i_cat_val4

            CustomCardListItem:
                md_bg_color: app._invisible
                icon_path: ""
                c_bg_color: "#37c3ea"
                left_text: "Other Income"
                right_text: root.i_cat_val5

<Spacer>:
    size_hint: (1, None)
    height: dp(11.5)
    md_bg_color: app._invisible

<FinancialReportsButton>:
    md_bg_color: app._white
    size_hint: (1, None)
    height: dp(49)
    radius: dp(11.5)
    ripple_behavior: True

    MDRectangleFlatIconButton:
        text: "Financial Reports"
        halign: "center"
        theme_text_color: "Custom"
        text_color: "#00001f"
        font_size: "22dp"
        size_hint: (1, 1)
        line_color: app._invisible
        _no_ripple_effect: True
        on_release: app.change_screen_wt("reports_screen", "left")

<InsightScreenTopBar>:
    md_bg_color: app._tinted
    size_hint: (.9, .085)
    pos_hint: {"center_x": .5, "top": .97}    
    radius: dp(11.5)

    TopLeftBackButton:
        pos_hint: {"center_y": .5}

    MDLabel:
        padding: (23, 0)
        text: "Insights"
        font_style: "H6"
        pos_hint: {"center_y": .5}
        halign: "center"
        theme_text_color: "Custom"
        text_color: app._white

    MDIconButton:
        _no_ripple_effect: True
        icon: "assets/images/settings_icon.png"
        pos_hint: {"center_y": .5}
        on_release: app.change_screen_wt("settings_screen", "left")

<CustomTwoLineListItem>:
    divider: None
    _no_ripple_effect: True

    MDCard:
        md_bg_color: app._invisible
        size_hint: (1, 1)
        pos_hint: {"center_x": .5, "center_y": .5}
        padding: dp(6)

        MDCard:
            md_bg_color: app._tinted
            radius: dp(11.5)
            padding: dp(2), dp(6), dp(6), dp(6)

            MDBoxLayout:
                size_hint: (None, None)
                size: ("50dp", "50dp")
                pos_hint: {"center_y": .5}
                Image:
                    source: root.icon_path
                    size_hint: (1,.9)
                    pos_hint: {"center_y": .5}

            MDBoxLayout:
                padding: dp(3)
                MDLabel:
                    text: root.left_text
                    markup: True
                    pos_hint: {"center_y": .5}
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: app._white

            MDBoxLayout:
                size_hint: (None, 1)
                width: dp(150)
                MDLabel:
                    text: root.right_text
                    markup: True
                    pos_hint: {"center_y": .5}
                    halign: "right"
                    theme_text_color: "Custom"
                    text_color: app._white

<CEPOneLineListItem>:
    size_hint: (1, None)
    height: dp(root.list_height)
    padding: dp(8), dp(0), dp(0), dp(0)

    MDBoxLayout:
        CustomLabel:
            text: f"[b][size=13dp][color=a6a6a6]{root.left_text}[/size][b]"
            halign: "left"
            shorten: True

    MDBoxLayout:
        size_hint: (None, 1)
        width: dp(163)
        spacing: dp(6)

        MDBoxLayout:
            CustomLabel:
                text: f"[b][size=13dp][color=ffffff]{root.right_text}[/size][b]"
                halign: "left"

<AllTransactionsCard>:
    orientation: "vertical"
    md_bg_color: app._tinted
    size_hint_y: None
    height: self.minimum_height
    radius: dp(17.5)
    padding: dp(14.5)
    spacing: dp(8)

    MDCard:
        background: "assets/images/bg5.jpg"
        md_bg_color: app._green
        size_hint: (1, None)
        height: dp(80)
        radius: dp(17.5)

        MDBoxLayout:
            orientation: "vertical"
            size_hint: (1, 1)
            padding: dp(6)

            CustomLabel:
                text: f"[b][size=15dp]{root.sr_name}[/size][/b]"
                halign: "left"
                text_color: "#ffffff"
                shorten: True

        MDBoxLayout:
            orientation: "vertical"
            size_hint: (1, 1)
            padding: dp(6)

            CustomLabel:
                text: f"[b][size=17dp]{root.amount}[/size][/b]"
                halign: "right"
                text_color: "#2fc46cff" if "+" in root.amount else "#ff3f4fff"

    MDBoxLayout:
        orientation: "horizontal"
        size_hint: (1, None)
        height: dp(23)
        spacing: dp(6)
        padding: dp(2), dp(6), dp(17.5), dp(0)

        MDIcon:
            icon: "clock"
            pos_hint: {"center_y": .5}
            halign: "left"
            theme_text_color: "Custom"
            text_color: app._blue
            font_size: dp(21)

        CustomLabel:
            text: f"[b][size=14dp][color=ffffff]{root.t_time}[/size][b]"
            halign: "left"

        MDIcon:
            icon: f"{root.acc_type}"
            pos_hint: {"center_y": .5}
            halign: "right"
            font_size: dp(25)

    MDBoxLayout:
        size_hint: (1, None)
        height: dp(46)
        padding: dp(2), dp(6), dp(10), dp(0)

        MDBoxLayout
            size_hint: (1, 1)
            CustomLabel:
                text: " [color=ffffff]Transaction Details[/color]"

        MDBoxLayout:
            size_hint: (None, None)
            size: ("23dp", "23dp")
            pos_hint: {"center_y": .5}

            MDIcon:
                icon: "chevron-down"
                halign: "center"

    MDBoxLayout:
        md_bg_color: app._light
        background: "assets/images/bg5.jpg"
        orientation: "vertical"
        size_hint: (1, None)
        height: dp(230)
        spacing: dp(11.5)
        padding: dp(6)
        radius: dp(23)

        MDBoxLayout:
            orientation: "vertical"
            size_hint: (1, 1)
            spacing: dp(2)

            CEPOneLineListItem:
                left_text: "Transaction ID"
                right_text: f"{root.t_id}"

            CEPOneLineListItem:
                left_text: "Transaction Fee"
                right_text: f"{root.t_fee}"

            CEPOneLineListItem:
                left_text: "Sender Acc."
                right_text: f"{root.sender_acc}"
                list_height: 46

            CEPOneLineListItem:
                id: receiver_acc
                left_text: "Receiver Acc."
                right_text: f"{root.receiver_acc}"
                list_height: 46

            CEPOneLineListItem:
                id: t_category
                left_text: "Transaction Category "
                right_text: f"{root.t_category}"
                list_height: 43

<RecentTransaction>:
    orientation: "vertical"
    pos_hint: {"center_x": .5, "center_y": .5}

    MDBoxLayout:
        md_bg_color: app._tinted
        size_hint: (1, None)
        height: dp(75)
        pos_hint: {"center_x": .5}
        padding: dp(0)
        radius: dp(17.5)

        MDBoxLayout:
            orientation: "vertical"
            size_hint: (1, 1)
            padding: dp(6)

            CustomLabel:
                text: f"[b][size=15dp]{root.left_text}[/size][/b]"
                halign: "left"
                text_color: "#ffffff"
                shorten: True

        MDBoxLayout:
            orientation: "vertical"
            size_hint: (1, 1)
            padding: dp(6)

            CustomLabel:
                text: f"[b][size=17dp]{root.right_text}[/size][/b]"
                halign: "right"
                text_color: "#2fc46cff" if "+" in root.right_text else "#ff3f4fff"

    MDBoxLayout:
        orientation: "horizontal"
        size_hint: (1, None)
        height: dp(23)
        spacing: dp(6)
        padding: dp(2), dp(6), dp(17.5), dp(0)

        MDIcon:
            icon: "clock"
            pos_hint: {"center_y": .5}
            halign: "left"
            theme_text_color: "Custom"
            text_color: app._blue
            font_size: dp(21)
            size_hint_x: None
            width: dp(30)

        CustomLabel:
            text: f"[b][size=14dp][color=ffffff]   {root.t_time}[/size][b]"
            halign: "left"

        MDIcon:
            icon: f"{root.icon_path}"
            pos_hint: {"center_y": .5}
            halign: "right"
            font_size: dp(25)

<CustomInputDialogContent>:
    orientation: "vertical"
    spacing: dp(23)
    size_hint: (.9, .9)
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(23)
        MDLabel:
            text: "Password Reset Request\\n\\n[size=16dp]Please enter your account's email." + \
                " A password reset link will be sent there. If you are unable to" + \
                " locate it, try checking your spam folder.\\n\\n[/size]"
            halign: "left"
            font_style: "H6"
            markup: True

        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(23)
            padding: dp(0), dp(-136), dp(0), dp(106)
            TextFieldNormal:
                id: password_reset_mail
                hint_text: "Email"

            MDBoxLayout:
                size_hint_y: None 
                height: dp(44)

                MDRoundFlatButton:
                    text: "Request Password Reset Link"
                    font_size: dp(16)
                    theme_text_color: "Custom"
                    text_color: "#ffffff"
                    md_bg_color: "#aaaaaa26"
                    line_color: "#005eff"
                    size_hint: (1, 1)
                    on_release: 
                        app.request_password_reset_link(f"{password_reset_mail.text}") if len(password_reset_mail.text) >= 6 else None

<CryptoHelpContent>:
    orientation: "vertical"
    spacing: dp(23)
    size_hint: (.9, .9)

    MDBoxLayout:
        MDScrollView:
            do_scroll_x: False
            do_scroll_y: True
            scroll_cls: "ScrollEffect"

            MDBoxLayout:
                id: general_insight
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height

                LabelChunks:
                    text: root.help_text

    MDBoxLayout:
        size_hint_y: None
        height: dp(43)

        MDBoxLayout:
            size_hint: (1, 1)
        
        MDBoxLayout:
            size_hint: (None, None)
            size: ("136dp", "43dp") 

            MDRectangleFlatButton:
                text: "GOT IT"
                font_size: "16dp"
                theme_text_color: "Custom"
                text_color: "#ffffff"
                md_bg_color: "#aaaaaa26"
                line_color: "#005eff"
                size_hint: (1, 1)
                on_release: app.root.get_screen('wallet_setup_screen').close_crypto_help_dialog()

<KBItem>:
    size_hint: (1, None)
    height: dp(65)
    md_bg_color: root.bg_color
    radius: dp(0)
    orientation: "vertical"

    MDBoxLayout:
        md_bg_color: app._gray
        size_hint: (1, None)
        height: dp(.9)
        pos_hint: {"top": 1}

    MDBoxLayout:
        padding: dp(10)
        spacing: dp(10)
        MDLabel:
            text: root.sr_name
            halign: "left"
            theme_text_color: "Custom"
            text_color: app._white
            font_size: "15dp"

        TextFieldNormal:
            text: root.t_category
            size_hint: (None, None)
            size: ("170dp", "30dp")
            pos_hint: {"center_y": .5}
            readonly: True
            font_size: "15dp"
            fill_color_normal: app._tinted
            fill_color_focus: app._tinted
            text_color_normal: "#ffffff"
            text_color_focus: "#ffffff"
            on_touch_down:
                if self.collide_point(*args[1].pos): app.root.get_screen('tx_kb_screen').open_category_menu(self, root.sr_name)

"""

Builder.load_string(REUSABLES)


class TopLeftBackButton(MDIconButton):
    pass


class TextFieldNormal(MDTextField):
    pass


class PasswordTextField(MDRelativeLayout):
    text, hint_text = StringProperty(), StringProperty()

    def on_kv_post(self, base_widget):
        self.ids.password.bind(text=self.setter("text"), hint_text=self.setter("hint_text"))


class KeyItem(MDBoxLayout):
    key_color, key_text = ColorProperty(), StringProperty()


class WidgetContainer(MDCard):
    pass


class LeftIconContainer(MDBoxLayout):
    pass


class GridCard(MDCard):
    icon_path, grid_card_txt = StringProperty(""), StringProperty("")


class CustomLabel(MDLabel):
    pass


class LabelChunks(MDLabel):
    pass


class RightArrow(MDBoxLayout):
    pass


class HiddenCard(MDCard):
    swipe_threshold = NumericProperty(96)
    _touch_start_y = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos): self._touch_start_y = touch.y
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self._touch_start_y is not None and touch.y < self._touch_start_y:
            swipe_distance = self._touch_start_y - touch.y
            if swipe_distance > self.swipe_threshold: self.close_card()
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        self._touch_start_y = None
        return super().on_touch_up(touch)

    def close_card(self):
        anim = Animation(y=-self.height, duration=.2)
        anim.start(self)

    def open_card(self):
        anim = Animation(y=0, duration=.2)
        anim.start(self)


class CustomCard(MDCard):
    pass


class CustomCardLayout(MDBoxLayout):
    pass


class CustomCardIdentifier(CustomLabel):
    pass


class CustomCardTitleBar(MDBoxLayout):
    title = StringProperty()


class CustomCardGraph(MDBoxLayout):
    pass


class CustomCardTitleBarAlt(MDBoxLayout):
    left_text, right_text = StringProperty(), StringProperty()


class CustomCardListItem(MDBoxLayout):
    c_bg_color, icon_path, left_text, right_text = ColorProperty(), StringProperty(), StringProperty(), StringProperty()


class ExpenseCategoryCard(CustomCard):
    # e_cat_val means expense category value
    e_cat_val1, e_cat_val2, e_cat_val3, e_cat_val4, e_cat_val5 = StringProperty(), StringProperty(), StringProperty(), StringProperty(), StringProperty()


class IncomeCategoryCard(CustomCard):
    # i_cat_val means income category value
    i_cat_val1, i_cat_val2, i_cat_val3, i_cat_val4, i_cat_val5 = StringProperty(), StringProperty(), StringProperty(), StringProperty(), StringProperty()


class Spacer(Widget):
    pass


class FinancialReportsButton(MDCard):
    pass


class HiddenCardReportsContent(MDBoxLayout):
    date_time_label, info_text_label = StringProperty(""), StringProperty("")


class DownloadReportButton(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def trigger_download(self):
        self.dispatch('on_release')


class CloseCardButton(MDIconButton):
    pass


class Tab(MDRelativeLayout, MDTabsBase):
    pass


class CustomTabs(MDTabs):
    pass


class InsightCard(MDCard):
    pass


class InsightScreenTopBar(MDCard):
    pass


class CustomTwoLineListItem(TwoLineListItem):
    icon_path, left_text, right_text = StringProperty(), StringProperty(), StringProperty()


class AllTransactionsCard(MDBoxLayout):
    # "sr" means "sender or receiver", "t" means "transaction"
    sr_name, amount, t_time, acc_type = StringProperty(""), StringProperty("") , StringProperty(""), StringProperty("")
    t_id, t_fee, sender_acc, receiver_acc, t_category = StringProperty(""), StringProperty(""), StringProperty(""), StringProperty(""), StringProperty("")


class RV(RecycleView):
    pass


class CEPOneLineListItem(MDBoxLayout):
    # CEP Means CustomExpansionPanel
    left_text, right_text, list_height = StringProperty(), StringProperty(), NumericProperty(36)


class FileChooserDialog(ModalView):
    def __init__(self, on_select_callback, **kwargs):
        super().__init__(**kwargs)
        self.background_color = "#0001ffff"
        self.overlay_color = "#36363622"
        self.on_select_callback = on_select_callback
        self.size_hint = (.95, .8)
        self.auto_dismiss = True

        file_dialog_heading = MDBoxLayout(size_hint_y=None, height=dp(26), padding=dp(8))
        file_dialog_heading_txt = MDLabel(text="Profile Pic Updater", halign="center", font_style="H6")

        start_path = storagepath.get_pictures_dir() if platform == "android" else os.getcwd()

        layout = MDBoxLayout(orientation='vertical', spacing=dp(23), padding=dp(17.5))
        self.file_chooser = FileChooserListView(
            path=start_path,
            filters=["*.jpg", "*.jpeg", "*.png", "*.webp"]
        )

        button_background = MDBoxLayout(size_hint_y=None, height=dp(46))

        select_button = MDRoundFlatButton(
            text="Update Profile Photo",
            theme_text_color="Custom",
            text_color="#ffffff",
            md_bg_color="#aaaaaa26",
            line_color="#005eff",
            size_hint=(1, 1)
        )
        select_button.bind(on_release=self.select_file)

        file_dialog_heading.add_widget(file_dialog_heading_txt)
        layout.add_widget(file_dialog_heading)
        layout.add_widget(self.file_chooser)
        button_background.add_widget(select_button)
        layout.add_widget(button_background)
        self.add_widget(layout)

        Window.bind(on_keyboard=self.on_back_button)

    def select_file(self, *args):
        selection = self.file_chooser.selection
        if selection:
            self.on_select_callback(selection[0])
            self.dismiss()

    def on_back_button(self, window, key, *args):
        if key == 27:
            self.dismiss()
            return True
        return False

    def on_dismiss(self):
        Window.unbind(on_keyboard=self.on_back_button)


class RecentTransaction(MDBoxLayout):
    left_text, right_text, t_time, icon_path = StringProperty(""), StringProperty(""), StringProperty(""), StringProperty("")


class CustomInputDialogContent(MDBoxLayout):
    pass


class CustomInputDialog(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = "#0001ffff"
        self.overlay_color = "#36363622"
        self.size_hint = (.95, .7)
        self.auto_dismiss = True
        content = CustomInputDialogContent()

        Window.bind(on_keyboard=self.on_back_button)
        self.add_widget(content)

    def on_back_button(self, window, key, *args):
        if key == 27:
            self.dismiss()
            return True
        return False

    def on_dismiss(self):
        Window.unbind(on_keyboard=self.on_back_button)


class CryptoHelpContent(MDBoxLayout):
    help_text = StringProperty("")
    with open("assets/crypto_setup_help.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    help_text = MarkdownFormatter().format_text("".join(lines))


class CryptoHelpDialog(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = "#0001ffff"
        self.overlay_color = "#36363622"
        self.size_hint = (.95, .85)
        self.auto_dismiss = True
        content = CryptoHelpContent()

        Window.bind(on_keyboard=self.on_back_button)
        self.add_widget(content)

    def on_back_button(self, window, key, *args):
        if key == 27:
            self.dismiss()
            return True
        return False

    def on_dismiss(self):
        Window.unbind(on_keyboard=self.on_back_button)


class CustomPieChart(AKPieChart):
    custom_colors = []

    def _make_chart(self, items):
        self.size = (min(self.size), min(self.size))
        if not items:
            raise Exception("Items cannot be empty.")

        items = self._format_items(items)
        angle_start = 0
        color_item = 0
        circle_center = [
            self.pos[0] + self.size[0] / 2,
            self.pos[1] + self.size[1] / 2,
        ]

        for title, value in items.items():
            with self.canvas.before:
                if self.starting_animation: alpha = 0
                else: alpha = 1

                if color_item < len(self.custom_colors):
                    color = get_color_from_hex(self.custom_colors[color_item])
                else:
                    from kivymd.color_definitions import colors, palette
                    color = get_color_from_hex(
                        colors[palette[color_item]]["500"]
                    )

                c = Color(rgb=color, a=alpha)

                if self.starting_animation:
                    e = Ellipse(
                        pos=self.pos,
                        size=self.size,
                        angle_start=angle_start,
                        angle_end=angle_start + 0.01,
                    )

                    anim = Animation(
                        size=self.size,
                        angle_end=angle_start + value,
                        duration=self.duration,
                        t=self.transition,
                    )
                    anim_opcity = Animation(a=1, duration=self.duration * 0.5)

                    anim_opcity.start(c)
                    anim.start(e)
                else:
                    Ellipse(
                        pos=self.pos,
                        size=self.size,
                        angle_start=angle_start,
                        angle_end=angle_start + value,
                    )

            color_item += 1
            angle_start += value

        angle_start = 0
        for title, value in items.items():
            if value == 0:
                angle_start += value
                continue

            with self.canvas.after:
                label_pos = point_on_circle(
                    (angle_start + angle_start + value) / 2,
                    circle_center,
                    self.size[0] / 3,
                )
                number_anim = PieChartNumberLabel(
                    x=label_pos[0], y=label_pos[1], title=title
                )
                number_anim.theme_text_color = "Custom"
                number_anim.text_color = "#00001fff"
                Animation(percent=value * 100 / 360).start(number_anim)

            angle_start += value


class KBItem(MDBoxLayout):
    sr_name, t_category, bg_color = StringProperty(""), StringProperty(""), ColorProperty()
