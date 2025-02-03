from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.textfield import MDTextField

REUSABLES = """

<TopLeftBackButton>:
    icon: "arrow-left"
    icon_size: "24dp"
    pos_hint: {"center_x": .1, "center_y": .935}
    theme_text_color: "Custom"
    text_color: app._white
    _no_ripple_effect: True
    on_release: app.go_back()

<TextFieldNormal>:
    size_hint_x: .85
    mode: "rectangle"
    helper_text_mode: "persistent"
    line_color_focus: app._blue
    line_color_normal: app._white
    text_color_focus: app._white
    text_color_normal: app._white
    hint_text_color_focus: app._gray
    hint_text_color_normal: app._white
    icon_right_color_focus: app._white
    icon_right_color_normal: app._white

<PasswordTextField>:
    size_hint: .85, None
    height: password.height - 10

    MDTextField:
        id: password
        hint_text: root.hint_text
        text: root.text
        password: True
        mode: "rectangle"
        helper_text_mode: "persistent"
        line_color_focus: app._blue
        line_color_normal: app._white
        text_color_focus: app._white
        text_color_normal: app._white
        hint_text_color_focus: app._gray
        hint_text_color_normal: app._white

    MDIconButton:
        icon: "eye-off"
        pos_hint: {"center_y": .5}
        pos: password.width - self.width, 0
        theme_icon_color: "Custom"
        icon_color: app._white
        _no_ripple_effect: True
        on_release:
            self.icon = "eye" if self.icon == "eye-off" else "eye-off"
            password.password = False if password.password is True else True

<SlideIndicator>:
    md_bg_color: app._gray
    size_hint: (None, None)
    size: ("7.63dp", "7.63dp")
    pos_hint: {"center_y": .5}
    radius: self.height / 2

<NavIconButton>:
    _no_ripple_effect: True
    md_bg_color: app._invisible
    size_hint: (1, 1)
    pos_hint: {"center_y": .5}

<WidgetContainer>:
    md_bg_color: app._tinted
    size_hint: (.9, .085)
    radius: dp(11.5)
    padding: dp(6)

<LeftIconContainer>:
    size_hint: (None, None)
    size: ("43dp", "43dp")
    pos_hint: {"center_y": .5}

<CustomLabel>:
    halign: "left"
    markup: True
    font_size: "16dp"
    pos_hint: {"center_y": .5}
    theme_text_color: "Custom"
    text_color: app._white

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

"""

Builder.load_string(REUSABLES)


class TopLeftBackButton(MDIconButton):
    pass


class TextFieldNormal(MDTextField):
    pass


class PasswordTextField(MDRelativeLayout):
    text, hint_text = StringProperty(), StringProperty()

    def on_kv_post(self, base_widget):
        self.ids.password.bind(
            text=self.setter("text"),
            hint_text=self.setter("hint_text"),
        )


class SlideIndicator(MDCard):
    pass


class NavIconButton(MDIconButton):
    pass


class WidgetContainer(MDCard):
    pass


class LeftIconContainer(MDBoxLayout):
    pass


class CustomLabel(MDLabel):
    pass


class RightArrow(MDBoxLayout):
    pass


class HiddenCard(MDCard):
    pass


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
