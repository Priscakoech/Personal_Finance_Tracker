import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button

class LoadingScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20

        # Add the loading GIF
        self.loading_gif = AsyncImage(
            source='loading.gif',  # Path to your loading GIF
            anim_delay=0.1,       # Adjust animation speed
            size_hint=(1, 0.8)    # Adjust size
        )
        self.add_widget(self.loading_gif)

        # Add a label for status
        self.status_label = Label(text="Checking internet connection...", size_hint=(1, 0.2))
        self.add_widget(self.status_label)

        # Check internet connectivity
        self.check_internet()

    def check_internet(self):
        # Check internet connectivity
        try:
            response = requests.get("https://www.google.com", timeout=5)
            if response.status_code == 200:
                self.status_label.text = "Internet connected!"
                Clock.schedule_once(self.go_to_main_screen, 2)  # Proceed after 2 seconds
            else:
                self.show_no_internet_popup()
        except requests.ConnectionError:
            self.show_no_internet_popup()

    def show_no_internet_popup(self):
        # Display a popup if no internet is found
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text="No internet connection!"))
        retry_button = Button(text="Retry", size_hint=(1, 0.2))
        retry_button.bind(on_press=self.retry_check)
        popup_layout.add_widget(retry_button)

        self.popup = Popup(title="Connection Error", content=popup_layout, size_hint=(0.8, 0.4))
        self.popup.open()

    def retry_check(self, instance):
        # Retry internet check
        self.popup.dismiss()
        self.check_internet()

    def go_to_main_screen(self, dt):
        # Replace this with your main screen logic
        self.clear_widgets()  # Clear the loading screen
        self.add_widget(Label(text="Unleashing the magic ... just a moment!", font_size=30))  # Transition to the main screen


class MyApp(App):
    def build(self):
        return LoadingScreen()


if __name__ == '__main__':
    MyApp().run()